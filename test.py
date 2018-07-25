import time
import threading
import wechat_auto

wechat_auto.CHATROOM_NAME_MESSAGE = ["测试"]
wechat_auto.CHATROOM_NAME_AUTOFUNNY = ["测试"]
wechat_auto.CHATROOM_SPAN = 30
wechat_auto.AUTOFUNNY_SPAN = 20
wechat_auto.SWITCH_MESSAGE = True
wechat_auto.SWITCH_AUTOFUNNY = True
wechat_auto.run(True)