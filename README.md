# hcc

#### 目录介绍

1. metric_collecting: 收集原始数据，并提取出各项指标。子目录对应个人名字，没有的请另外添加。
2. metric_computing: 基于原始指标进行计算。
3. web_services: 提供外部restful访问接口、状态监控界面。

#### 开发规范

1. push前，须先pull(fetch+merge)同步远程服务器，合并后再push