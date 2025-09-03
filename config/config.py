from plano import *
import os

site.output_dir = "output"
site_prefix = os.environ.get("SITE_PREFIX", "")

def path_nav(page):
    files = reversed(list(page.ancestors)[:-1])
    links = [f"<a href=\"{site_prefix}{x.url}\">{x.title}</a>" for x in files]
    links = " <span class=\"path-separator\">&#8250;</span> ".join(links)

    return f"<nav id=\"-path-nav\"><div>{links}</div></nav>"

skupper_cli_version = '2.1.1'
