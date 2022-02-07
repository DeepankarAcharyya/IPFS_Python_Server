import flask
from flask import request
from flask_cors import CORS
import json
import requests
from werkzeug.utils import secure_filename
import urllib.request

app = flask.Flask(__name__)
CORS(app)

'''
Set this variable before running the script
It is free for nft.storage
'''
ipfs_token = '<api_token>'

ipfs_endpoint = 'https://api.nft.storage/upload'

@app.route("/ipfs_upload_file", methods=["POST"])
def ipfsUpload():
    
    if 'file' not in request.files:
        resp = json.dumps({'result': 'No file part in the request'})
        return resp
    else:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(filename)
        header = {"Authorization":'Bearer {}'.format(ipfs_token)}
        files = {'file': (filename, open(filename, 'rb'))}
        data = requests.post(ipfs_endpoint, files=files, headers=header)
        data = json.loads(data.content.decode('utf-8'))
        print(data["value"]["cid"])
        return dict(data)

def get_filename(cid):
    header = {"Authorization":'Bearer {}'.format(ipfs_token)}
    data = requests.get('https://api.nft.storage/'+cid,headers=header).content
    data = json.loads(data.decode('utf-8'))
    return data['value']['files'][0]['name']

@app.route("/ipfs_retrieve_file", methods=["POST"])
def retrieveAssetFromIPFS():
    data = request.get_json()
    cid = data["cid"]
    url = "https://ipfs.io/ipfs/"+str(cid)+"/"+get_filename(cid)
    filename = get_filename(cid)
    urllib.request.urlretrieve(url, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    