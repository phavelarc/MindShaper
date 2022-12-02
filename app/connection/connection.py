import MySQLdb
import json

def connection():
  dbconnect = MySQLdb.connect("localhost", "root", "", "sistema")
  return dbconnect