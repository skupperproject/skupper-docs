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

from bullseye import *
from plano.github import *

project.name = "transom"
project.data_dirs = ["profiles", "test-site"]
project.test_modules = ["transom.tests"]

@command(parent=build)
def build(*args, **kwargs):
    parent(*args, **kwargs)

    with project_env():
        run("transom --help", quiet=True, stash=True)

        with working_dir(quiet=True):
            touch("config/config.py", quiet=True)
            run("transom render --init-only", quiet=True)

@command(parent=clean)
def clean(*args, **kwargs):
    parent(*args, **kwargs)

    remove("test-site/output")
    remove("qpid-site/output")
    remove("htmlcov")
    remove(".coverage")

@command
def update_bullseye():
    """
    Update the embedded Bullseye repo
    """
    update_external_from_github("external/bullseye", "ssorj", "bullseye")

@command
def update_plano():
    """
    Update the embedded Plano repo
    """
    update_external_from_github("external/plano", "ssorj", "plano")

@command
def update_mistune():
    """
    Update the embedded Mistune repo
    """
    update_external_from_github("external/mistune", "lepture", "mistune", ref="v3.0.2")
