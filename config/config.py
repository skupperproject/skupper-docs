from plano import *

site.output_dir = "output"

def path_nav(page):
    files = reversed(list(page.ancestors)[:-1])
    links = [f"<a href=\"{x.url}\">{x.title}</a>" for x in files]
    links = " <span class=\"path-separator\">&#8250;</span> ".join(links)

    return f"<nav id=\"-path-nav\"><div>{links}</div></nav>"

skupper_cli_version = '2.0.0-rc1'
