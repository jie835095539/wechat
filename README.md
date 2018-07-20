# wechat_auto

## Function list

1. 使用微信`文件助手`实现远程控制，在`文件助手`中输入`help`获取所有命令列表
2. 已经把自己删除的好友的名字定时保存在根目录`storage\deleted_friend`文件中，留待用户手工清理
3. 自动通过好友请求，打招呼信息保存在`wechat_auto.GREETING`变量中，为长度为3的一个数组
4. 定时给好友发送问候信息,信息内容当前为当日天气，根据好友自己设置的城市确定
5. 如果好友的备注是“例外”那么无论如何都不会自动AI回复

## Specification

根目录下必须有storage文件夹用来存放数据，
storage文件夹下须有city.json文件告诉组件需要提前请求哪些城市的天气情况
具体格式参考github上的模板

## New features

### 1

可以给制定群定时发送消息，消息内容在`/storage/joke`文件中读取，每条消息由'|'符号分割。
消息间隔时间在`wechat_auto.CHATROOM_SPAN`定义，默认为1小时，也就是3600秒。
群名称由`wechat_auto.CHATROOM_NAME`定义，默认是"哈哈哈哈哈哈哈"
`wechat_auto.SWITCH_CHATROOM`默认为False，也就是关闭定时群消息功能

### 2

添加新功能，可以在所有群聊有新人加入的时候自动@新人打招呼，并且可是设置过滤名称，符合过滤名称的群聊不会自动打招呼
过滤变量为`wechat_auto.FILTER_CHATROOM`
打招呼信息变量为`wechat_auto.MESSAGE_CHATRROM`

## Bug Fixed

改变了userid的获取方式，不会在调用图灵AI时出现userid错误的问题