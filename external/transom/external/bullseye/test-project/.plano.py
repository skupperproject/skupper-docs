import sys

sys.path.insert(0, "../python")

from bullseye import *

project.name = "chucker"
project.source_exclude = ["bumper.*"]
project.data_dirs = ["files"]
project.test_modules = ["chucker.tests"]

result_file = "build/result.json"

@command(parent=build)
def build(*args, **kwargs):
    parent(*args, **kwargs)

    notice("Extended building")

    data = {"built": True}
    write_json(result_file, data)

# XXX Consider instead inheriting the passthrough behavior from the parent
@command(parent=test_, passthrough=True)
def test_(*args, passthrough_args=[], **kwargs):
    parent(*args, passthrough_args=passthrough_args, **kwargs)

    notice("Extended testing")

    check_file(result_file)

    if exists(result_file):
        data = read_json(result_file)
        data["tested"] = True
        write_json(result_file, data)

@command(parent=install)
def install(*args, **kwargs):
    parent(*args, **kwargs)

    notice("Extended installing")

    data = read_json(result_file)
    data["installed"] = True
    write_json(result_file, data)
