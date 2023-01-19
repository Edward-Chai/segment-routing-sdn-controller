# Copyright (C) 2017 Binh Nguyen binh@cs.utah.edu.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import uuid
import requests
# !/usr/bin/python

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.controller import dpset
from ryu.app.wsgi import ControllerBase, WSGIApplication
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from collections import defaultdict
from ofctl_rest_listener import SR_rest_api
from sr_flows_mgmt import SR_flows_mgmt
from parameters import *
from TE.te_controller import *
import logging
import paramiko
from srv6_fields_match import SRv6_field_match
from info_conversion import info_conversion
from iproute2_utils import iproute2_utils
import os

LOG = logging.getLogger('ryu.app.rest_api_test')
LOG.setLevel(logging.INFO)

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST',
    'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, X-Requested-With'}

regionId_addr_mapping = []
CDinterURL = ""
IntraMANOURL = ""
IntraFuncURL_Inter = ""

InterFuncURL = ""

IntraFuncURL_DC = ""

class FUNC_MGR_Controller(ControllerBase):

    def __init__(self, req, link, data, **config):
        super(FUNC_MGR_Controller, self).__init__(req, link, data, **config)
        global regionId_addr_mapping


    def req_of_regional_func_deploy(self, req):
        infoConversion = info_conversion()
        # funcHandlingUtil = funcHandling()
        req_body = req.body
        msg_dec = req_body.decode()
        jsonMsg = json.loads(msg_dec)

    def dc_scope_to_intra(self, req, **kwargs):
        req_body = req.body

        # LOG.info("req_body: ", req_body)
        msg_dec = req_body.decode()
        # LOG.info("msg_dec: ", msg_dec)
        jsonMsg = json.loads(msg_dec)
        print(jsonMsg, "\n")
        # funcHandlingUtil = funcHandling()
        # req_body_dec = req_body.decode('utf-8')
        # SRv6_match = SRv6_field_match()
        # iproute2u = iproute2_utils()
        # match_fields = SRv6_match.parse_match_fields(req_body)
        # LOG.info("--------------- Match Fields Start ---------------")
        # for key in match_fields:
        #     LOG.info("%s:   %s", key, match_fields[key])
        # LOG.info("--------------- Match Fields End -----------------")
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname='131.113.71.192', port=22, username='root', password='Zhaizehua960929')
        # stdin, stdout, stderr = ssh.exec_command('ps -ef | grep test')
        # print(stdout.read().decode())
        # ssh.close()
        # iproute2u.insert_srv6_rule_local(match_fields)

        # print("req_body:", req_body)
        return Response(content_type='application/json', status=200, body=json.dumps("TEST OK!"),
                        charset='utf8', headers=HEADERS)

    def request_of_regional_func_deploy(self, req):
        req_body = req.body
        msg_dec = req_body.decode()
        jsonMsg = json.loads(msg_dec)
        infoConversion = info_conversion()
        reqHandler = reqHandling()
        reqRegionalFuncDeploy = infoConversion.global_func_deploy_to_regional_func_deploy(jsonMsg)
        print("requestOfGlobalFuncDeploy: ", reqRegionalFuncDeploy, "\n")
        # InterRegionFuncMgrURL = ""
        # r = reqHandler.sendPost(InterRegionFuncMgrURL, reqRegionalFuncDeploy)


class reqHandling(object):

    def __init__(self):
        super(reqHandling, self).__init__()

    def sendPost(self, url, postMsg):
        s = json.dumps(postMsg)
        # keep = True
        # while keep:
        r = ""
        try:
            r = requests.post(url, data=s, timeout=5)
            keep = False
        except Exception as e:
            print(datetime.datetime.now(), " Request failed!")
        # r = requests.post(url, data=s, timeout=5)
        return r

    def sendGet(self, url):
        # keep = True
        # while keep:
        r = ""
        try:
            r = requests.get(url, timeout=5)
            keep = False
        except Exception as e:
            print(datetime.datetime.now(), " Request failed!")
        # r = requests.post(url, data=s, timeout=5)
        return r




class funcMgr(app_manager.RyuApp):
    _CONTEXTS = {
        'wsgi': WSGIApplication,
    }

    def __init__(self, *args, **kwargs):
        super(funcMgr, self).__init__(*args, **kwargs)
        wsgi = kwargs['wsgi']

        # os.chdir("/home/edward/funcInfo/")
        # f = open("funcInfoList", "r")
        # region_id = ""
        # infoConversion = info_conversion()
        # funcInfo = f.readlines()
        # f.close()
        # f = open("monitorURL", "r")
        # monitorURL = f.readline()
        # monitorURL = monitorURL.strip()
        # dcFuncInfoDict = infoConversion.formatDCFuncInfo(funcInfo)
        # funcHandlingUtil = funcHandling()
        # jsonMsg = json.dumps(dcFuncInfoDict)
        # f.close()
        # f = open("dcFuncList", "w")
        # f.write(jsonMsg)
        # f.close()
        if os.path.exists("region_id"):
            f = open("region_id", "r")
            region_id = f.readline()
            f.close()
        else:
            f = open("region_id", "w")
            region_id = str(uuid.uuid4())
            f.write(region_id)
            f.close()

        funcMgrConfig = ""
        if os.path.exists("config_funcmgr"):
            f = open("config_funcmgr", "r")
            funcMgrConfig = f.readlines()
            f.close()
        else:
            print("Cannot open config file for Request Manager !\n")
            exit()

        global CDinterURL, IntraMANOURL, IntraFuncURL_Inter, InterFuncURL, IntraFuncURL_DC
        while len(funcMgrConfig) != 0:
            case1 = funcMgrConfig[0].split()
            if case1[0] == "Inter" and case1[1] == "Primary":
                case2 = funcMgrConfig[1].split()
                case3 = funcMgrConfig[2].split()
                case4 = funcMgrConfig[3].split()
                CDinterURL = case2[1]
                IntraMANOURL = case3[1]
                IntraFuncURL_Inter = case4[1]
                funcMgrConfig.pop(3)
                funcMgrConfig.pop(2)
                funcMgrConfig.pop(1)
                funcMgrConfig.pop(0)
            elif case1[0] == "Intra":
                case2 = funcMgrConfig[1].split()
                InterFuncURL = case2[1]
                funcMgrConfig.pop(1)
                funcMgrConfig.pop(0)
            elif case1[0] == "DC":
                case2 = funcMgrConfig[1].split()
                IntraFuncURL_DC = case2[1]

                os.chdir("/home/edward/funcInfo/")
                f = open("funcInfoList", "r")
                funcInfo = f.readlines()
                f.close()
                dcFuncInfoDict = infoConversion.formatDCFuncInfo(funcInfo)
                jsonMsg = json.dumps(dcFuncInfoDict)
                f = open("dcFuncList", "w")
                f.write(jsonMsg)
                f.close()

            else:
                funcMgrConfig.pop(0)


        # reqResult = funcHandlingUtil.sendFuncInfo(monitorURL, dcFuncInfoDict)
        # LOG.info(dcFuncInfoDict, "\n")
        # LOG.info("args: ", args, "\nkwargs: ", kwargs, "\n")
        # LOG.info("reqResult: ", reqResult)
        # print("jsonMsg: ", jsonMsg)

        mapper = wsgi.mapper
        # wsgi.registory['SR_API_Controller'] = self.data

        # sr_rules_path = '/sr_rules'
        # uri = sr_rules_path + '/insert'
        # mapper.connect('sr_rules', uri,
        #                controller=SR_API_Controller, action='insert_single_flow',
        #                conditions=dict(method=['POST']))
        monitor_path = '/funcMgr/req'
        uri = monitor_path + '/globalFuncDeploy'
        mapper.connect('funcMgr', uri,
                       controller=FUNC_MGR_Controller, action='request_of_regional_func_deploy',
                       conditions=dict(method=['POST']))

'''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        ovs_address = datapath.address[0]
        parameters = self.get_parameters(ovs_address)
        self.del_flows(datapath)
        self.dpid_to_datapath[datapath.id] = datapath
        self._push_bridging_flows(datapath, parser)
        LOG.info("New OVS connected: %d, still waiting for %s OVS to join ..." % (
        datapath.id, self.NUM_OF_OVS_SWITCHES - 1 - len(self.dpset.get_all())))
        if len(self.dpset.get_all()) == self.NUM_OF_OVS_SWITCHES - 1:
            try:
                SR_rest_api(dpset=self.dpset, wsgi=self.wsgi);
                SR_flows_mgmt.set_dpid_to_datapath(self.dpid_to_datapath)
                LOG.info("Datapath objects:")
                LOG.info(self.dpid_to_datapath)
                LOG.info("Northbound REST started!")
            except Exception as e:
                LOG.error("Error when start the NB API: %s" % e)
                '''
