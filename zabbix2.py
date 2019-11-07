# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
from pprint import pprint
from transliterate import translit,get_available_language_codes
#import pymysql.cursors

zabbix_connect= ZabbixAPI('http://172.20.103.201', user='zero',password='1alexander2')
'''
sql_connect = pymysql.connect(host='192.168.0.5',
                              user='root',
                              db='radio',
                              password='yfbvtyjdfybt',
                              charset='utf8mb4',
                              use_unicode=True,
                              cursorclass=pymysql.cursors.DictCursor)

#try:
#    with 
cursor=sql_connect.cursor()
cursor.execute("SET NAMES 'utf8'")
sql='SELECT * FROM devices_bases'
sql2='''SELECT CONCAT_WS(" ", CONCAT("AK-", DC.fio), CONCAT("BS", DB.base, " ", DB.address), CONCAT("RRL-Master ", DRL1.comments), CONCAT("RRL-Slave ", DRL2.comments))
FROM devices_ip_addresses DIP
LEFT JOIN devices_bases DB ON DIP.id = DB.ip_id
LEFT JOIN devices_complekts DC ON DIP.id = DC.ip_id
LEFT JOIN devices_rrl DRL1 ON DIP.id = DRL1.ip_id_master
LEFT JOIN devices_rrl DRL2 ON DIP.id = DRL2.ip_id_slave
WHERE ip = "192.168.30.65"'''


cursor.execute(sql2)
#print('cursor.description',cursor.description)
c=0
for row in cursor:
       print (row.values().decode('utf-8'))
       c+=1


'''
# запрос id group по имени Группы
for group in zabbix_connect.hostgroup.get(output="extend"):
#     print (translit(i['name'],'ru',reversed=True))
     if 'Потеряшки' in group['name']:
         groupid=group['groupid']
         print ('Потеряшки id',groupid)

#список устройств по id group

i=0
for host in zabbix_connect.host.get(groupids=groupid):
        if host['host'] == host ['name']:
           if '192.168.32.' in  host['host']:
               pprint (host)
               i+=1
print ('count zabbix: {} курс: {}'.format(i,c))
'''