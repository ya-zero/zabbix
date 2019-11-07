# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
from pprint import pprint
from transliterate import translit,get_available_language_codes
import MySQLdb
import re
#выполнить подключние к zabbix и выполение запросов
def zabbix_connect():
    try:
      zabbix_connect= ZabbixAPI('http://172.20.103.201', user='zero',password='1alexander2')
      return zabbix_connect
    except:
      return ('')

def sql_connect():
    try:
      sql_connect = MySQLdb.connect(host='192.168.0.5',
                              user='script',
                              password='script',
                              charset='utf8',
                              use_unicode=False,
                              db='radio')

      cursor=sql_connect.cursor()
      return cursor
    except MySQLdb.Error as error:
      return error


#запросы
zabbix_connect=zabbix_connect()
cursor=sql_connect()
print ('dd',cursor)
if zabbix_connect:
 # запрос id group по имени Группы
 for group in zabbix_connect.hostgroup.get(output="extend"):
     if 'Потеряшки' in group['name']:
         groupid=group['groupid']
         print ('Потеряшки id',groupid)
  #список устройств по id group
 for host in zabbix_connect.host.get(groupids=groupid):
    if host['host'] == host ['name'] :
#      if '192.168.30.143'  in  host['host']:
#      if '192.168.30.141' or '192.168.32'  in  host['host']:
  #       print (host)
  # делаем запрос в курс
       if cursor :
         sql='''SELECT DIP.id,CONCAT_WS(" ", CONCAT("AK-", DC.fio), CONCAT("BS", DB.base, " ", DB.address),
              CONCAT("RRL-Master ", DRL1.comments), CONCAT("RRL-Slave ", DRL2.comments))
              FROM devices_ip_addresses DIP
              LEFT JOIN devices_bases DB ON DIP.id = DB.ip_id
              LEFT JOIN devices_complekts DC ON DIP.id = DC.ip_id
              LEFT JOIN devices_rrl DRL1 ON DIP.id = DRL1.ip_id_master
              LEFT JOIN devices_rrl DRL2 ON DIP.id = DRL2.ip_id_slave
              WHERE ip = "%s"'''% host['host']
         try:
             cursor.execute(sql)
             for row1,row2 in cursor:
                 #print ('tut2',row2.decode('utf8'),host['host'])
                 if row2: # не пустое
                   kurs_name=(translit(row2.decode('utf8'),'ru',reversed=True))
                   print (kurs_name,host['host'])
                   new_kurs_name=re.search('\d+.\d+.(\d+.\d+)',host['host'])
                   new_kurs_name=new_kurs_name.group(1)+'_'+kurs_name

                   zabbix_connect.host.update(hostid=host['hostid'],name=new_kurs_name)
                   zabbix_connect.hostgroup.massadd(groups='107',hosts=host['hostid'])
         except MySQLdb.Error as error:
                 print ('MySQL SELECT error {}'.format(error))

#     print (translit(i['name'],'ru',reversed=True))
