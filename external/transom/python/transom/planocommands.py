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
from plano.github import *
from transom import TransomCommand

@command(passthrough=True)
def render(passthrough_args=[]):
    """
    Render site output
    """
    with project_env():
        TransomCommand().main(["render"] + passthrough_args)

# https://stackoverflow.com/questions/22475849/node-js-what-is-enospc-error-and-how-to-solve
# $ echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
@command(passthrough=True)
def serve(passthrough_args=[]):
    """
    Serve the site and rerender when input files change
    """
    with project_env():
        TransomCommand().main(["serve"] + passthrough_args)

@command(passthrough=True)
def check_links(passthrough_args=[]):
    """
    Check for broken links
    """
    render()

    with project_env():
        TransomCommand().main(["check-links"] + passthrough_args)

@command(passthrough=True)
def check_files(passthrough_args=[]):
    """
    Check for missing or extra files
    """
    render()

    with project_env():
        TransomCommand().main(["check-files"] + passthrough_args)

@command
def clean():
    remove(find(".", "__pycache__"))

@command
def update_transom():
    """
    Update the embedded Transom repo
    """
    update_external_from_github("external/transom", "ssorj", "transom")

class project_env(working_env):
    def __init__(self):
        super(project_env, self).__init__(PYTHONPATH="python")
