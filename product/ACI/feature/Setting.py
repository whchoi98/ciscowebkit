#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#                                                                              #
################################################################################
#                                                                              #
# Copyright (c) 2016 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
# Licensed under the Apache License, Version 2.0 (the "License"); you may      #
# not use this file except in compliance with the License. You may obtain      #
# a copy of the License at                                                     #
#                                                                              #
# http://www.apache.org/licenses/LICENSE-2.0                                   #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################


'''
Created on 2016. 7. 27.

@author: "comfact"
'''

from ciscowebkit.common import *
 
class Setting(Feature):
    
    def __init__(self):
        Feature.__init__(self, icon='fa-wrench')
        
        form = Form('Connect')
        form.addText('domain', 'Domain', 'input unique domain name')
        form.addText('ips', 'APIC Address', 'x.x.x.x/y.y.y.y/z.z.z.z')
        form.addText('user', 'User', 'input admin name')
        form.addText('pwd', 'Password', 'input admin password')
        self.form_panel = Panel('Add Connection', form, icon='fa-asterisk')
        
        self.info = None;
        
    def get(self, request, *cmd):
        apic_table = Table('Domain', 'Address', 'User', 'Password', 'Connected')
        for domain in ACI._order: apic_table.add(domain, str(ACI[domain].ips), ACI[domain].user, ACI[domain].pwd, ACI[domain].connected, did=domain)
        
        if self.info:
            lo = Layout(Row(Col(self.info)))
            self.info = None
        else: lo = Layout()
        
        lo(
            Row(self.form_panel),
            Row(Panel('Connection List', apic_table, icon='fa-table'))
        )
        
        return lo
    
    def post(self, request, data, *cmd):
        apic = ACI.addDomain(data.domain, data.ips, data.user, data.pwd)
        if apic: self.info = InfoBlock('연결성공', u'%s의 APIC과 %s로 연결되었습니다.' % (apic.domain, apic.connected)) 
        else: self.info = InfoBlock('연결실패', 'APIC 연결이 실패하였습니다. 연결정보를 확인하세요.')
        return self.get(request, *cmd)
    
    def delete(self, request, data, *cmd):
        ACI.delDomain(data)
        self.info = InfoBlock('연결삭제', '%s의 연결을 제거하였습니다.' % data)
        return self.get(request, *cmd)