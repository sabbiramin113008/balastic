# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 25 Jul 2021
email: sabbiramin.cse11ruet@gmail.com, sabbir@rokomari.com

"""
import random

from locust import HttpUser, task, between
from populate_data import bulk_generate


def prepare_payload(n):
    res = bulk_generate(n)
    w = []
    for model in res.get('models', []):
        researchId = model['researchId']
        author = model['author']
        publishDate = model['publishDate']
        status = model['status']
        researchText = model['researchText'].replace('\n', '').replace('\r', '')

        temp = f"{{\"index\" : {{\"_index\" : \"paper_index\", \"_id\":\"{researchId}\" }}\n{{\"reseachId\":{researchId}," f"\"author\":\"{author}\", \"publishDate\":\"{publishDate}\", \"status\":\"{status}\", \"researchText\":\"{researchText}\" }}\n"
        w.append(temp)
    w.append("\n")
    payload = ''.join(w)
    return payload


class ElasticLocust(HttpUser):
    base_url = 'http://localhost:9200/'
    wait_time = between(1, 2.5)

    @task(100)
    def get_doc_details_by_id(self):
        doc_id = random.randint(100, 10000)
        url = 'http://localhost:9200/paper_index/_doc/{}'.format(doc_id)
        response = self.client.get(url)
        print(response.json())

    @task(10)
    def bulk_insert(self):
        url = "http://localhost:9200/_bulk"

        payload = prepare_payload(n=30)
        headers = {"Content-Type": "application/x-ndjson"}

        response = self.client.post(url=url, data='{}\n'.format(payload), headers=headers)
        print(response.json())
