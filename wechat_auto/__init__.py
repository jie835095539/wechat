import itchat
from itchat.content import *
import json
import time
import threading
import os
from .components import AI
from .components import weather

list_friends = []
switch_AI = True

'''
#全部消息
@itchat.msg_register(INCOME_MSG)
def text_reply(msg):
    print(msg)
    return 'Hello'
'''

'''
#文本消息
@itchat.msg_register(TEXT)
def msg_system(msg):
    global switch_AI
    #通过文件助手控制是否开启AI自动回复
    if msg['ToUserName'] == 'filehelper':
        if msg['Text'] == 'start':
            switch_AI = True
            itchat.send('AI started', toUserName='filehelper')
        if msg['Text'] == 'stop':
            switch_AI = False
            itchat.send('AI stoped', toUserName='filehelper')
        return
    #备注为AI的用户自动使用AI回复
    if msg['User']['RemarkName'] == 'AI' and switch_AI==True:
        return AI.get_msg(msg['Text'])
'''
'''
#系统消息
#UNDO, 删除好友用户记录到本地文档，定期清理好友
@itchat.msg_register(NOTE)
def msg_system(msg):
    print(msg)

#新好友请求
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    print(msg)
    #延时接受好友请求
    #time.sleep(10)
    itchat.add_friend(**msg['Text'])# 该操作将自动将好友的消息录入，不需要重载通讯录
    #UNDO 新好友的打招呼信息,延迟后发送公众号信息
    itchat.send_msg('Nice to meet you!',msg['RecommendInfo']['UserName'])
'''
#群发问候 子线程
def batch_message(list_friends, weathers):
    #读取好友地址，调用接口定时发送天气预报

    while True:
        if time.localtime(time.time())[3]==23 and time.localtime(time.time())[4]==28:
            for friend in list_friends:
                if friend['RemarkName'] == '毛诗茹' or friend['NickName']=='毛诗茹':
                    print("YES")
                    weather_brief = _get_location_weather(friend, weathers)
                    itchat.send('@msg@'+weather_brief,friend.UserName)
            time.sleep(60)

def _get_location_weather(friend, weathers):
    if friend['City'] in weathers:
        return  weathers[friend['City']]
    if friend['Province'] in weathers:
        return  weathers[friend['Province']]
    if '北京' in weathers:
        return  weathers['北京']
    return "现在是23:28"


def run():
    
    global list_friends
    itchat.auto_login(hotReload=True)
    #获取天气
    weather.init()
    #获取好友
    list_friends = itchat.get_friends(update=True)
    #开启定时问候任务
    timing_task = threading.Thread(target=batch_message,args=(list_friends,weather.CITYS_WEATHER))
    timing_task.start()
    #with open('friends.json','w',encoding='utf-8') as f:
    #    f.write(json.dumps(list_friends,ensure_ascii=False))
    #print(len(result))
    itchat.run()
    