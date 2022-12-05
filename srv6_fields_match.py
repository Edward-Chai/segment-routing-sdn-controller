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

LOG = logging.getLogger('ryu.app.srv6_field_match')
LOG.setLevel(logging.INFO)


class SRv6_field_match(object):
    match_fields = {  # all supported match fields. eg, curl -d "match="in_port=1,out_port=2,nw_src=::01""
        "host_ip": None,
        "seg": None,
        "action": None,
        "params": None,
        "segs": None,
    }

    def get_match_fields(self):
        return self.match_fields

    def parse_match_fields(self, str_enc):
        LOG.debug("Match.parse_match_field, str=%s" % str_enc)
        str_dec = str_enc.decode()
        # str = str.strip('b\'')
        # str = str.strip('\'')
        LOG.debug("POST in str: " + str_dec)
        tokens = str_dec.split(',')
        LOG.info("Tokens_pre:", tokens)
        count = 0
        while count < len(tokens):
            print("count: %d", count)
            if tokens[count].find("=") == -1:
                LOG.info("Tokens[count(%d)]:%s", count, tokens[count])
                tokens[count - 1] += "," + tokens[count]
                LOG.info("Tokens[count-1(%d)]:%s", count - 1, tokens[count - 1])
                tokens.pop(count)
                print("Tokens: ", tokens)
                count -= 1
                LOG.info("Tokens[count+1(%d)]:%s", count + 1, tokens[count + 1])
            count += 1


        # LOG.info("Tokens:", tokens)

        for t in tokens:
            try:
                key = t.split("=")[0]
                value = t.split("=")[1]
            except:
                LOG.error("Invalid match field: %s" % t)
                return None

            if key in self.match_fields:
                self.match_fields[key] = value
            else:
                LOG.error("Key isn't supported: %s" % key)
        return self.match_fields

    def __init__(self, **kwagrs):
        super(SRv6_field_match, self).__init__()
        for key in self.match_fields:
            self.match_fields[key] = None
        for key in kwagrs:
            self.match_fields[key] = kwagrs[key]

    def print_me(self):
        LOG.info("Match_fields -> value")
        for key in self.match_fields:
            LOG.info("%s -> %s" % (key, self.match_fields[key]))
