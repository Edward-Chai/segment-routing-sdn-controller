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
import os
import uuid

LOG = logging.getLogger('ryu.app.info_conversion')
LOG.setLevel(logging.INFO)
contentProviderId = ""

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
        "interRegionLink": [{
            "linkId": None,
            "inbound": 1024,
            "inboundUsage": float(0),
            "outbound": 1024,
            "outboundUsage": float(0)
        }],
        "regionalCPUClockRate": 0,
        "regionalCPUUsage": float(0),
        "regionalGPUExistence": 0,
        "regionalMemory": 0,
        "regionalMemoryUsage": 0,
        "dcFuncList": []
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
        "taskName": None,
        "regionId": None,
        "funcList": []
    }

request_of_Regional_Function_Deployment = {
        "cdId": None,
        "taskName": None,
        "validTime": None,
        "funcList": []
    }

result_of_Global_Function_deployment = {
        "globalStatusCode": None,
        "regionalFunctionDeploymentList": []
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

result_of_inter_Region_path_computation = {
        "regionId": None,
        "funcList": [{
            "funcId": None,
            "funcParams": None
        }]
    }

request_of_intra_Region_path_computation = {
        "validTime": None,
        "funcList": []
    }

result_of_intra_region_path_comput = {
        "validTime": None,
        "dcList": [{
            "dcId": None,
            "dcIngressIp6": None,
            "dcIngressSID": None,
            "dcEgressIp6": None,
            "dcEgressSID": None,
            "machineList": [{
                "taskIdInternal": None,
                "taskIdRegional": None,
                "machineAddr": None,
                "machineSID": None,
                "funcId": None,
                "funcParams": [{
                    "cmdKey": None,
                    "cmdVal": None
                }]
            }]
        }]

}

request_of_regional_function_offloading = {
        "validTime": None,
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
        "regionId": None,
        "regionStatusCode": None,
        "dcList": [{
            "dcId": None,
            "routerNodeList": [{
                "ingressSID": None,
                "egressSID": None,
                "statusCode": None
            }],
            "machineList": [{
                "taskIdRegional": None,
                "funcId": None,
                "machineId": None,
                "statusCode": None
            }]
        }]
    }

request_of_inter_region_path_comput = {
    "contentId": "",
    "Customization": {
        "VideoQual": "",
        "SubLang": "",
        "AudioLang": ""
    },
    "locality": ""
}

dcIdList = []

cpId_taskId_mapping = [{
    "cdId": None,
    "taskIdInternal": [],
    "taskIdRegional": []
}]

class info_conversion(object):
    def __init__(self, **kwagrs):
        super(info_conversion, self).__init__()

        os.chdir("/home/edward/funcInfo/")
        global contentProviderId
        global cpId_taskId_mapping
        if os.path.exists("cdId"):
            f = open("cdId", "r")
            region_id = f.readline()
            f.close()
        else:
            f = open("cdId", "w")
            region_id = str(uuid.uuid4())
            f.write(region_id)
            f.close()


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
                dict['dcFuncList'].append(copy.deepcopy(dict['dcFuncList'][0]))

            lineContents = lines[lineIdx].split(',')
            print("lines[lineIdx]: ", lines[lineIdx])
            print("lineContents: ", lineContents)
            dict['dcFuncList'][lineIdx]['funcId'] = lineContents[0]
            dict['dcFuncList'][lineIdx]['orientation'] = lineContents[1]
            dict['dcFuncList'][lineIdx]['Customization']['VideoQual'] = lineContents[2]
            dict['dcFuncList'][lineIdx]['Customization']['SubLang'] = lineContents[3]
            dict['dcFuncList'][lineIdx]['Customization']['AudioLang'] = lineContents[4]
            dict['dcFuncList'][lineIdx]['funcParams'][0]['cmdKey'] = "base"
            dict['dcFuncList'][lineIdx]['funcParams'][0]['cmdVal'] = lineContents[5]
            if len(lineContents) > 6:
                for idx in range(6, len(lineContents)):
                    dict['dcFuncList'][lineIdx]['funcParams'].append(copy.deepcopy(dict['dcFuncList'][lineIdx]['funcParams'][0]))
                    tmpLine = lineContents[idx].split("=")
                    dict['dcFuncList'][lineIdx]['funcParams'][idx-5]['cmdKey'] = tmpLine[0]
                    print(len(tmpLine))
                    print("lineContents[idx]:", lineContents[idx])
                    dict['dcFuncList'][lineIdx]['funcParams'][idx-5]['cmdVal'] = tmpLine[1].strip('"\n')
        return dict

    def DCScopeToIntra(self, jsonMsg, region_id):
        regional_Scope_Resource_Info['regionId'] = region_id
        if jsonMsg['dcid'] not in dcIdList:
            dcIdList.append(jsonMsg['dcid'])
            for dcMachineIdx in range(len(jsonMsg['dc_machine_info'])):
                # if dcMachineIdx > 0:
                regional_Scope_Resource_Info['regionalGPUExistence'] = int(jsonMsg['dc_machine_info'][dcMachineIdx]['gpu_existence'])
                regional_Scope_Resource_Info["regionalCPUUsage"] = (regional_Scope_Resource_Info['regionalCPUClockRate'] * regional_Scope_Resource_Info["regionalCPUUsage"] + int(jsonMsg['dc_machine_info'][dcMachineIdx]['cpu_clock_rate']) * float(jsonMsg['dc_machine_info'][dcMachineIdx]['cpu_usage'])) / (int(jsonMsg['dc_machine_info'][dcMachineIdx]['cpu_clock_rate']) + regional_Scope_Resource_Info['regionalCPUClockRate'])
                regional_Scope_Resource_Info['regionalCPUClockRate'] += int(jsonMsg['dc_machine_info'][dcMachineIdx]['cpu_clock_rate'])
                regional_Scope_Resource_Info["regionalMemoryUsage"] = regional_Scope_Resource_Info["regionalMemoryUsage"] + int(jsonMsg['dc_machine_info'][dcMachineIdx]['free_ram'])
                regional_Scope_Resource_Info['regionalMemory'] += int(jsonMsg['dc_machine_info'][dcMachineIdx]['total_ram'])
            for Idx in range(len(jsonMsg['dcFuncList'])):
                # regional_Scope_Resource_Info['dcFuncList'] = []
                regional_Scope_Resource_Info['dcFuncList'].append(jsonMsg['dcFuncList'][Idx])
                regional_Scope_Resource_Info['dcFuncList'][-1].update({"dcId": jsonMsg['dcid']})
        return regional_Scope_Resource_Info

    def usr_req_to_req_of_inter_region_path_comput(self, jsonMsg):
        request_of_inter_region_path_comput["contentId"] = jsonMsg["contentId"]
        request_of_inter_region_path_comput["Customization"] = jsonMsg["Customization"]
        request_of_inter_region_path_comput["locality"] = "0001"
        return request_of_inter_region_path_comput

    def result_of_inter_region_path_comput(self, jsonMsg):
        resultOfInterPathComput = copy.deepcopy(result_of_inter_Region_path_computation)
        resultOfInterPathComput["regionId"] = jsonMsg[0]["regionId"]
        resultOfInterPathComput["funcList"][0]["funcId"] = jsonMsg[0]["dcFuncList"][0]["funcId"]
        resultOfInterPathComput["funcList"][0]["funcParams"] = jsonMsg[0]["dcFuncList"][0]["funcParams"]
        return resultOfInterPathComput

    def request_of_global_func_deploy(self, jsonMsg):
        requestOfGlobalFunctionDeployment = copy.deepcopy(request_of_Global_Function_Deployment)
        requestOfGlobalFunctionDeployment["validTime"] = "100000000"
        requestOfGlobalFunctionDeployment["taskName"] = "TEST"
        requestOfGlobalFunctionDeployment["regionId"] = jsonMsg["regionId"]
        requestOfGlobalFunctionDeployment["funcList"] = jsonMsg["funcList"]
        requestOfGlobalFunctionDeployment["funcList"][0].update({"taskIdInternal": "00000001"})
        return requestOfGlobalFunctionDeployment

    def global_func_deploy_to_regional_func_deploy(self, jsonMsg):
        regionalFuncDeploy = copy.deepcopy(request_of_Regional_Function_Deployment)
        regionalFuncDeploy["validTime"] = jsonMsg["validTime"]
        regionalFuncDeploy["cdId"] = contentProviderId
        regionalFuncDeploy["funcList"] = jsonMsg["funcList"]
        regionalFuncDeploy["taskName"] = jsonMsg["taskName"]
        # regionalFuncDeploy["taskIdInternal"] = jsonMsg["taskIdInternal"]
        return regionalFuncDeploy

    def req_of_intra_region_path_comput(self, jsonMsg):
        reqIntraRegionPathComput = copy.deepcopy(request_of_intra_Region_path_computation)
        reqIntraRegionPathComput["validTime"] = jsonMsg["validTime"]
        # cdId_exist = 0
        # cdId_Idx = 0
        # for idx in range(len(cpId_taskId_mapping)):
        #     if cpId_taskId_mapping[idx]["cdId"] == jsonMsg["cdId"]:
        #         cdId_exist = 1
        #         cdId_Idx = idx
        #
        # if cdId_exist == 0 and len(cpId_taskId_mapping) >= 1:
        #     mappingList = copy.deepcopy(cpId_taskId_mapping[0])
        #     mappingList["cdId"] = jsonMsg["cdId"]
        #     for item in jsonMsg["funcList"]:
        #         mappingList["taskIdInternal"].append(item["taskIdInternal"])
        #     cpId_taskId_mapping.append(mappingList)
        # elif cdId_exist == 0 and (cpId_taskId_mapping[0]["cdId"] is None):
        #     cpId_taskId_mapping[0]["cdId"] = jsonMsg["cdId"]
        #     for item in jsonMsg["funcList"]:
        #         cpId_taskId_mapping[0]["taskIdInternal"].append(item["taskIdInternal"])
        # elif cdId_exist == 1:
        #     for item in jsonMsg["funcList"]:
        #         cpId_taskId_mapping[cdId_Idx]["taskIdInternal"].append(item["taskIdInternal"])
        reqIntraRegionPathComput["funcList"] = jsonMsg["funcList"]
        return reqIntraRegionPathComput


    def req_of_regional_func_offloading(self, jsonMsg):
        reqRegionalFuncOffloading = copy.deepcopy(request_of_regional_function_offloading)
        reqRegionalFuncOffloading["validTime"] = jsonMsg["validTime"]
        internal = []
        regional = []
        for item in jsonMsg["dcList"]:
            for ml in item["machineList"]:
                internal.append(ml["taskIdInternal"])
                regional.append(ml["taskIdRegional"])
                ml.pop("taskIdInternal")

        for idx in range(len(cpId_taskId_mapping)):
            if internal[0] in cpId_taskId_mapping[idx]["taskIdInternal"]:
                cpId_taskId_mapping[idx]["taskIdRegional"].extend(regional)
        reqRegionalFuncOffloading["dcList"] = jsonMsg["dcList"]
        return reqRegionalFuncOffloading

    def req_of_dc_scope_func_deploy(self, jsonMsg):
        dcScopeFuncDeploy = copy.deepcopy(request_of_dc_scope_function_deployment)
        dcScopeFuncDeploy["validTime"] = jsonMsg["validTime"]
        dcScopeFuncDeploy["dcIngressIp6"] = jsonMsg["dcList"][0]["dcIngressIp6"]
        dcScopeFuncDeploy["dcIngressSID"] = jsonMsg["dcList"][0]["dcIngressSID"]
        dcScopeFuncDeploy["dcEgressIp6"] = jsonMsg["dcList"][0]["dcEgressIp6"]
        dcScopeFuncDeploy["dcEgressSID"]= jsonMsg["dcList"][0]["dcEgressSID"]
        dcScopeFuncDeploy["machineList"] = jsonMsg["dcList"][0]["machineList"]
        return dcScopeFuncDeploy

    def result_of_regional_func_deployment(self, jsonMsg, regionId):
        global result_of_regional_function_deployment
        result_of_regional_function_deployment["regionId"] = regionId
        regional = []
        regional_info = []
        dc_exist = 0
        dc_idx = 0
        isAll = 0
        for idx in range(len(result_of_regional_function_deployment["dcList"])):
            if jsonMsg["dcId"] == result_of_regional_function_deployment["dcList"][idx]["dcId"]:
                dc_exist = 1
                dc_idx = idx
                break


        if dc_exist:
            result_of_regional_function_deployment["dcList"][dc_idx]["routerNodeList"] = jsonMsg["routerNodeList"]
            result_of_regional_function_deployment["dcList"][dc_idx]["machineList"] = jsonMsg["machineList"]
        elif (len(result_of_regional_function_deployment["dcList"]) == 1) and (result_of_regional_function_deployment["dcList"][0]["dcId"] is None):
            result_of_regional_function_deployment["dcList"][0]["routerNodeList"] = jsonMsg["routerNodeList"]
            result_of_regional_function_deployment["dcList"][0]["machineList"] = jsonMsg["machineList"]
            result_of_regional_function_deployment["dcList"][0]["dcId"] = jsonMsg["dcId"]
        else:
            item = copy.deepcopy(result_of_regional_function_deployment["dcList"][0])
            item["dcId"] = jsonMsg["dcId"]
            item["machineList"] = jsonMsg["machineList"]
            item["routerNodeList"] = jsonMsg["routerNodeList"]
            result_of_regional_function_deployment["dcList"].append(item)

        for item in cpId_taskId_mapping:
            if result_of_regional_function_deployment["dcList"][0]["machineList"][0]["taskIdRegional"] in item["taskIdRegional"]:
                regional = item["taskIdRegional"]

        for item in result_of_regional_function_deployment["dcList"]:
            for machine in item["machineList"]:
                regional_info.append(machine["taskIdRegional"])

        regional.sort()
        regional_info.sort()
        if regional_info == regional:
            isAll = 1
        else:
            isAll = 0

        if isAll:
            regionalStatus = 1
            for item in result_of_regional_function_deployment["dcList"]:
                for router in item["routerNodeList"]:
                    if router["statusCode"] == "0000":
                        regionalStatus = 0
                        break
                if regionalStatus == 0:
                    break
                for machine in item["machineList"]:
                    if machine["statusCode"] == "0000":
                        regionalStatus = 0
                        break
            if regionalStatus == 1:
                result_of_regional_function_deployment["regionStatusCode"] = "0001"

        return result_of_regional_function_deployment, isAll

    def result_of_intra_region_path_comput(self, jsonMsg, jsonMsg1):
        intraRegionPathComput = copy.deepcopy(result_of_intra_region_path_comput)
        intraRegionPathComput["validTime"] = "10000000"
        intraRegionPathComput["dcList"][0]["dcId"] = jsonMsg[0]["dcid"]
        intraRegionPathComput["dcList"][0]["dcIngressIp6"] = jsonMsg[0]["dc_router_node_info"][0]["ip6addr"]
        intraRegionPathComput["dcList"][0]["dcEgressIp6"] = jsonMsg[0]["dc_router_node_info"][0]["ip6addr"]
        intraRegionPathComput["dcList"][0]["dcIngressSID"] = ""
        ipv6addrs = intraRegionPathComput["dcList"][0]["dcIngressIp6"].split(":")
        for idx in range(len(ipv6addrs)):
            intraRegionPathComput["dcList"][0]["dcIngressSID"] += ipv6addrs[idx]
            if idx+2 != len(ipv6addrs):
                intraRegionPathComput["dcList"][0]["dcIngressSID"] += ":"
        intraRegionPathComput["dcList"][0]["dcEgressSID"] = intraRegionPathComput["dcList"][0]["dcIngressSID"]
        intraRegionPathComput["dcList"][0]["machineList"][0]["taskIdInternal"] = jsonMsg1["funcList"][0]["taskIdInternal"]
        intraRegionPathComput["dcList"][0]["machineList"][0]["taskIdRegional"] = "00000001"
        intraRegionPathComput["dcList"][0]["machineList"][0]["machineAddr"] = jsonMsg[0]["dc_machine_info"][0]["ip6addr"]
        intraRegionPathComput["dcList"][0]["machineList"][0]["machineSID"] = ""
        intraRegionPathComput["dcList"][0]["machineList"][0]["funcId"] = jsonMsg1["funcList"][0]["funcId"]
        intraRegionPathComput["dcList"][0]["machineList"][0]["funcParams"] = jsonMsg1["funcList"][0]["funcParams"]
        return intraRegionPathComput



    def resultof_global_func_deploy(self, jsonMsg):
        global result_of_Global_Function_deployment
        globalStatus = 1
        # resultRegionalFuncDeploy = result_of_Global_Function_deployment
        result_of_Global_Function_deployment["regionalFunctionDeploymentList"].append(jsonMsg)
        for item in result_of_Global_Function_deployment["regionalFunctionDeploymentList"]:
            if item["regionStatusCode"] == "0000":
                globalStatus = 0
                break
        if globalStatus == 1:
            result_of_Global_Function_deployment["globalStatusCode"] = "0001"

        return result_of_Global_Function_deployment
    "转换taskid，两个mano，来自各个region是否齐全"