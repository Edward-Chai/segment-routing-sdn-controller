# Copyright (C) 2017 Binh Nguyen binh@cs.utah.edu.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# !/usr/bin/python

import logging

LOG = logging.getLogger('ryu.app.Actions')
LOG.setLevel(logging.INFO)


class Actions(object):
    actions_fields = {
        # all supported actions fields. eg, curl -d "actions="ipv6_dst=::01,mod_dl_src="AA:BB:CC:DD:EE:FF""
        "ipv6_dst": [],
        "mod_dl_dst": None,
        "output": None
    }

    def get_actions_fields(self):
        return actions_fields

    def parse_actions_fields(self, str):
        LOG.debug("parse_actions_fields, str=%s" % str)

        tokens = str.split(',')
        for t in tokens:
            try:
                key = t.split("=")[0]
                value = t.split("=")[1]
            except:
                LOG.error("Invalid actions: %s" % t)
                return None

            if key in self.actions_fields:
                if key == "ipv6_dst":
                    self.actions_fields[key].append(value)
                else:
                    self.actions_fields[key] = value
            else:
                LOG.warn("Key isn't supported: %s" % key)

        return self.actions_fields

    def __init__(self, *args, **kwagrs):
        super(Actions, self).__init__(*args, **kwagrs)
        self.actions_fields['ipv6_dst'] = []
        for key in kwagrs:
            if key == "ipv6_dst":
                self.actions_fields[key].append(kwagrs[key])
            else:
                self.actions_fields[key] = kwagrs[key]

    def print_me(self):
        LOG.info("Actions_fields -> value")
        for key in self.actions_fields:
            LOG.info("%s -> %s" % (key, self.actions_fields[key]))
