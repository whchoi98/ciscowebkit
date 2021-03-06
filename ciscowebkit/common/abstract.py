#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#        _____ _                  _____           _                            #
#       / ____(_)                / ____|         | |                           #
#      | |     _ ___  ___ ___   | (___  _   _ ___| |_ ___ _ __ ___  ___        #
#      | |    | / __|/ __/ _ \   \___ \| | | / __| __/ _ \ '_ ` _ \/ __|       #
#      | |____| \__ \ (_| (_) |  ____) | |_| \__ \ ||  __/ | | | | \__ \       #
#       \_____|_|___/\___\___/  |_____/ \__, |___/\__\___|_| |_| |_|___/       #
#                                        __/ |                                 #
#                                       |___/                                  #
#           _  __                       _____       _  _____ ______            #
#          | |/ /                      / ____|     | |/ ____|  ____|           #
#          | ' / ___  _ __ ___  __ _  | (___   ___ | | (___ | |__              #
#          |  < / _ \| '__/ _ \/ _` |  \___ \ / _ \| |\___ \|  __|             #
#          | . \ (_) | | |  __/ (_| |  ____) | (_) | |____) | |____            #
#          |_|\_\___/|_|  \___|\__,_| |_____/ \___/|_|_____/|______|           #
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
Created on 2016. 7. 15.

@author: "comfact"
'''

from ciscowebkit.common.pygics import instof, SingleTon, M

class __Feature__(SingleTon, M):
    
    def __init__(self, tick, icon):
        M.__init__(self, _tick=tick*1000, _icon=icon)
        
    def get(self, request, *cmd):
        return __View__('none')
    
    def post(self, request, data, *cmd):
        return __View__('none')
    
    def update(self, request, data, *cmd):
        return __View__('none')
    
    def delete(self, request, data, *cmd):
        return __View__('none')
    

class __View__(M):
    
    def __init__(self, ux, **kargs):
        M.__init__(self, _ux=ux, **kargs)
        
    def __create_link__(self, link):
        if instof(link, tuple):
            flink, clink = link
            if flink != None or clink != None:
                return ''' onclick="show_feature('%s','%s');"''' % (flink['_code'] if flink else '', clink if clink else '')
        return ''
    
    def __create_del__(self, did):
        return '''<p class="close" style="float:left !important;padding:0px 5px 0px 0px;margin:0px;" onclick="del_data('%s');"> &times; </p>''' % did if did else ''
        
    def __render__(self):
        return ''
