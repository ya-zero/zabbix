# -*- coding: utf-8 -*-

import requests
import json
r= requests.get('http://192.168.0.4:8080/bgbilling/executer/json/ru.bitel.bgbiiling.kernel.conntarck.api/ContrackService')
print (r.status_code)
#print (r.headers['content-type'])
bill_data = {"method" : "contractList",
"user" :{ "user" : "shamil", "pswd" : "xxxx" },
"params" : {
"title" : "0",
"fc" : -1,
"groupMask" : 0,
"closed" : True,
"hidden" : False,
"page" : { "pageIndex" : 2, "pageSize" : 2 }
} }

r= requests.post('http://192.168.0.4:8080/bgbilling/executer/json/ru.bitel.bgbiiling.kernel.conntarck.api/ContrackService',data=json.dumps(bill_data))
print(r.text)