# Transom

[![main](https://github.com/ssorj/transom/workflows/main/badge.svg)](https://github.com/ssorj/transom/actions?query=workflow%3Amain)

Transom renders static websites from Markdown and Python

## Overview

Transom is a fairly run-of-the-mill static site generator written in
Python.  It converts Markdown input files into HTML output files.

But that does oversimplify things a bit.  Transom actually converts
Markdown input files and simple HTML files and Python code into
somewhat fancier HTML output files.  For me, I like that it automates
a lot of the work of creating a real website, *and* it does it with a
simple transformation model that leverages things I already know well:

* Markdown converts to HTML in a conventional way.

* Python code works like standard Python code, with some extra model
  data and functions for the pages I'm working with.

* Everything, including input HTML, is wrapped in site templates.

The full power of Python is available in the generation phase.  That
allows me to efficiently express and reuse display logic.

Transom is pleasantly quick on modern machines.  I use it to generate
the Apache Qpid website, which is large (about 2 gigs) and has many
files (more than 30,000).  Transom can render everything in less than
a second.

## Installation

Install the dependencies and then use `./plano install`:

~~~
pip install pyyaml
./plano install
~~~

## Using the transom command

To generate a starter website project, use `transom init`.  The
starter site is really basic.  It just lays down an index page
(`input/index.md`) a CSS file (`input/main.css`) and a JavaScript file
(`input/main.js`) plus the supporting Transom config files.

~~~ sh
$ cd <your-new-project-dir>

$ transom init
transom: Creating 'config/config.py'
transom: Creating 'config/head.html'
transom: Creating 'config/body.html'
transom: Creating 'input/index.md'
transom: Creating 'input/main.css'
transom: Creating 'input/main.js'
~~~

The `transom render` command uses the config and input files to
generate the rendered output.

~~~ sh
$ transom render
Rendering files from 'input' to 'output'
Found 3 input files
Rendered 3 output files
~~~

Now you have the HTML website under `<your-project-dir>/output`.  You
can send that whereever you need it to be for publishing purposes.
Since I often use GitHub pages for publishing, I set my output dir to
`docs` and then configure the GitHub project to serve those files.

For local development, you will likely want to use the `transom serve`
command.  This renders the site to the output dir and stands up a
local webserver so you can see what you have.  Transom watches for any
updates to the config or input files and re-renders the output as
needed.

~~~ sh
$ transom serve
Rendering files from 'input' to 'output'
Found 3 input files
Rendered 0 output files (3 unchanged)
Watching for input file changes
Serving at http://localhost:8080
Starting LiveReload v0.9.3 for /tmp/tmp.57gwncgHua/output on port 35729.
~~~

<!-- Site checks for files and links -->
<!-- ## Implementation notes -->
<!-- Multiprocessing -->
<!-- Mistune (having tried others before) -->
<!-- ## Template syntax (really Python code syntax) -->
<!-- ## Site config options and how to set them -->
<!-- ## Page and Site APIs -->
<!-- ## Page metadata -->
<!-- ## HTML generation functions -->
<!-- Conveniences -->
<!-- ## Using Plano project commands -->
<!-- ## Project commands -->
<!-- Once you have set up the project, you can use the `./plano` command in -->
<!-- the root of the project to perform project tasks.  It accepts a -->
<!-- subcommand.  Use `./plano --help` to list the available commands. -->

<!-- ## Site configuration -->

<!-- ## Page configuration -->

## Templates

Transom templates allow you to generate output by embedding Python
expressions inside `{{ }}` placeholders.  These expressions are
designed to execute Python code using Python's `eval` function.

You can call functions or access variables you've defined in
`config.py`.  You also have access to the Transom `site` and `page`
objects, which have APIs for site and page metadata.

You can use `{{{ }}}` to produce literal `{{ }}` output.

`config/config.py`:

~~~ python
def get_page_info(page):
    return page.url, page.title, page.parent, page.site
~~~

`input/index.md`:

~~~ html
<pre>{{get_page_info(page)}}</pre>
~~~

<!-- ## Site API -->

<!-- ## Page API -->

<!-- ## HTML generation functions -->

## Setting up Transom for a website repo

Change directory to the root of your project:

    cd <project-dir>/

Add the Transom code as a subdirectory:

    mkdir -p external
    curl -sfL https://github.com/ssorj/transom/archive/main.tar.gz | tar -C external -xz
    mv external/transom-main external/transom

Symlink the Transom and Plano libraries into your `python` directory:

    mkdir -p python
    ln -s ../external/transom/python/transom python/transom
    ln -s ../external/transom/python/mistune python/mistune
    ln -s ../external/transom/python/plano python/plano

Copy the `plano` command into the root of your project:

    cp external/transom/plano plano

Copy the standard config files:

    cp external/transom/profiles/website/.plano.py .plano.py
    cp external/transom/profiles/website/.gitignore .gitignore

Copy the standard workflow file:

    mkdir -p .github/workflows
    cp external/transom/profiles/website/.github/workflows/main.yaml .github/workflows/main.yaml
