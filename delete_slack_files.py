# /bin/python
import json
import os
import urllib
import urllib2

def get_user_id(token):
    user_data = urllib.urlencode(token)
    json_data = urllib2.urlopen("https://slack.com/api/auth.test", data=user_data).read()
    user = json.loads(json_data)
    return user['user_id']


def get_user_info(token, user_id):
    token['user'] = user_id
    encoded = urllib.urlencode(token)
    json_data = urllib2.urlopen('https://slack.com/api/users.info', data=encoded).read()
    return json.loads(json_data)['user']

def delete_file(file_id, token):
    token["file"] = file_id
    req = urllib2.Request("https://slack.com/api/files.delete", urllib.urlencode(token))
    resp = urllib2.urlopen(req)
    return resp.read()


def get_token(user):
    if user['is_admin']:
        return {"token": os.environ["SLACK_TOKEN"]}
    return {"token": os.environ["SLACK_TOKEN"], "user": user['id']}


def get_files(user):
    token = get_token(user)
    data = urllib.urlencode(token)
    json_data = urllib2.urlopen("https://slack.com/api/files.list", data=data).read()
    return json.loads(json_data)

token = {"token": os.environ["SLACK_TOKEN"]}
user_id = get_user_id(token)
user = get_user_info(token, user_id)

while True:
    resp = get_files(user)
    if not resp["ok"]:
        print resp
        print "failed"
        break
    if resp["paging"]["total"] == 0:
        print "done"
        break
    for f in resp["files"]:
        print delete_file(f["id"], get_token(user))
