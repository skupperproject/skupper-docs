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

from .main import *

test_project_dir = get_absolute_path("test-project")
result_file = "build/result.json"

class test_project(working_dir):
    def __enter__(self):
        dir = super(test_project, self).__enter__()
        copy(test_project_dir, ".", inside=False)
        return dir

def run_plano(*args):
    PlanoCommand().main(["-f", join(test_project_dir, ".plano.py")] + list(args))

@test
def project_operations():
    project.name = "alphabet"

    with project_env():
        assert "ALPHABET_HOME" in ENV, ENV

    with working_dir():
        input_file = write("zeta-file", "X@replace-me@X")
        output_file = configure_file(input_file, "zeta-file", {"replace-me": "Y"})
        output = read(output_file)
        assert output == "XYX", output

@test
def build_command():
    if WINDOWS: # pragma: nocover
        raise PlanoTestSkipped("Not ready for Windows")

    with test_project():
        run_plano("build")

        result = read_json(result_file)
        assert result["built"], result

        check_file("build/bin/chucker")
        check_file("build/chucker/python/chucker/__init__.py")
        check_file("build/chucker/python/chucker/main.py")
        check_file("build/chucker/python/chucker/tests.py")
        check_file("build/chucker/python/flipper.py")

        assert not exists("build/chucker/python/bumper.py")

        result = read("build/bin/chucker").strip()
        assert result.endswith(join(".local", "lib", "chucker")), result

        result = read_json("build/build.json")
        assert result["prefix"].endswith(".local"), result

        run_plano("build", "--prefix", "/usr/local")

        result = read("build/bin/chucker").strip()
        assert result == "/usr/local/lib/chucker", result

        result = read_json("build/build.json")
        assert result["prefix"] == ("/usr/local"), result

@test
def test_command():
    with test_project():
        run_plano("test")

        check_file(result_file)

        result = read_json(result_file)
        assert result["tested"], result

        run_plano("test", "--verbose")
        run_plano("test", "--list")
        run_plano("test", "test-hello")

@test
def coverage_command():
    with test_project():
        run_plano("coverage")

        check_file(result_file)

        result = read_json(result_file)
        assert result["tested"], result

@test
def install_command():
    if WINDOWS: # pragma: nocover
        raise PlanoTestSkipped("Not ready for Windows")

    with test_project():
        run_plano("install", "--staging-dir", "staging")

        result = read_json(result_file)
        assert result["installed"], result

        check_dir("staging")

    with test_project():
        assert not exists("build"), list_dir()

        run_plano("build", "--prefix", "/opt/local")
        run_plano("install", "--staging-dir", "staging")

        check_dir("staging/opt/local")

@test
def clean_command():
    with test_project():
        run_plano("build")

        check_dir("build")

        run_plano("clean")

        assert not is_dir("build")

@test
def env_command():
    with test_project():
        run_plano("env")
        run_plano("env", "--undo")
