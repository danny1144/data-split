# oracle环境配置

配一个ORACLE_HOME的环境变量，指向Instant Client的目录（如果你到这已经可以成功连接orcale数据库了，环境变量这一步不执行也可以，视情况而定）：

到自己想要放的路径下，我的是C:\instantclient-basic-win32-11.2.0.1.0\instantclient_11_2

然后是配置环境变量：右键计算机——属性——高级系统设置——环境变量——系统变量——新建

　　变量：ORACLE_HOME  值：Q:\OracleClient

　　变量：TNS_ADMIN       值：Q:\OracleClient

　　编辑path用';'隔开加一个  Q:\OracleClient

