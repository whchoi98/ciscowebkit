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

################################################################################
#                                  _    ____ ___                               #
#                                 / \  / ___|_ _|                              #
#                                / _ \| |    | |                               #
#                               / ___ \ |___ | |                               #
#                         _____/_/   \_\____|___|_ _                           #
#                        |_   _|__   ___ | | | _(_) |_                         #
#                          | |/ _ \ / _ \| | |/ / | __|                        #
#                          | | (_) | (_) | |   <| | |_                         #
#                          |_|\___/ \___/|_|_|\_\_|\__|                        #
#                                                                              #
################################################################################
#                                                                              #
# Copyright (c) 2015 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
"""
ACI Toolkit module for Health Scores
"""
import json


class HealthScore(object):
    """
    A class for Health Score objects
    """
    def __init__(self):
        self.chng = None
        self.cur = None
        self.dn = None
        self.prev = None
        self.lastchanged = None

    def __str__(self):
        return self.cur

    @classmethod
    def _get_apic_classes(cls):
        """
        Get the APIC classes used by this acitoolkit class.
        :returns: list of strings containing APIC class names
        """
        return ['healthInst']

    @classmethod
    def _get_url(cls):
        return '/api/class/{}.json'.format(cls._get_apic_classes()[0])

    @classmethod
    def _get_by_url(cls, session, url):
        """
        Helper for other get methods e.g get(), get_by_dn()
        :param session: Session object for communicating with APIC
        :param url: the URL to query for healthInst objects
        :return: list of HealthScore objects
        """
        resp = session.get(url)
        scores = json.loads(resp.text)['imdata']
        objects = []
        for score in scores:
            obj = HealthScore()
            attribute_data = score[cls._get_apic_classes()[0]]['attributes']
            obj._populate_from_attributes(attribute_data)
            objects.append(obj)
        return objects

    def _populate_from_attributes(self, attributes):
        """
        populates HealthScore object from attributes
        """
        self.chng = attributes['chng']
        self.cur = attributes['cur']
        self.dn = attributes['dn']
        self.prev = attributes['prev']
        self.lastchanged = attributes['updTs']

    @classmethod
    def get(cls, session, obj):
        """
        Gets HealthScore for an object
        :param session: the instance of Session used for APIC communication
        :param obj: ACI Toolkit object
        :returns: HealthScore object
        """

        return cls.get_by_dn(session, obj.dn)

    @classmethod
    def get_all(cls, session):
        """
        Gets all of the Health Scores from the APIC.
        :param session: the instance of Session used for APIC communication
        :returns: List of HealthScore objects
        """

        url = cls._get_url()
        objects = cls._get_by_url(session, url)
        return objects

    @classmethod
    def get_unhealthy(cls, session, threshold):
        """
        Gets all health scores below a certain value
        :param session the instance of Session used for APIC communication
        :param threshold integer for determining unhealthy objects
        :returns: List of HealthScore objects
        """
        url = '/api/node/class/healthInst.json?' \
              'query-target-filter=and(lt(healthInst.cur,"{}"))'.format(threshold)
        objects = cls._get_by_url(session, url)
        return objects

    @classmethod
    def get_by_dn(cls, session, dn):
        url = '/api/node/mo/{}/health.json'.format(dn)
        obj = cls._get_by_url(session, url)[0]
        return obj
    
    
    
    #===========================================================================
    # Additional Feature
    #===========================================================================
    
    @classmethod
    def get_topology_health(cls, session):
        ret = {}
        resp = session.get('/api/class/fabricHealthTotal.json?')
        scores = json.loads(resp.text)['imdata']
        for score in scores:
            dn = score['fabricHealthTotal']['attributes']['dn']
            value = int(score['fabricHealthTotal']['attributes']['cur'])
            if dn == 'topology/health': dn = 'total'
            else: dn = dn[9:-7]
            ret[dn] = value
        resp = session.get('/api/class/fabricNodeHealth5min.json?')
        scores = json.loads(resp.text)['imdata']
        for score in scores:
            dn = score['fabricNodeHealth5min']['attributes']['dn'].split('/sys/')[0][9:]
            value = int(score['fabricNodeHealth5min']['attributes']['healthLast'])
            ret[dn] = value
        return ret
    
    @classmethod
    def get_tenant_health(cls, session):
        ret = {}
        resp = session.get('/api/class/healthInst.json?query-target-filter=wcard(healthInst.dn,"^uni/tn-")')
        scores = json.loads(resp.text)['imdata']
        for score in scores:
            dn = score['healthInst']['attributes']['dn'][4:-7]
            if 'topology' in dn: continue
            value = int(score['healthInst']['attributes']['cur'])
            ret[dn] = value
        return ret
