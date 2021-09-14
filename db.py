
import pymysql
from pymysql import MySQLError

import tools

DB_HOST = "10.0.100.138"
PORT = 3306
PASSWORD = '123456'


class DBClient:
    def __init__(self):
        self.db = pymysql.connect(DB_HOST, port=PORT, database="batchquery", user="batchquery", password=PASSWORD)

    def __del__(self):
        try:
            self.db.close()
        except MySQLError:
            self.log.exception('DBClient __del__ close db exception')

    def newCursor(self):
        return self.db.cursor()

    def safeCloseCursor(self, cursor):
        try:
            cursor.close()
        except MySQLError:
            self.log.exception('safeCloseCursor error')

    def safeCloseDb(self):
        try:
            self.db.close()
        except MySQLError:
            self.log.exception('db safeCloseDb exception')

    def queryaal(self, oid):
        cursor = self.db.cursor()
        sql = f"select * from brand_info where `aal_id`='{oid}'"
        try:
            # 执行sql语句
            ret = cursor.execute(sql)
            if ret > 0:
                return cursor.fetchone()
            return None
        except Exception:
            print(sql)
            return None
        finally:
            self.safeCloseCursor(cursor)

    def insertBrand(self, name, aal_id):
        cursor = self.db.cursor()
        md5id = tools.md5(name)
        sql = f"insert into brand_info (`id_md5`,`name`, `aal_id`) values ('{md5id}', '{pymysql.escape_string(name)}', '{pymysql.escape_string(aal_id)}')"
        try:

            # 执行sql语句
            ret = cursor.execute(sql)
            if ret > 0:
                self.db.commit()
                return True
            return False
        except Exception as e:
            print(e)
            return False
        finally:
            self.safeCloseCursor(cursor)



if __name__ == "__main__":
    db = DBClient()
    count = db.queryCount("130680993a4a6d4a953ff8c133960947")
    print(count, type(count))
    print(db.delCount("130680993a4a6d4a953ff8c133960947"))
    print(db.queryCount("130680993a4a6d4a953ff8c133960947"))

    # 增加次数
    db.addCount("130680993a4a6d4a953ff8c133960947", 10)