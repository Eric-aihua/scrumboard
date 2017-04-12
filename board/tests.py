# encoding:utf-8
from pprint import pprint

import datetime
import random

import requests
from django.test import TestCase

# Create your tests here.

URL_BASE = 'http://localhost:8000/api'
auth=('demo','demotest')
response = requests.get(URL_BASE)
api = response.json()

class ScrumBoardTestCase(TestCase):

    def test_get_rest_add_sprint(self):
        end_data=datetime.date.today()+datetime.timedelta(days=random.randint(1,50))
        sprint_data=  {
                   "name": ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',10)),
                   "description": "this is a test sprint",
                   "end": end_data,
               }
        # 创建sprint
        sprint_response=requests.post(api['sprints'],data=sprint_data,auth=auth)
        self.assertEqual(sprint_response.status_code, 201)
        sprint=sprint_response.json()
        task_data={
            "name": ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',10)),
            "description":''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',10)),
            "assigned":"demo",
            'sprint':sprint['id']
        }
        #创建task
        response=requests.post(api['tasks'],data=task_data,auth=auth)
        self.assertEqual(response.status_code, 201)
        task=response.json()
        task['description']='update by put'
        #update task
        response=requests.put(task['links']['self'],data=task,auth=auth)
        self.assertEqual(response.status_code, 200)


