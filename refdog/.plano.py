from generate import *
from transom.planocommands import *

@command
def generate():
    """
    Generate input files from YAML config files
    """
    generate_objects()
    generate_index()

@command
def test():
    generate()
    render()
    check_links()

@command
def generate_diagrams():
    """
    Generate SVG diagrams from D2 files
    """
    for input_file in find("input/concepts/images", "*.d2"):
        output_file = input_file.removesuffix(".d2") + ".svg"

        with temp_file() as tmp:
            run(f"d2 --layout elk --theme 105 --pad 0 {input_file} {tmp}")
            move(tmp, output_file)

@command
def update_crds():
    """
    Update the CRD source files from main
    """
    url = "https://github.com/skupperproject/skupper/archive/refs/heads/main.tar.gz"
    crd_dir = get_absolute_path("crds")

    with temp_file() as temp:
        http_get(url, output_file=temp)

        with working_dir(quiet=True):
            extract_archive(temp)

            extracted_dir = list_dir()[0]
            assert is_dir(extracted_dir)

            with working_dir(extracted_dir):
                copy("config/crd/bases/", crd_dir, inside=False)


@command
def update_cli():
    """
    Update the CLI files using ../skupper/generate-doc
    """
    run("../skupper/generate-doc ./cli-doc")
