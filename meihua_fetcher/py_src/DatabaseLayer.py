#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

class DatabaseLayer:

    STORE_RESULT_MODE = 0
    USE_RESULT_MODE = 1
    
    isDryRun = False

    def connect(self, host="localhost", user="root", pwd="", db="", dbport=3306, autocommit=False):
        try:
            self.isConnect = False

            self.conn = mdb.connect(host, user, pwd, db, charset='utf8', port=dbport);

            self.isConnect = True

            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT VERSION ()")

            data = self.cursor.fetchone()

            if autocommit:
                self.conn.autocommit(True)
            else:
                self.conn.autocommit(False)

        except mdb.Error as e:
            print("Connect Error % d: % s" % (e.args[0], e.args[1]))

        print("Database version : % s " %  data)


    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except mdb.Error as e:
            print("Close Error % d: % s" % (e.args[0], e.args[1]))


    # Execute and commit. No need to rollback.
    def excute(self, sql = "", many = False, commit = True):
        if self.isDryRun:
            print("DRY RUN SQL: ", sql)
            return True
          
        try:
            if many:
                self.cursor.executemany(sql)
            else:
                self.cursor.execute(sql)

            if commit:
                self.conn.commit()
                
        except mdb.Error as e:
            print("Excute Error % d: % s" % (e.args[0], e.args[1]))
            print("Excute sql= % s" %  sql)
            self.conn.rollback()
            return False
        except Exception as e:
            print("Excute Error: ", e)
            print("Excute sql= % s" % sql)
            self.conn.rollback()
            return False
          
        return True


    def getRows(self, sql, many = False):
        try:
            self.excute(sql)
            if many:
                rows = self.cursor.fetchall()
            else:
                rows = self.cursor.fetchone()
                
            return rows
        except mdb.Error as e:
            print("getRows Error % d: % s" % (e.args[0], e.args[1]))   


    def query(self, sqltext, mode = STORE_RESULT_MODE):
        """
                作用：使用connection对象的query方法，并返回一个元组(影响行数(int),结果集(result))
                参数：sqltext：sql语句
                     mode=STORE_RESULT_MODE（0） 表示返回store_result，mode=USESTORE_RESULT_MODE（1） 表示返回use_result
                返回：元组(影响行数(int),结果集(result)
        """
        if self.conn == None or self.conn.open == False:
            return -1
        self.conn.query(sqltext)
        if mode == 0 :
            result = self.conn.store_result() 
        elif mode == 1 :
            result = self.conn.use_result()
        else :
            raise Exception("mode value is wrong.")
        return (self.conn.affected_rows(),result)


    def fetchQueryResult(self,result,maxrows=1,how=0,moreinfo=False):
        """
                参数:result： query后的结果集合
                    maxrows： 返回的最大行数
                    how： 以何种方式存储结果
                     (0：tuple,1：dictionaries with columnname,2：dictionaries with table.columnname)
                    moreinfo 表示是否获取更多额外信息（num_fields，num_rows,num_fields）
                返回：元组（数据集，附加信息（当moreinfo=False）或单一数据集（当moreinfo=True）
        """
        if result == None : return None
        dataset =  result.fetch_row(maxrows,how)
        if moreinfo is False :
            return dataset
        else :
            num_fields = result.num_fields()
            num_rows = result.num_rows()
            field_flags = result.field_flags()
            info = (num_fields,num_rows,field_flags)
            return (dataset,info)


    def selectDB(self, dbName):
        self.conn.select_db(dbName)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def setautocommit(self, auto=False):
        self.conn.autocommit(auto)

    def isConnected(self):
        return self.isConnect

    def setDryRun(self, isDryRun):
        # TODO: this flag is not in place
        self.isDryRun = isDryRun