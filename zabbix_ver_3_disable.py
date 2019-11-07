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
if cursor :
     sql = '''SELECT address,devices_bases.id,devices_ip_addresses.ip FROM devices_bases INNER JOIN devices_ip_addresses ON (devices_bases.ip_id = devices_ip_addresses.id) WHERE devices_bases.is_deleted = "1";'''
     try:
         cursor.execute(sql)
         for row1 in cursor:
             print (list(row1)[2].decode('utf8'))
     except MySQLdb.Error as error:
             print ('MySQL SELECT error {}'.format(error))

