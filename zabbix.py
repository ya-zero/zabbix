# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
from pprint import pprint
from transliterate import translit,get_available_language_codes
import MySQLdb

#выполнить подключние к zabbix
zabbix_connect= ZabbixAPI('http://172.20.103.201', user='zero',password='1alexander2')
sql_connect = MySQLdb.connect(host='192.168.0.5',
                              user='root',
                              password='yfbvtyjdfybt',
                              charset='utf8',
                              use_unicode=False,
                              db='radio')

#try:
#    with 
cursor=sql_connect.cursor()
print (cursor)
#cursor.execute("SET NAMES UTF8")
#cursor.execute("SET CHARACTER SET 'utf8'")
#cursor.execute("SET character_set_connection=utf8")
sql='SELECT * FROM devices_bases'

sql2='''SELECT DIP.id,CONCAT_WS(" ", CONCAT("AK-", DC.fio), CONCAT("BS", DB.base, " ", DB.address), CONCAT("RRL-Master ", DRL1.comments), CONCAT("RRL-Slave ", DRL2.comments))
FROM devices_ip_addresses DIP
LEFT JOIN devices_bases DB ON DIP.id = DB.ip_id
LEFT JOIN devices_complekts DC ON DIP.id = DC.ip_id
LEFT JOIN devices_rrl DRL1 ON DIP.id = DRL1.ip_id_master
LEFT JOIN devices_rrl DRL2 ON DIP.id = DRL2.ip_id_slave
WHERE ip = "192.168.32.43"'''


cursor.execute(sql2)
#print('cursor.description',cursor.description)
for row1,row2 in cursor:
    print (row2.decode('utf8'))
    kurs_name=row2.decode('utf8')

# запрос id group по имени Группы
#for group in zabbix_connect.hostgroup.get(output="extend"):
#     print (translit(i['name'],'ru',reversed=True))
#     if 'системой Курс' in group['name']:
#         groupid=group['groupid']
#         print ('Потеряшки id',groupid)

#список устройств по id group
#for host in zabbix_connect.host.get(groupids=groupid):
#        if host['host'] == host ['name']:
#           if '192.168.32.101' in  host['host']:
#               pprint (host)
'''
изменение параметров хоста. по host  имя(name)
добавить в группу.
'''
#kurs_name=(translit(kurs_name,'ru',reversed=True))
#zabbix_connect.host.update(hostid='11010',name=kurs_name)

#zabbix_connect.hostgroup.massadd(groups='107',hosts='11010')
#     print (translit(i['name'],'ru',reversed=True))