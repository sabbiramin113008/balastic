# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 25 Jul 2021
email: sabbiramin.cse11ruet@gmail.com, sabbir@rokomari.com

"""
import codecs
import json
import random
import uuid

from faker import Faker

source_json_file = 'resources/raw_paper_info.json'
bulk_insertion_paper_data = 'resources/bulk_insertion_paper_data.txt'


def bulk_generate(n=20):
    '''
    {
        reserchId: <Integer; Unique id of the paper>,
        author: <String; Name of the author>,
        publishDate: <Date; Date of publication>,
        status: <String; Possible values: SUBMITTED, ACCEPTED, REJECTED>,
        reserchText: <String; The paper>
    }
    :return: list
    '''
    status_choice = ['SUBMITTED', 'ACCEPTED', 'REJECTED']
    faker = Faker()
    models = []
    for i in range(1, n):
        researchId = i
        author = faker.name()
        publishDate = (faker.date_between(start_date='-20y', end_date='today'))
        status = random.choice(status_choice)
        researchText = str(faker.text()).strip().replace('\\n', '')

        print(researchId, author, publishDate, status, researchText)
        model = dict()
        model['researchId'] = i
        model['author'] = author
        model['publishDate'] = publishDate.strftime('%Y-%m-%d')
        model['status'] = status
        model['researchText'] = researchText
        models.append(model)
    res = dict()
    res['models'] = models
    with codecs.open(source_json_file, 'w', 'utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)


def prep_request_file_for_curl(source_file_name=source_json_file):
    with codecs.open(source_file_name, 'r', 'utf-8') as f:
        res = json.load(f)
        w = []
        for model in res.get('models', []):
            researchId = model['researchId']
            author = model['author']
            publishDate = model['publishDate']
            status = model['status']
            researchText = model['researchText'].replace('\n', '').replace('\r', '')
            # researchText = 'sample data'

            temp = f"{{\"index\" : {{\"_index\" : \"paper_index\", \"_id\":\"{researchId}\" }}\\n\n{{\"reseachId\":{researchId}," \
                   f"\"author\":\"{author}\", \"publishDate\":\"{publishDate}\", \"status\":\"{status}\", \"researchText\":\"{researchText}\" }}\n"
            w.append(temp)
        w.append('\n')
        with codecs.open(bulk_insertion_paper_data, 'w', 'utf-8') as f:
            f.writelines(w)


if __name__ == '__main__':
    # Dump and Generate JSON Dummy File
    bulk_generate()
    # Prepare bulk insertion request file for _bulk insert
    prep_request_file_for_curl()
