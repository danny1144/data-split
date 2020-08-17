# ecoding=utf-8
import cx_Oracle
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('properties.conf', encoding="UTF-8")
lists_header = config.sections()  # 配置组名
oracleConfig = {
    "userName": 'DPP_CRP',
    "password": 'DPP_CRP',
    "host": '10.192.30.136',
    "instance": 'orcl',
}
pgsqlConfig = {
    "db": 'pgsql',
    "host": '10.192.30.103',
    "user": 'pgsql',
    "pw": 'Dpp-pgsql123##',
    "port": '5432'
}


class Oracle(object):
    """  oracle db operator  """
    def __init__(self, userName, password, host, instance):
        self._conn = cx_Oracle.connect("%s/%s@%s/%s" %
                                       (userName, password, host, instance))
        self.cursor = self._conn.cursor()
        print('connect successful!')

    def queryTitle(self, sql, nameParams={}):
        if len(nameParams) > 0:
            self.cursor.execute(sql, nameParams)
        else:
            self.cursor.execute(sql)

        colNames = []
        for i in range(0, len(self.cursor.description)):
            colNames.append(self.cursor.description[i][0])

        return colNames

    # query methods
    def queryAll(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def queryOne(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def queryBy(self, sql, nameParams={}):
        if len(nameParams) > 0:
            self.cursor.execute(sql, nameParams)
        else:
            self.cursor.execute(sql)

        return self.cursor.fetchall()

    def insertBatch(self, sql, nameParams=[]):
        """batch insert much rows one time,use location parameter"""
        self.cursor.prepare(sql)
        self.cursor.executemany(None, nameParams)
        self.commit()

    def commit(self):
        self._conn.commit()

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()

        if hasattr(self, '_conn'):
            self._conn.close()


class Pgsql10(object):
    def __init__(self, db, host, user, pw, port):
        self._conn = psycopg2.connect(database=db,
                                      user=user,
                                      password=pw,
                                      host=host,
                                      port=port)
        self.cursor = self._conn.cursor()
        print('connect successful!')

    # query methods
    def queryAll(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def updateBy(self, sql, nameParams={}):
        if len(nameParams) > 0:
            self.cursor.execute(sql, nameParams)
            self._conn.commit()
            return
        else:
            self.cursor.execute(sql)

    def queryOne(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()


def getOracleMap():
    # sql = """select user_name,user_real_name,to_char(create_date,'yyyy-mm-dd') create_date from sys_user where id = '10000' """
    sql = """select ID,DESCRIPTION from SENSOR   """
    oraDb = Oracle(userName=oracleConfig["userName"],
                   password=oracleConfig['password'],
                   host=oracleConfig['host'],
                   instance=oracleConfig['instance'])

    # fields = oraDb.queryTitle(sql, {'id': 'CRP_NJHX_0300_04_030503003302'})
    # print(fields)
    listSensor = oraDb.queryAll(sql)
    #print(listSensor)
    mapSenser = dict(listSensor)
    return mapSenser


# def test2():
#     oraDb = Oracle('test', 'java', '192.168.0.192', 'orcl')
#     cursor = oraDb.cursor

#     create_table = """
#     CREATE TABLE python_modules (
#     module_name VARCHAR2(50) NOT NULL,
#     file_path VARCHAR2(300) NOT NULL
#     )
#     """
#     from sys import modules

#     cursor.execute(create_table)
#     M = []
#     for m_name, m_info in modules.items():
#         try:
#             M.append((m_name, m_info.__file__))
#         except AttributeError:
#             pass

#     sql = "INSERT INTO python_modules(module_name, file_path) VALUES (:1, :2)"
#     oraDb.insertBatch(sql, M)

#     cursor.execute("SELECT COUNT(*) FROM python_modules")
#     print(cursor.fetchone())
#     print('insert batch ok.')

#     cursor.execute("DROP TABLE python_modules PURGE")

if __name__ == '__main__':
    # 获取待更新的数据源map
    mySensor = getOracleMap()
    sql1 = "select siecode,description from  da_config_sensor where description='离线导入'"
    sql2 = 'update da_config_sensor set description=%(description)s where siecode=%(siecode)s'
    pgDb = Pgsql10(**pgsqlConfig)
    listSensor = pgDb.queryAll(sql1)
    print(listSensor)
    for item in listSensor:
        if item[0] in mySensor:
            pgDb.updateBy(sql2, {
                "description": mySensor[item[0]],
                "siecode": item[0]
            })
            del mySensor[item[0]]
        if item[0].replace('CRP_TP_', 'CRP_') in mySensor:
            pgDb.updateBy(
                sql2, {
                    "description": mySensor[item[0].replace('CRP_TP_',
                                                            'CRP_')],
                    "siecode": item[0]
                })
