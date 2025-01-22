#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import argparse as _argparse
import collections as _collections
import collections.abc as _abc
import csv as _csv
import fnmatch as _fnmatch
import http.server as _http
import math as _math
import mistune as _mistune
import multiprocessing as _multiprocessing
import os as _os
import re as _re
import shutil as _shutil
import subprocess as _subprocess
import sys as _sys
import threading as _threading
import types as _types
import yaml as _yaml

from html import escape as _escape
from html.parser import HTMLParser
from urllib import parse as _urlparse

__all__ = ["Transom", "TransomCommand"]

_default_page_template = """
<!DOCTYPE html>
<html>
  {{page.head}}
  {{page.body}}
</html>
"""

_default_head_template = """
<head>
  <title>{{page.title}}</title>
  <link rel="icon" href="data:;"/>
  {{page.extra_headers}}
</head>
"""

_default_body_template = """
<body>
  {{page.content}}
</body>
"""

_index_file_names = "index.md", "index.html.in", "index.html"
_markdown_title_regex = _re.compile(r"(#|##) (.+)")
_variable_regex = _re.compile(r"({{{.+?}}}|{{.+?}})")

# An improvised solution for trouble on Mac OS
_once = False
if not _once:
    _multiprocessing.set_start_method("fork")
    _once = True

class Transom:
    def __init__(self, project_dir, verbose=False, quiet=False):
        self.project_dir = _os.path.normpath(project_dir)
        self.config_dir = _os.path.normpath(_os.path.join(self.project_dir, "config"))
        self.input_dir = _os.path.normpath(_os.path.join(self.project_dir, "input"))
        self.output_dir = _os.path.normpath(_os.path.join(self.project_dir, "output"))

        self.verbose = verbose
        self.quiet = quiet

        self.ignored_file_patterns = [".git", ".svn", ".#*", "#*"]
        self.ignored_link_patterns = []

        self._config = {
            "site": self,
            "lipsum": lipsum,
            "plural": plural,
            "html_table": html_table,
            "html_table_csv": html_table_csv,
        }

        self._body_template = None
        self._page_template = None

        self._config_modified = False

        self._files = list()
        self._index_files = dict() # parent input dir => _File

    def init(self):
        self._page_template = load_site_template(_os.path.join(self.config_dir, "page.html"), _default_page_template)
        self._head_template = load_site_template(_os.path.join(self.config_dir, "head.html"), _default_head_template)
        self._body_template = load_site_template(_os.path.join(self.config_dir, "body.html"), _default_body_template)

        self._ignored_file_regex = "({})".format("|".join([_fnmatch.translate(x) for x in self.ignored_file_patterns]))
        self._ignored_file_regex = _re.compile(self._ignored_file_regex)

        try:
            exec(read_file(_os.path.join(self.config_dir, "config.py")), self._config)
        except FileNotFoundError as e:
            self.warning("Config file not found: {}", e)

    def _get_config_modified(self, output_mtime):
        for root, dirs, names in _os.walk(self.config_dir):
            for name in {x for x in names if not self._ignored_file_regex.match(x)}:
                mtime = _os.path.getmtime(_os.path.join(root, name))

                if mtime > output_mtime:
                    return True

        return False

    def _init_files(self):
        self._files.clear()
        self._index_files.clear()

        for root, dirs, names in _os.walk(self.input_dir):
            files = {x for x in names if not self._ignored_file_regex.match(x)}
            index_files = {x for x in names if x in _index_file_names}

            if len(index_files) > 1:
                raise Exception(f"Duplicate index files in {root}")

            for name in index_files:
                self._files.append(self._init_file(_os.path.join(root, name)))

            for name in files - index_files:
                self._files.append(self._init_file(_os.path.join(root, name)))

    def _init_file(self, input_path):
        output_path = _os.path.join(self.output_dir, input_path[len(self.input_dir) + 1:])

        if input_path.endswith(".md"):
            return MarkdownPage(self, input_path, f"{output_path[:-3]}.html")
        elif input_path.endswith(".html.in"):
            return TemplatePage(self, input_path, output_path[:-3])
        else:
            return File(self, input_path, output_path)

    def render(self, force=False):
        self.notice("Rendering files from '{}' to '{}'", self.input_dir, self.output_dir)

        if _os.path.exists(self.output_dir):
            output_mtime = _os.path.getmtime(self.output_dir)
            self._config_modified = self._get_config_modified(output_mtime)

        self._init_files()

        self.notice("Found {:,} input {}", len(self._files), plural("file", len(self._files)))

        # XXX Consider parallizing this too
        for file_ in self._files:
            file_._process_input()

        proc_count = _os.cpu_count()
        procs = list()
        batch_size = _math.ceil(len(self._files) / proc_count)

        for i in range(proc_count):
            start = i * batch_size
            end = start + batch_size

            procs.append(RenderProcess(self._files[start:end], force))

        for proc in procs:
            proc.start()

        for proc in procs:
            proc.join()

            if proc.exitcode != 0:
                raise Exception("A child render process failed")

        if _os.path.exists(self.output_dir):
            _os.utime(self.output_dir)

        rendered_count = sum([x.rendered_count.value for x in procs])
        unmodified_count = len(self._files) - rendered_count
        unmodified_note = ""

        if unmodified_count > 0:
            unmodified_note = " ({:,} unchanged)".format(unmodified_count)

        self.notice("Rendered {:,} output {}{}", rendered_count, plural("file", rendered_count), unmodified_note)

    def serve(self, port=8080):
        watcher = None

        try:
            watcher = WatcherThread(self)
        except ImportError: # pragma: nocover
            self.notice("Failed to import pyinotify, so I won't auto-render updated input files")
            self.notice("Try installing the Python inotify package")
            self.notice("On Fedora, use 'dnf install python-inotify'")
        else:
            watcher.start()

        try:
            server = ServerThread(self, port)
            server.run()
        finally:
            if watcher is not None:
                watcher.stop()

    def check_files(self):
        self._init_files()

        expected_paths = {x.output_path for x in self._files}
        found_paths = set()

        for root, dirs, names in _os.walk(self.output_dir):
            found_paths.update((_os.path.join(root, x) for x in names))

        missing_paths = expected_paths - found_paths
        extra_paths = found_paths - expected_paths

        if missing_paths:
            print("Missing output files:")

            for path in sorted(missing_paths):
                print(f"  {path}")

        if extra_paths:
            print("Extra output files:")

            for path in sorted(extra_paths):
                print(f"  {path}")

        return len(missing_paths), len(extra_paths)

    def check_links(self):
        self._init_files()

        link_sources = _collections.defaultdict(set) # link => files
        link_targets = set()

        for file_ in self._files:
            file_._collect_link_data(link_sources, link_targets)

        def not_ignored(link):
            return not any((_fnmatch.fnmatchcase(link, x) for x in self.ignored_link_patterns))

        links = filter(not_ignored, link_sources.keys())
        errors = 0

        for link in links:
            if link not in link_targets:
                errors += 1

                print(f"Error: Link to '{link}' has no destination")

                for source in link_sources[link]:
                    print(f"  Source: {source.input_path}")

        return errors

    def debug(self, message, *args):
        if self.verbose:
            print(message.format(*args))

    def notice(self, message, *args):
        if not self.quiet:
            print(message.format(*args))

    def warning(self, message, *args):
        print("Warning:", message.format(*args))

class File:
    __slots__ = "site", "input_path", "_input_mtime", "output_path", "_output_mtime", "_rendered", \
        "url", "title", "parent"

    def __init__(self, site, input_path, output_path):
        self.site = site

        self.input_path = input_path
        self._input_mtime = _os.path.getmtime(self.input_path)

        self.output_path = output_path
        self._output_mtime = None

        self._rendered = False

        self.url = self.output_path[len(self.site.output_dir):]
        self.title = ""
        self.parent = None

        dir_, name = _os.path.split(self.input_path)

        if name in _index_file_names:
            self.site._index_files[dir_] = self
            dir_ = _os.path.dirname(dir_)

        while dir_ != "":
            try:
                self.parent = self.site._index_files[dir_]
            except KeyError:
                dir_ = _os.path.dirname(dir_)
            else:
                break

    def __repr__(self):
        return f"{self.__class__.__name__}({self.input_path}, {self.output_path})"

    def _process_input(self): # pragma: nocover
        pass

    def _render(self, force=False):
        if not force and not self._is_modified():
            return

        self.site.debug("Rendering {}", self)

        self._render_content()

        self._rendered = True

    def _is_modified(self):
        if self._output_mtime is None:
            try:
                self._output_mtime = _os.path.getmtime(self.output_path)
            except FileNotFoundError:
                return True

        return self._input_mtime > self._output_mtime

    def _render_content(self):
        copy_file(self.input_path, self.output_path)

    def _collect_link_data(self, link_sources, link_targets):
        link_targets.add(self.url)

        if not self.url.endswith(".html"):
            return

        parser = LinkParser(self, link_sources, link_targets)
        parser.feed(read_file(self.output_path))

    @property
    def ancestors(self):
        file_ = self

        while file_ is not None:
            yield file_
            file_ = file_.parent

    @property
    def children(self):
        for file_ in self.site._files:
            if file_.parent is self:
                yield file_

class LinkParser(HTMLParser):
    def __init__(self, file_, link_sources, link_targets):
        super().__init__()

        self.file = file_
        self.link_sources = link_sources
        self.link_targets = link_targets

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        for name in ("href", "src", "action"):
            try:
                url = attrs[name]
            except KeyError:
                continue

            split_url = _urlparse.urlsplit(url)

            if split_url.scheme or split_url.netloc:
                continue

            normalized_url = _urlparse.urljoin(self.file.url, _urlparse.urlunsplit(split_url))

            self.link_sources[normalized_url].add(self.file)

        if "id" in attrs:
            normalized_url = _urlparse.urljoin(self.file.url, f"#{attrs['id']}")

            if normalized_url in self.link_targets:
                self.file.site.warning("Duplicate link target in '{}'", normalized_url)

            self.link_targets.add(normalized_url)

class TemplatePage(File):
    __slots__ = "_content", "metadata", "_page_template", "_head_template", "_body_template"

    def _process_input(self):
        self._content = read_file(self.input_path)
        self._content, self.metadata = extract_metadata(self._content)

        self.title = self.metadata.get("title", self.title)

        try:
            self._page_template = load_page_template(self.metadata["page_template"], "")
        except KeyError:
            self._page_template = self.site._page_template

        try:
            self._head_template = load_page_template(self.metadata["head_template"], "")
        except KeyError:
            self._head_template = self.site._head_template

        try:
            self._body_template = load_page_template(self.metadata["body_template"], "{{page.content}}")
        except KeyError:
            self._body_template = self.site._body_template

    def _is_modified(self):
        return self.site._config_modified or super()._is_modified()

    def _render_content(self):
        if not hasattr(self, "_content"):
            self._process_input()

        _os.makedirs(_os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w") as f:
            for elem in self._render_template(self._page_template):
                f.write(elem)

    @property
    def head(self):
        return self._render_template(self._head_template)

    @property
    def extra_headers(self):
        return self.metadata.get("extra_headers", "")

    @property
    def body(self):
        return self._render_template(self._body_template)

    @property
    def content(self):
        parsed = parse_template(self._content)
        rendered = "".join(self._render_template(parsed))

        return self._convert_content(rendered)

    def path_nav(self, start=None, end=None):
        files = reversed(list(self.ancestors))
        links = [f"<a href=\"{x.url}\">{x.title}</a>" for x in files]

        return f"<nav class=\"path-nav\">{''.join(links)}</nav>"

    def _convert_content(self, content):
        return content

    def _render_template(self, template):
        local_vars = {"page": self}

        for elem in template:
            if type(elem) is _types.CodeType:
                result = eval(elem, self.site._config, local_vars)

                if type(result) is _types.GeneratorType:
                    yield from result
                else:
                    yield result
            else:
                yield elem

    def render_text(self, text, markdown=False):
        if markdown:
            text = convert_markdown(text)

        return self._render_template(parse_template(text))

    def include(self, input_path):
        return self.render_text(read_file(input_path), markdown=input_path.endswith(".md"))

class MarkdownPage(TemplatePage):
    __slots__ = ()

    def _process_input(self):
        super()._process_input()

        if not self.title:
            match = _markdown_title_regex.search(self._content)
            self.title = match.group(2).strip() if match else ""

    def _convert_content(self, content):
        return convert_markdown(content)

class RenderProcess(_multiprocessing.Process):
    def __init__(self, files, force):
        super().__init__()

        self.files = files
        self.force = force
        self.rendered_count = _multiprocessing.Value('L', 0)

    def run(self):
        rendered_count = 0

        for file_ in self.files:
            file_._render(force=self.force)

            if file_._rendered:
                rendered_count += 1

        self.rendered_count.value = rendered_count

class WatcherThread:
    def __init__(self, site):
        import pyinotify as _pyinotify

        self.site = site

        watcher = _pyinotify.WatchManager()
        mask = _pyinotify.IN_CREATE | _pyinotify.IN_MODIFY

        def render_file(event):
            input_path = _os.path.relpath(event.pathname, _os.getcwd())
            _, base_name = _os.path.split(input_path)

            if _os.path.isdir(input_path):
                return True

            if self.site._ignored_file_regex.match(base_name):
                return True

            try:
                file_ = self.site._init_file(input_path)
            except FileNotFoundError:
                return True

            file_._render()

            if _os.path.exists(self.site.output_dir):
                _os.utime(self.site.output_dir)

        def render_site(event):
            self.site.init()
            self.site.render()

        watcher.add_watch(self.site.input_dir, mask, render_file, rec=True, auto_add=True)
        watcher.add_watch(self.site.config_dir, mask, render_site, rec=True, auto_add=True)

        self.notifier = _pyinotify.ThreadedNotifier(watcher)

    def start(self):
        self.site.notice("Watching for input file changes")
        self.notifier.start()

    def stop(self):
        self.notifier.stop()

class ServerThread(_threading.Thread):
    def __init__(self, site, port):
        super().__init__(name="server", daemon=True)

        self.site = site
        self.port = port
        self.server = Server(site, port)

    def run(self):
        self.site.notice("Serving at http://localhost:{}", self.port)
        self.server.serve_forever()

class Server(_http.ThreadingHTTPServer):
    def __init__(self, site, port):
        super().__init__(("localhost", port), ServerRequestHandler)

        self.site = site

class ServerRequestHandler(_http.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, directory=None):
        super().__init__(request, client_address, server, directory=server.site.output_dir)

    def do_POST(self):
        if self.path == "/RENDER":
            self.server.site.render()
        elif self.path == "/STOP":
            self.server.shutdown()
        else:
            raise Exception()

        self.send_response(_http.HTTPStatus.OK)
        self.end_headers()

class TransomCommand:
    def __init__(self, home=None):
        self.home = home
        self.name = "transom"

        self.parser = _argparse.ArgumentParser()
        self.parser.description = "Generate static websites from Markdown and Python"
        self.parser.formatter_class = _argparse.RawDescriptionHelpFormatter

        self.args = None
        self.quiet = False
        self.verbose = False

        subparsers = self.parser.add_subparsers(title="subcommands")

        common = _argparse.ArgumentParser()
        common.add_argument("--init-only", action="store_true",
                            help=_argparse.SUPPRESS)
        common.add_argument("--verbose", action="store_true",
                            help="Print detailed logging to the console")
        common.add_argument("--quiet", action="store_true",
                            help="Print no logging to the console")
        common.add_argument("--output", metavar="OUTPUT-DIR",
                            help="The output directory (default: PROJECT-DIR/output)")
        common.add_argument("project_dir", metavar="PROJECT-DIR", nargs="?", default=".",
                            help="The project root directory (default: current directory)")

        init = subparsers.add_parser("init", parents=[common], add_help=False,
                                     help="Prepare an input directory")
        init.set_defaults(command_fn=self.init_command)
        init.add_argument("--profile", metavar="PROFILE", choices=("website", "webapp"), default="website",
                          help="Select starter files for different scenarios (default: website)")
        init.add_argument("--github", action="store_true",
                          help="Add extra files for use in a GitHub repo")

        render = subparsers.add_parser("render", parents=[common], add_help=False,
                                       help="Generate output files")
        render.set_defaults(command_fn=self.render_command)
        render.add_argument("--force", action="store_true",
                            help="Render all input files, including unmodified ones")

        render = subparsers.add_parser("serve", parents=[common], add_help=False,
                                       help="Generate output files and serve the site on a local port")
        render.set_defaults(command_fn=self.serve_command)
        render.add_argument("--port", type=int, metavar="PORT", default=8080,
                            help="Listen on PORT (default 8080)")
        render.add_argument("--force", action="store_true",
                            help="Render all input files, including unmodified ones")

        check_links = subparsers.add_parser("check-links", parents=[common], add_help=False,
                                            help="Check for broken links")
        check_links.set_defaults(command_fn=self.check_links_command)

        check_files = subparsers.add_parser("check-files", parents=[common], add_help=False,
                                            help="Check for missing or extra files")
        check_files.set_defaults(command_fn=self.check_files_command)

    def init(self, args=None):
        self.args = self.parser.parse_args(args)

        if "command_fn" not in self.args:
            self.parser.print_usage()
            _sys.exit(1)

        self.quiet = self.args.quiet
        self.verbose = self.args.verbose

        if self.args.command_fn != self.init_command:
            self.lib = Transom(self.args.project_dir, verbose=self.verbose, quiet=self.quiet)

            if self.args.output:
                self.lib.output_dir = self.args.output

            self.lib.init()

    def main(self, args=None):
        self.init(args)

        assert self.args is not None

        if self.args.init_only:
            return

        try:
            self.args.command_fn()
        except KeyboardInterrupt: # pragma: nocover
            pass

    def notice(self, message, *args):
        if not self.quiet:
            self.print_message(message, *args)

    def warning(self, message, *args):
        message = "Warning: {}".format(message)
        self.print_message(message, *args)

    def error(self, message, *args):
        message = "Error! {}".format(message)
        self.print_message(message, *args)

    def fail(self, message, *args):
        self.error(message, *args)
        _sys.exit(1)

    def print_message(self, message, *args):
        message = message[0].upper() + message[1:]
        message = message.format(*args)
        message = "{}: {}".format(self.name, message)

        _sys.stderr.write("{}\n".format(message))
        _sys.stderr.flush()

    def init_command(self):
        if self.home is None:
            self.fail("I can't find the default input files")

        def copy(from_path, to_path):
            if _os.path.exists(to_path):
                self.notice("Skipping '{}'. It already exists.", to_path)
                return

            copy_path(from_path, to_path)

            self.notice("Creating '{}'", to_path)

        profile_dir = _os.path.join(self.home, "profiles", self.args.profile)
        project_dir = self.args.project_dir

        assert _os.path.exists(profile_dir), profile_dir

        for name in _os.listdir(_os.path.join(profile_dir, "config")):
            copy(_os.path.join(profile_dir, "config", name),
                 _os.path.join(project_dir, "config", name))

        for name in _os.listdir(_os.path.join(profile_dir, "input")):
            copy(_os.path.join(profile_dir, "input", name),
                 _os.path.join(project_dir, "input", name))

        if self.args.github:
            python_dir = _os.path.join(self.home, "python")

            copy(_os.path.join(profile_dir, ".github/workflows/main.yaml"),
                 _os.path.join(project_dir, ".github/workflows/main.yaml"))
            copy(_os.path.join(profile_dir, ".gitignore"), _os.path.join(project_dir, ".gitignore"))
            copy(_os.path.join(profile_dir, ".plano.py"), _os.path.join(project_dir, ".plano.py"))
            copy(_os.path.join(python_dir, "mistune"), _os.path.join(project_dir, "python", "mistune"))
            copy(_os.path.join(python_dir, "transom"), _os.path.join(project_dir, "python", "transom"))

    def render_command(self):
        self.lib.render(force=self.args.force)

    def serve_command(self):
        self.lib.render(force=self.args.force)
        self.lib.serve(port=self.args.port)

    def check_links_command(self):
        errors = self.lib.check_links()

        if errors == 0:
            self.notice("PASSED")
        else:
            self.fail("FAILED")

    def check_files_command(self):
        missing_files, extra_files = self.lib.check_files()

        if extra_files != 0:
            self.warning("{} extra files in the output", extra_files)

        if missing_files == 0:
            self.notice("PASSED")
        else:
            self.fail("FAILED")

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def copy_file(from_path, to_path):
    try:
        _shutil.copyfile(from_path, to_path)
    except FileNotFoundError:
        _os.makedirs(_os.path.dirname(to_path), exist_ok=True)
        _shutil.copyfile(from_path, to_path)

def copy_dir(from_dir, to_dir):
    for name in _os.listdir(from_dir):
        if name == "__pycache__":
            continue

        from_path = _os.path.join(from_dir, name)
        to_path = _os.path.join(to_dir, name)

        copy_path(from_path, to_path)

def copy_path(from_path, to_path):
    if _os.path.isdir(from_path):
        copy_dir(from_path, to_path)
    else:
        copy_file(from_path, to_path)

def extract_metadata(text):
    if text.startswith("---\n"):
        end = text.index("---\n", 4)
        yaml = text[4:end]
        text = text[end + 4:]

        return text, _yaml.safe_load(yaml)

    return text, dict()

def load_site_template(path, default_text):
    if path is None or not _os.path.exists(path):
        return list(parse_template(default_text))

    return list(parse_template(read_file(path)))

def load_page_template(path, default_text):
    if path is None:
        return list(parse_template(default_text))

    return list(parse_template(read_file(path)))

def parse_template(text):
    for token in _variable_regex.split(text):
        if token.startswith("{{{") and token.endswith("}}}"):
            yield token[1:-1]
        elif token.startswith("{{") and token.endswith("}}"):
            yield compile(token[2:-2], "<string>", "eval")
        else:
            yield token

_heading_id_regex_1 = _re.compile(r"[^a-zA-Z0-9_ ]+")
_heading_id_regex_2 = _re.compile(r"[_ ]")

class HtmlRenderer(_mistune.renderers.html.HTMLRenderer):
    def heading(self, text, level, **attrs):
        id = _heading_id_regex_1.sub("", text)
        id = _heading_id_regex_2.sub("-", id)
        id = id.lower()

        return f"<h{level} id=\"{id}\">{text}</h{level}>\n"

class MarkdownLocal(_threading.local):
    def __init__(self):
        self.value = _mistune.create_markdown(renderer=HtmlRenderer(escape=False), plugins=["table"])
        self.value.block.list_rules += ['table', 'nptable']

_markdown_local = MarkdownLocal()

def convert_markdown(text):
    lines = (x for x in text.splitlines(keepends=True) if not x.startswith(";;"))
    return _markdown_local.value("".join(lines))

_lipsum_words = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "vestibulum", "enim", "urna",
    "ornare", "pellentesque", "felis", "eget", "maximus", "lacinia", "lorem", "nulla", "auctor", "massa", "vitae",
    "ultricies", "varius", "curabitur", "consectetur", "lacus", "sapien", "a", "lacinia", "urna", "tempus", "quis",
    "vestibulum", "vitae", "augue", "non", "augue", "lobortis", "semper", "nullam", "fringilla", "odio", "quis",
    "ligula", "consequat", "condimentum", "integer", "tempus", "sem",
]

def lipsum(count=50, end="."):
    return (" ".join((_lipsum_words[i % len(_lipsum_words)] for i in range(count))) + end).capitalize()

def plural(noun, count=0, plural=None):
    if noun in (None, ""):
        return ""

    if count == 1:
        return noun

    if plural is None:
        if noun.endswith("s"):
            plural = "{}ses".format(noun)
        else:
            plural = "{}s".format(noun)

    return plural

def html_table_csv(path, **attrs):
    with open(path, newline="") as f:
        return html_table(_csv.reader(f), **attrs)

def html_table_cell(column_index, value):
    return html_elem("td", str(value if value is not None else ""))

def html_table(data, headings=None, cell_fn=html_table_cell, **attrs):
    return html_elem("table", html_elem("tbody", html_table_rows(data, headings, cell_fn)), **attrs)

def html_table_rows(data, headings, cell_fn):
    if headings:
        yield html_elem("tr", (html_elem("th", x) for x in headings))

    for row in data:
        yield html_elem("tr", (cell_fn(i, x) for i, x in enumerate(row)))

def html_elem(tag, content, **attrs):
    if isinstance(content, _abc.Iterable) and not isinstance(content, str):
        content = "".join(content)

    return f"<{tag}{''.join(html_attrs(attrs))}>{content or ''}</{tag}>"

def html_attrs(attrs):
    for name, value in attrs.items():
        name = "class" if name in ("class_", "_class") else name
        value = name if value is True else value

        if value is not False:
            yield f" {name}=\"{_escape(value, quote=True)}\""

if __name__ == "__main__": # pragma: nocover
    command = TransomCommand()
    command.main()
