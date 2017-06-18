# /bin/python
import urllib2
import urllib
import json
import os

while True:
	token = {"token": os.environ["SLACK_TOKEN"]}
	data = urllib.urlencode(token)
	json_data = urllib2.urlopen("https://slack.com/api/files.list", data=data).read()
	resp = json.loads(json_data)
	if not resp["ok"]:
		print resp
		print "failed"
		break
	if resp["paging"]["total"] == 0:
		print "done"
		break
	for f in resp["files"]:
		token["file"] = f["id"]
		req = urllib2.Request("https://slack.com/api/files.delete", urllib.urlencode(token))
		resp = urllib2.urlopen(req)
		print resp.read()
