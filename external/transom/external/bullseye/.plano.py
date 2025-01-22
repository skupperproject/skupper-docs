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

from plano import *

@command(passthrough=True)
def test_(passthrough_args=[]):
    clean()

    with working_env(PYTHONPATH=get_absolute_path("python")):
        run(["plano-test", "-m", "bullseye.tests"] + passthrough_args)

@command
def shellcheck():
    check_program("shellcheck", "Install shellcheck")

    with working_dir("test-project"):
        with temp_file() as do_env, temp_file() as undo_env:
            run("plano env", stdout=do_env)
            run("plano env --undo", stdout=undo_env)

            run(f"shellcheck --shell sh --enable all {do_env}")
            run(f"shellcheck --shell sh --enable all {undo_env}")

@command
def coverage():
    """
    Analyze test coverage
    """

    check_program("coverage", "Install the Python coverage package")

    clean()

    with working_env(PYTHONPATH=get_absolute_path("python")):
        run(f"coverage run --include python/* {which('plano-test')} -m bullseye.tests", stash=True)

    run("coverage report")
    run("coverage html")

    print("OUTPUT:", get_file_url("htmlcov/index.html"))

@command
def clean():
    remove(find(".", "__pycache__"))
    remove(".coverage")
    remove("htmlcov")
