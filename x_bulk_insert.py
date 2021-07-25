# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 25 Jul 2021
email: sabbiramin.cse11ruet@gmail.com, sabbir@rokomari.com

"""

import requests
from populate_data import bulk_generate

res = bulk_generate()
w = []
for model in res.get('models', []):
    researchId = model['researchId']
    author = model['author']
    publishDate = model['publishDate']
    status = model['status']
    researchText = model['researchText'].replace('\n', '').replace('\r', '')
    # researchText = 'sample data'

    temp = f"{{\"index\" : {{\"_index\" : \"paper-index-2\", \"_id\":\"{researchId}\" }}\n{{\"reseachId\":{researchId}," \
           f"\"author\":\"{author}\", \"publishDate\":\"{publishDate}\", \"status\":\"{status}\", \"researchText\":\"{researchText}\" }}\n"
    w.append(temp)
w.append('\n')
payload = ''.join(w)
url = "http://localhost:9200/_bulk"

headers = {"Content-Type": "application/x-ndjson"}
#
response = requests.request("POST", url, data=payload, headers=headers)
#
print(response.text)