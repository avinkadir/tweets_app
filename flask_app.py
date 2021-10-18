from flask import Flask
from flask_celery import make_celery
from celery.result import AsyncResult
import os
import subprocess
import sys

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://avin:123@localhost:5672/vh1',
    CELERY_RESULT_BACKEND='rpc://'
)

celery = make_celery(flask_app)

@flask_app.route('/pronouns/', methods=['GET'])
def process1():
  result = pronouns.delay()
  res = result.get()

  with open('data.dat', 'w') as f:
    f.write('han ' + str(res[0]) + "\n")
    f.write('hon ' + str(res[1]) + "\n")
    f.write('hen ' + str(res[2]) + "\n")
    f.write('den ' + str(res[3]) + "\n")
    f.write('det ' + str(res[4]) + "\n")
    f.write('denna ' + str(res[5]) + "\n")
    f.write('denne ' + str(res[6]) + "\n")

  data=subprocess.check_output(["termgraph","data.dat"])
  return data

@celery.task(name='flask_celery.count_pronouns')
def pronouns():
  han = 0
  hon = 0
  den = 0
  det = 0
  denna = 0
  denne = 0
  hen = 0

  for filename in os.listdir("data"):
     with open(os.path.join("data", filename), 'r') as f:
         for line in f:
           if line != "\n":
              start_index = line.find("text") + len("text") + 3
              end_index = line.find("source") - 3
              text = line[start_index:end_index]
              text_list = list(text.split(" "))
              if text_list[0] != "RT":
                han += text_list.count("han")
                hon += text_list.count("hon")
                den += text_list.count("den")
                det += text_list.count("det")
                denna += text_list.count("denna")
                denne += text_list.count("denne")
                hen += text_list.count("hen")

  return [han, hon, hen, den, det, denna, denne]


if __name__ == '__main__':
  flask_app.run(host='0.0.0.0',debug=True)
