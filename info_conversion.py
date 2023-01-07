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
import copy
# !/usr/bin/python

import logging

LOG = logging.getLogger('ryu.app.info_conversion')
LOG.setLevel(logging.INFO)


dc_Scope_Resource_Info = {  # all supported match fields. eg, curl -d "match="in_port=1,out_port=2,nw_src=::01""
        "dcId": None,
        "dcRouterNodeInfo": [{
            "ip6Addr": None,
            "inbound": None,
            "inboundUsage": None,
            "outbound": None,
            "outboundUsage": None,
            "interRegionLink": [{
                "srcAddr": None,
                "dstAddr": None
            }]
        }],
        "dcFuncList": [{
            "funcId": None,
            "funcParams": [{
                "cmdKey": None,
                "cmdVal": None
            }],
            "orientation": None,
            "Customization": [{
                "VideoQual": None,
                "Sublang": None,
                "AudioLang": None
            }]
        }],
        "dcMachineInfo": [{
            "machineAddr": None,
            "machineClockRate": None,
            "machineMemory": None,
            "machineMemoryUsage": None,
            "GPUExisttence": None
        }]
    }

    # all supported match fields. eg, curl -d "match="in_port=1,out_port=2,nw_src=::01""
regional_Scope_Resource_Info = {
        "regionId": None,
        "dcId": None,
        "interRegionLink": [{
            "srcAddr": None,
            "dstAddr": None,
            "linkType": None,
            "inbound": None,
            "inboundUsage": None,
            "outbound": None,
            "outboundUsage": None
        }],
        "regionalCPUClockRate": None,
        "regionalCPUUsage": None,
        "regionalGPUExistence": None,
        "regionalMemory": None,
        "regionalMemoryUsage": None,
        "dcFuncList": {
            "funcId": None,
            "funcParams": [{
                "cmdKey": None,
                "cmdVal": None
            }],
            "orientation": None,
            "customMapping": [{
                "videoQual": None,
                "subLang": None,
                "audioLang": None
            }]
        }
    }

global_Scope_Resource_Info = {
        # all supported match fields. eg, curl -d "match="in_port=1,out_port=2,nw_src=::01""
        "dcId": None,
        "dcRouterNodeInfo": None,
        "dcMachineInfo": None,
        "dcFunctionCustom": None
    }

usr_Req = {  # all supported match fields. eg, curl -d "match="in_port=1,out_port=2,nw_src=::01""
        "usrId": None,
        "ContentId": None,
        "AuthToken": None,
        "TokenLen": None,
        "Customization": [{
            "VideoQual": None,
            "Sublang": None,
            "AudioLang": None
        }]
    }

    # End-User’s ID: JP00000000000001
    # Content ID: 0001_000000000001
    # Authorization Token: testUname:testPswd
    # Token Length: 18
    # Customization:
    # Video Quality: Full HD / 24 fps/ MPEG4 encoding
    # 1_01_01
    # Language of subtitle: Japanese
    # 02
    # Language of audio track: English
    # 01

request_of_Global_Function_Deployment = {
        "validTime": None,
        "pathComputationResult": [{
            "taskName": None,
            "taskIdInteral": None,
            "regionId": None,
            "funcList": [{
                "funcId": None,
                "funcParams": None
            }]
        }]
    }

request_of_Regional_Function_Deployment = {
        "contentId": None,
        "validTime": None,
        "pathComputationResultList": [{
            "taskName": None,
            "taskIdInteral": None,
            "funcList": [{
                "funcId": None,
                "funcParams": None
            }]
        }]
    }

result_of_Global_Function_Offloading = {
        "globalStatusCode": None,
        "regionalFunctionDeploymentList": {
            "regionalStatusCode": None,
            "regionId": None,
            "dcList": [{
                "dcId": None,
                "routerNodeList": [{
                    "ingressSID": None,
                    "egressSID": None,
                    "statusCode": None
                }],
                "machineList": [{
                    "functionId": None,
                    "machineAddr": None,
                    "statusCode": None
                }]
            }]
        }
    }

result_of_Regional_Function_Offloading = {
        "regionalFunctionDeploymentList": {
            "regionalStatusCode": None,
            "regionId": None,
            "dcList": [{
                "dcId": None,
                "routerNodeList": [{
                    "ingressSID": None,
                    "egressSID": None,
                    "statusCode": None
                }],
                "machineList": [{
                    "functionId": None,
                    "machineAddr": None,
                    "statusCode": None
                }],
            }]
        }
    }

response_to_usr = {
        "responseCode": None,
        "responseContent": None,
        "url": None
    }

function_Info_Synchronization = {
        "dcFuncList": [{
            "funcId": None,
            "funcParams": [{
                "cmdKey": None,
                "cmdVal": None
            }],
            "orientation": None,
            "Customization": {
                "VideoQual": None,
                "SubLang": None,
                "AudioLang": None
            }
        }]
}

request_of_intra_Region_path_computation = {
        "validTime": None,
        "pathComputationResultList": {
            "taskIdInternal": None,
            "funcList": [{
                "funcId": None,
                "funcParams": [{
                    "cmdKey": None,
                    "cmdVal": None
                }]
            }]
        }
    }

result_of_intra_region_path_comput = {
        "validTime": None,
        "pathComputationResultList": {
            "taskName": None,
            "taskIdInternal": None,
            "taskIdRegional": None,
            "dcList": [{
                "dcId": None,
                "dcIngressIp6": None,
                "dcIngressSID": None,
                "dcEgressIp6": None,
                "dcEgressSID": None,
                "machineList": [{
                    "machineAddr": None,
                    "machineSID": None,
                    "funcId": None,
                    "funcParam": [{
                        "funcId": None,
                        "funcParams": [{
                            "cmdKey": None,
                            "cmdVal": None
                        }]
                    }]
                }]
            }]
        }
}

request_of_dc_function_deployment = {
        "validTime": None,
        "pathComputationResultList": {
            "taskIdRegional": None,
            "dcList": [{
                "dcId": None,
                "dcIngressIp6": None,
                "dcIngressSID": None,
                "dcEgressIp6": None,
                "dcEgressSID": None,
                "machineList": [{
                    "machineAddr": None,
                    "machineSID": None,
                    "funcId": None,
                    "funcParam": [{
                        "funcId": None,
                        "funcParams": [{
                            "cmdKey": None,
                            "cmdVal": None
                        }]
                    }]
                }]
            }]
        }
}

request_of_dc_scope_function_deployment = {
        "validTime": None,
        "taskIdRegional": None,
        "dcIngressIp6": None,
        "dcIngressSID": None,
        "dcEgressIp6": None,
        "dcEgressSID": None,
        "machineList": [{
            "machineAddr": None,
            "machineSID": None,
            "funcId": None,
            "funcParam": [{
                "funcId": None,
                "funcParams": [{
                    "cmdKey": None,
                    "cmdVal": None
                }]
            }]
        }]
    }

result_of_dc_scope_function_deployment = {
        "taskIdRegional": None,
        "dcId": None,
        "routerNodeList": [{
            "ingressSID": None,
            "egressSID": None,
            "statusCode": None
        }],
        "machineList": [{
            "funcId": None,
            "machineId": None,
            "statusCode": None
        }]
    }

result_of_regional_function_deployment = {
        "taskIdRegional": None,
        "dcList": [{
            "dcId": None,
            "routerNodeList": [{
                "ingressSID": None,
                "egressSID": None,
                "statusCode": None
            }],
            "machineList": [{
                "funcId": None,
                "machineId": None,
                "statusCode": None
            }]
        }]
    }

class info_conversion(object):


    # Valid time: 10000000
    # Path Computation Result List: {
    # Task name: “TEST”
    # Task id_Internal: 00000001
    # Region id: 0001
    # Function List: {
    # Function id: 00000001
    # Function parameters
    #       }
    # }

    # def get_match_fields(self):
    #     return self.match_fields

    def parse_match_fields(self, str_enc):
        LOG.debug("Match.parse_match_field, str=%s" % str_enc)
        str_dec = str_enc.decode()
        # str = str.strip('b\'')
        # str = str.strip('\'')
        LOG.debug("POST in str: " + str_dec)
        tokens = str_dec.split(',')
        # LOG.info("Tokens_pre:", tokens)
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
                # LOG.info("Tokens[count+1(%d)]:%s", count + 1, tokens[count + 1])
            count += 1

        # LOG.info("Tokens:", tokens)

    def formatDCFuncInfo(self, lines):
        dict = copy.copy(function_Info_Synchronization)
        for lineIdx in range(len(lines)):
            if lineIdx > 1:
                dict['dcFuncList'].append(dict['dcFuncList'][0])

            lineContents = lines[lineIdx].strip(",")
            dict['dcFuncList'][lineIdx]['funcId'] = lineContents[0]
            dict['dcFuncList'][lineIdx]['orientation'] = lineContents[1]
            dict['dcFuncList'][lineIdx]['Customization']['VideoQual'] = lineContents[2]
            dict['dcFuncList'][lineIdx]['Customization']['SubLang'] = lineContents[3]
            dict['dcFuncList'][lineIdx]['Customization']['AudioLang'] = lineContents[4]
            dict['dcFuncList'][lineIdx]['funcParams'][0]['cmdKey'] = "base"
            dict['dcFuncList'][lineIdx]['funcParams'][0]['cmdVal'] = lineContents[5]
            if len(lineContents) > 6:
                for idx in range(6, len(lineContents)):
                    dict['dcFuncList'][lineIdx]['funcParams'].append(dict['dcFuncList'][lineIdx]['funcParams'][0])
                    tmpLine = lineContents[idx].strip("=")
                    dict['dcFuncList'][lineIdx]['funcParams'][idx-5]['cmdKey'] = tmpLine[0]
                    print(len(tmpLine))
                    print("tmpLine:", tmpLine)
                    dict['dcFuncList'][lineIdx]['funcParams'][idx-5]['cmdVal'] = tmpLine[1].strip('"')
        return dict

    def DCScopeToIntra(self, str_enc):
        str_dec = str_enc.decode()
        tokens = str_dec.split(',')

    def __init__(self, **kwagrs):
        super(info_conversion, self).__init__()

