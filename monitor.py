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
import datetime
from info_conversion import info_conversion
from iproute2_utils import iproute2_utils
import requests
import os
import uuid

LOG = logging.getLogger('ryu.app.monitor')
LOG.setLevel(logging.INFO)

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST',
    'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, X-Requested-With'}

region_id = ""
interRegionResourceInfoList = []
interRegionResourceInfoRegionIdList = []

class Monitor(ControllerBase):

    def __init__(self, req, link, data, **config):
        super(Monitor, self).__init__(req, link, data, **config)


    def insert_single_flow(self, req, **kwargs):
        req_body = req.body
        LOG.debug(req_body)
        # req_body_dec = req_body.decode('utf-8')
        infoConversion = info_conversion()
        iproute2u = iproute2_utils()
        match_fields = infoConversion.parse_match_fields(req_body)
        LOG.info("--------------- Match Fields Start ---------------")
        for key in match_fields:
            LOG.info("%s:   %s", key, match_fields[key])
        LOG.info("--------------- Match Fields End -----------------")
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname='131.113.71.192', port=22, username='root', password='Zhaizehua960929')
        # stdin, stdout, stderr = ssh.exec_command('ps -ef | grep test')
        # print(stdout.read().decode())
        # ssh.close()
        iproute2u.insert_srv6_rule_local(match_fields)

        # print("req_body:", req_body)
        return Response(content_type='application/json', status=200, body=json.dumps("TEST OK!"),
                        charset='utf8', headers=HEADERS)

    def dc_scope_to_intra(self, req, **kwargs):
        req_body = req.body
        LOG.debug(req_body)
        msg_dec = req_body.decode()
        print("req.client_addr: ", req.client_addr)
        # LOG.info("msg_dec: ", msg_dec)
        jsonMsg = json.loads(msg_dec)
        infoConversion =info_conversion()
        reqHandler = reqHandling()
        intraFuncInfo = infoConversion.DCScopeToIntra(jsonMsg, region_id)
        # print("intraFuncInfo: ", intraFuncInfo)
        # reqHandler.sendFuncInfo("http://[2001:200:0:6811:2000:100:0:1]:8000/monitor/inter", intraFuncInfo)


    def intra_scope_to_inter(self, req, **kwargs):
        global interRegionResourceInfoList, interRegionResourceInfoRegionIdList
        req_body = req.body
        LOG.debug(req_body)
        msg_dec = req_body.decode()
        # LOG.info("msg_dec: ", msg_dec)
        jsonMsg = json.loads(msg_dec)
        if jsonMsg["regionId"] in interRegionResourceInfoRegionIdList:
            for Idx in range(len(interRegionResourceInfoList)):
                if interRegionResourceInfoList[Idx]["regionId"] == jsonMsg["regionId"]:
                    interRegionResourceInfoList.pop(Idx)
        else:
            interRegionResourceInfoRegionIdList.append(jsonMsg["regionId"])
            interRegionResourceInfoList.append(jsonMsg)

        # infoConversion = info_conversion()
        # reqHandler = reqHandling()
        # intraFuncInfo = infoConversion.DCScopeToIntra(jsonMsg, region_id)
        print("interFuncInfo: ", jsonMsg)

class reqHandling(object):

    def __init__(self):
        super(reqHandling, self).__init__()

    def sendFuncInfo(self, url, postMsg):
        s = json.dumps(postMsg)
        # keep = True
        # while keep:
        try:
            r = requests.post(url, data=s, timeout=5)
            keep = False
        except Exception as e:
            print(datetime.datetime.now(), " Request failed!")
        # r = requests.post(url, data=s, timeout=5)
        return r


class InitMonitor(app_manager.RyuApp):
    _CONTEXTS = {
        'wsgi': WSGIApplication,
    }

    def __init__(self, *args, **kwargs):
        super(InitMonitor, self).__init__(*args, **kwargs)
        wsgi = kwargs['wsgi']
        mapper = wsgi.mapper
        # region_id = ""
        # wsgi.registory['SR_API_Controller'] = self.data

        global region_id
        if os.path.exists("region_id"):
            f = open("region_id", "r")
            region_id = f.readline()
            f.close()
        else:
            f = open("region_id", "w")
            region_id = str(uuid.uuid4())
            f.write(region_id)
            f.close()



        monitor_path = '/monitor'
        uri = monitor_path + '/intra'
        mapper.connect('monitor', uri,
                       controller=Monitor, action='dc_scope_to_intra',
                       conditions=dict(method=['POST']))
        uri = monitor_path + '/inter'
        mapper.connect('monitor', uri,
                       controller=Monitor, action='intra_scope_to_inter',
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
