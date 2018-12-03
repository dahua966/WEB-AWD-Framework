仅供web使用，注意ps aux 查看web服务是否是 /usr/sbin/apache2 -k start

若不是，请联系我修改

若是

1. 把这个文件改成777，放在web马能访问到的地方

2. 用你的web马执行该文件，不需要参数

3. 测试ls 等是否被杀掉

如何停止
1. touch /tmp/stop 暂停，删除则恢复
2. touch /tmp/kill 毁尸灭迹