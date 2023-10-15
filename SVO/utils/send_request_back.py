import json,requests


def send_it_back(my_url,  body):
    # handler che elabora la richiesta
    url_rec_back = body["vo_url"] + "receive/friendship/back"
    print(url_rec_back)
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    param = {"vo_url": my_url, "type": body["type"]}
             #"tag":body["tag"]}
    payload = json.dumps(param)
    requests.post(url_rec_back, data=payload)