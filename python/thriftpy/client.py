# -*- coding: utf-8 -*-
#
#
# Author: Unescaped left brace in regex is deprecated, passed through in regex; marked by <-- HERE in m/%{ <-- HERE (.*?)}/ at /usr/bin/print line 528. Error: no such file "alex"
# Created Time: 2017年10月10日 星期二 17时11分39秒
import time
import thriftpy
pingpong_thrift = thriftpy.load("pingpong.thrift", module_name="pingpong_thrift")

from thriftpy.rpc import make_client

client = make_client(pingpong_thrift.PingPong, '127.0.0.1', 6000)

start = time.time()
for i in range(10000):
    client.ping()

print(time.time()-start)
