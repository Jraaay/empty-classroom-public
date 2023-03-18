# 空教室查询 - 后端

## 基于

- Sanic

## 介绍

先从微教务获取今日空教室，再加上课表中的课程安排，返回当天的空教室

其中课表通过 `xls2json.py` 转换为 json 格式保存在 classTable 中

需要先登录一次微教务，抓包获取加密后的密码，填写入 `get_classroom.py` 的 `userNo` 和 `encoded_pwd`

程序运行在 8856 端口，需要反向代理至前端的 /api 路径

在 `main.py` 同目录创建 `version.json` 来保存当前最新版本信息，用于提示用户更新

在 `main.py` 同目录创建 `notification.json` 来保存需要向前端发出的通知

## 运行

```shell
python main.py
```
