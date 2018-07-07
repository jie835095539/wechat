import itchat
import json

@itchat.msg_register(itchat.content.PICTURE)
def text_reply(msg):
    print(msg.FileName)
    return 'Hello'

itchat.auto_login(hotReload=True)
result = itchat.get_friends()

#with open('friends.json','w',encoding='utf-8') as f:
#    f.write(json.dumps(result,ensure_ascii=False))
print(len(result))
#itchat.run()
