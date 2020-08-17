'''
Created on 2020年6月10日
@author: Dannyz
'''
import cx_Oracle
import psycopg2
oracleConfig = {
    "userName": '10.192.30.136',
    "password": 'DPP_CRP',
    "host": 'DPP_CRP',
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
    oraDb = Oracle(**oracleConfig)

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
    # mySensor = getOracleMap()
    sql1 = "SELECT p.pointexp from trendwarning_modepoints p  where p.pointtype=1 and  p.pointexp not in (SELECT s.siecode from da_config_sensor s) GROUP BY p.pointexp "

    sql3 = """INSERT INTO "public"."da_config_sensor"("siecode", "connector_id", "tag", "app_id", 
    "status", "description", "unit", "from_regist") VALUES (%(siecode)s,
     1004, 'W1.UNIT_HUIXIE.'%(siecode)s, 1000, 1, '离线导入', NULL, NULL);"""

    sql4 = """INSERT INTO "public"."da_config_connector_sensor"(  "tag", "status", "unit", 
    "connector_info", "connector_id", "from_regist", "da_prefix", "hda_prefix", "description") 
    VALUES (  'W1.UNIT_HUIXIE.'%(siecode)s, 1, NULL,
     'TIME_SERIES_DATA#REAL_TIME_AND_ARCHIVED#OPENPLANT#OPENPLANTSDK_LINUX#10.192.30.173#8200#W1#', 1004, 1, NULL, NULL, NULL);
    """

    pgDb = Pgsql10(**pgsqlConfig)
    listSensor = pgDb.queryAll(sql1)
    print(listSensor)
    for item in listSensor:
        pgDb.updateBy(sql3, {"siecode": item[0]})
        pgDb.updateBy(sql4, {"siecode": item[0]})
