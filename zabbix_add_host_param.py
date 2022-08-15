# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
from pprint import pprint
from transliterate import translit,get_available_language_codes
import MySQLdb
import re
import argparse
import sys
import logging

#выполнить подключние к zabbix и выполение запросов
def zabbix_con(url,us,pas):
    """Connnect to zabbix server over api"""
    try:
      zabbix_connect= ZabbixAPI(url, user=us,password=pas)
      return zabbix_connect
    except:
      print ('Warning: error to connect zabbix api')
      return ('')

def sql_connect(ip,us,pas,base):
    """Connect to server mysql hosted Kurs database"""
    try:
      sql_connect = MySQLdb.connect(host=ip,
                              user=us,
                              password=pas,
                              charset='utf8',
                              use_unicode=False,
                              db=base)
      cursor=sql_connect.cursor()
      return cursor
    except MySQLdb.Error as error:
           print ('Warning: error to connect database',error.args[1])
           return 'error'

def main():

 parser = argparse.ArgumentParser(description='Добавление секторов(изменение имени,добавление в группу  Синхронизация с Курс) в zabbix, по хостам обнаруженным в группе Потеряшки')
 
 parser.add_argument ('-sql', action='store',dest='sql_server', default='192.168.0.5', help="ip address mysql_server  hosted system Kurs")
 parser.add_argument ('-user', action='store',dest='sql_user',default='script',  help="username for acces to mysq_server hosted system Kurs")
 parser.add_argument ('-pass', action='store',dest='sql_pass',default='script', help="password for acces to mysq_server hosted system Kurs")
 parser.add_argument ('-db', action='store',dest='sql_base',default='radio', help="name database on  mysq_server bg Kurs")
 parser.add_argument ('-zab_api', action='store',dest='url_zab_api',default='http://172.20.103.201', help="url to access zabbix api")
 parser.add_argument ('-zab_user', action='store',dest='user_zab',default='zero', help="user name to access zabbix api")
 parser.add_argument ('-zab_pass', action='store',dest='pass_zab',default='1alexander2', help="pass to access zabbix api")
 parser.add_argument ('-debug',action='store_true',dest='debug',default=False, help="Enable Debug")
 #считываем параметры
 args=parser.parse_args()
 if args.debug == True:
  logging.basicConfig(filename='debug.log',level=logging.DEBUG)
  # CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET
 # подключаемся к api zabbix
 zabbix_connect=zabbix_con(args.url_zab_api,args.user_zab,args.pass_zab)
 #подключаемся с mysql kurs
 cursor=sql_connect(args.sql_server,args.sql_user,args.sql_pass,args.sql_base)
 #print ('#',cursor)
 if zabbix_connect :
 # запрос id group по имени Группы
  for group in zabbix_connect.hostgroup.get(output="extend") :
      if 'Потеряшки' in group['name'] :
          groupid=group['groupid']
          print ('Поиск новых секторов в Потеряшки id:',groupid)
   #список устройств по id group
  for host in zabbix_connect.host.get(groupids=groupid) :
     if host['host'] == host ['name'] :
#      if '192.168.30.143'  in  host['host']:
#      if '192.168.30.141' or '192.168.32'  in  host['host']:
  #       print (host)
  # делаем запрос в курс
        if cursor != 'error':
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
if __name__ == "__main__":
     sys.exit(main())
