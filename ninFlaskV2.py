from threading import Thread
from flask import Flask, request
import os
import json
import requests
from flask_discord_extended import FlaskDiscord

print(os.getcwd())
app = Flask("app")

app.config["DISCORD_AUTHORIZATION"] = "MTE4MzM2NjgzNTgzNjU1MTE2OA.GqQIOG.PgM6ol1OyiKviuQLOaVk9l2D4ZIQ9VhUO0aEPQ"
Discord = FlaskDiscord(app)

ipath="aiueo/1.json"
ipath2="aiueo/"

@app.route('/', methods=["GET"])
def index():
    try:
        id = request.args.get('code', '')
        if id == "":
          return
        server = request.args.get('state', '')
        server = server.split(",")
        
        API_ENDPOINT = 'https://discord.com/api/v10'
        CLIENT_ID = ['1183366835836551168']
        my_secret = ['TlJwVp9BW7dvBOWlsz4GOLgmdxfzbjsx']
        CLIENT_SECRET = my_secret
        REDIRECT_URI = 'https://yuushijinzi.uhegeje.repl.co/'
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': id,
            'redirect_uri': REDIRECT_URI
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
        r.raise_for_status()
        tokens = json.loads(r.text)
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']

    # jsonへの保存
        user_tokens = {user: {"access_token": access_token, "refresh_token": refresh_token}}
        json.dump(user_tokens, open(f"{ipath}","w"))
        data = requests.get(API_ENDPOINT + '/users/@me', headers={'Authorization': f'Bearer {token}'})
        user = json.loads(data.text)["id"]
        name = json.loads(data.text)["username"]
        ck=Discord.Utilities.add_role(guild=server[0], user_id=user, role=server[1])
        if not f"{server[1]}" in ck["roles"]:
          return "<h1>ロールを付与できませんでした</h1>"

        try:
          serveridj = open(f"{ipath2}{server[0]}.json")
        except:
          f = open(f"{ipath2}{server[0]}.json","w")
          f.write('{}')
          f.close()
          serveridj = open(f"{ipath2}{server[0]}.json")
        serverid=json.load(serveridj)   
        useridj=open(ipath)
        userid = json.load(useridj)

        if not token in serverid.values():
          if user in serverid.values():
            del (serverid[f"{user}"])
          serverid.update({user:token})
          json.dump(serverid, open(f"{ipath2}{server[0]}.json","w"))     
      
        if not token in userid.values():
          if user in userid.values():
            del (userid[f"{user}"])
          userid.update({user:token})
          json.dump(userid, open(f"{ipath}","w"))
        
    except Exception as e:
        return f"<h1>エラー : {e}</h1>"

    return f"<h1>登録成功！ {name}さんよろしく！</h1>"

def run():
  app.run(debug=False,host="0.0.0.0")

def start():
  t = Thread(target=run)
  t.start()
