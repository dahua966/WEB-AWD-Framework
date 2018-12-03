## 注意事项
链接sqlite3时路径中不能有中文，所以该文件夹要放在英文目录下使用。

## 使用流程
- python dbinit.py 创建数据库
- 修改util.py中的参数
- python main.py
- 可在另一个窗口中sqlite3 flag.db3+select * from flag 查看数据库

## 交flag方式
curl 127.0.0.1:6666/flag/672f9407-27b4-4f48-a9f1-036db0438232
requests.get('http://127.0.0.1:6666/flag/672f9407-27b4-4f48-a9f1-036db0438232')
