# -*- coding: utf-8 -*-
from tornado import database 
import time
import pymongo
from pymongo import Connection
from random import randrange
mongo = Connection('localhost:27017,localhost:27018,localhost:27019')['promise'] 
mysql = database.Connection(host='localhost',database='promise',user='root',password='123456')
 

def publish(db,e):
    e['uid'] = '%s'%(randrange(3)+1)
    params = [e['uid'],e['category'],e['title'],e['content'],e['created_at']] 
    sql = "INSERT INTO entries(uid,cid,title,content,created) VALUES(%s,%s,%s,%s,%s);"
    sql += "SET @last = LAST_INSERT_ID();" 
    for tag in e['tags']: params.append(tag)
    for tag in e['tags']:
        sql += "INSERT INTO tags(entry_id,name) VALUES(@last,%s);"   
        
    db.execute(sql,*params)

for e in mongo.threads.find():
    publish(mysql,e)


    