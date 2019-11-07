# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI

connect=ZabbixAPI('http://172.20.103.201', user='zero',password='1alexander2')
zabbix= connect.api_version()
print (zabbix)

