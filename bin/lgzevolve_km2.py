import requests
import requests_jwt
import json
import ast
import os

import logging
logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import pprint 
pp=pprint.PrettyPrinter(indent=4)

GOOGLER='/usr/local/bin/googler'


def create_question():
    TICKET_API='http://10.19.226.116:3030/tickets'
    question = {
        "status":"new",
        "due_date":"2018-07-22",
        "description":"",
        "assign": "googler",
        "tags":"tag1,tag2",
        "children":"124,3,4,5,6",
        "estimateEffort":"1hours",
        "Weight":"0",
        "title":"vuejs fogbugz",
        "created":"2018-06-22",
        "tid":"1",
        "spentEffort": "2hours"
    }
    requests.post(TICKET_API,data=question)

def submit_answers(answers_list,question_id):
    ANSWERS_API='http://10.19.226.116:3030/answers'
    for ele in answers_list:
        ele['vote'] = 0
        ele['user'] = 'googler'
        ele['tid']  = question_id
        ele['comments']= ''
        requests.post(ANSWERS_API,data=ele)
def update_question(question_id,update):
    TICKET_API='http://10.19.226.116:3030/tickets/{}'.format(question_id)
    requests.patch(TICKET_API,data=update)
def main():
    TICKET_API='http://10.19.226.116:3030/tickets'
    ticket_requests = requests.get(TICKET_API)
    questions = json.loads(ticket_requests.content)['data']
    for question in questions:
        if question.has_key('assign') and question['assign'] == "googler":
           print(u"{}, {}".format(question['title'],question['_id']))
           cmd = [GOOGLER,"-c hk", "-n 10", "--np --json" ,question['title']]
           logger.info(cmd)
           out= os.popen(" ".join(cmd)).read()
           logger.info(out)
           update = {
               "assign": "lgw"
           }
           update_question(question['_id'],update)
           answers = ast.literal_eval(out)
           submit_answers(answers,question['_id'])



if __name__ == "__main__":
    #create_question()
    main()
