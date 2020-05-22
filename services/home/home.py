# from __main__ import app
from __main__ import api, config, dev_config, debug
from flask_restful import Resource
from flask import request
import json
import sqlite3


class home(Resource):
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.cur = self.conn.cursor()
        #Success Table
        self.cur.execute("""CREATE TABLE success(
                    status text,
                    success int,
                    data_key text,
                    data_value text,
                    return_code int)    
        """)
        self.cur.execute("INSERT INTO success VALUES ('DB success',1,'test','Heyyy.. Welcome',200)")
        #Failure Table
        self.cur.execute("""CREATE TABLE failure(
                    status text,
                    success int,
                    error_id NULL,
                    error_message NULL,
                    return_code int)    
        """)
        self.cur.execute("INSERT INTO failure VALUES ('failure',0,'','',500)")
        self.conn.commit()
        
    def get(self):
        self.cur.execute("SELECT * FROM success")
        success_row = self.cur.fetchall()[0]
        try:
            ret_obj = {
                "status" : success_row[0],
                "success" : bool(success_row[1]),
                "data" : {
                    success_row[2] : success_row[3]
                }
            }
            ret_satus = success_row[4]            
            return ret_obj, ret_satus

        except Exception as e:
            self.cur.execute("SELECT * FROM failure")
            failure_row = self.cur.fetchall()
            ret_obj = {
                "status" : failure_row[0],
                "success" : bool(failure_row[1]),
                "error" : {
                    "id" : failure_row[2],
                    "message" : str(e)
                }
            }
            
            #By default the status code is 200, so we need to return status code
            ret_status = failure_row[4]        
            return ret_obj, ret_status
        self.conn.close()

api.add_resource(home, '/', resource_class_kwargs={})
