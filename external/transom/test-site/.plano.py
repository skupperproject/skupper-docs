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

from transom.planocommands import *

result_file = "output/result.json"

@command(parent=render)
def render(*args, **kwargs):
    render.parent.function(*args, **kwargs)

    data = {"rendered": True}
    write_json(result_file, data)

@command(parent=serve)
def serve(*args, **kwargs):
    serve.parent.function(*args, **kwargs)

    data = {"served": True}
    write_json(result_file, data)

@command(parent=check_links)
def check_links(*args, **kwargs):
    check_links.parent.function(*args, **kwargs)

    data = {"links_checked": True}
    write_json(result_file, data)

@command(parent=check_files)
def check_files(*args, **kwargs):
    check_files.parent.function(*args, **kwargs)

    data = {"files_checked": True}
    write_json(result_file, data)
