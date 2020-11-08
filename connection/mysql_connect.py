import pymysql
from . import mysql_info

login = mysql_info.info

def get_connection() :
    conn = pymysql.connect(host=login['host'], user=login['user'],
            password=login['password'], db=login['db'], charset=login['charset'])

    return conn