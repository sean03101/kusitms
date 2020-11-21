from connection.mysql_connect import get_connection
import pymysql

def mypost_list(user_idx):
    sql = '''select posts.post_idx, location, sell_yn
             from posts inner join post_file on posts.post_idx = post_file.post_idx
             where file_idx in (select min(file_idx) from post_file group by post_idx) 
             and posts.user_idx=%s'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, user_idx)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['location'] = row[1]
        temp_dict['sell_yn'] = row[2]
        data_list.append(temp_dict)
    print(data_list)
    return data_list

#can change columns
def user_info(user_idx):
    sql = '''select id, name from user where user_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, user_idx)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    data = {}
    data['id'] = result[0]
    data['name'] = result[1]
    
    return data

def cart_list(user_idx):
    sql = '''select posts.post_idx, title, price, location
             from cart inner join posts on posts.post_idx = cart.post_idx
             inner join post_file on posts.post_idx = post_file.post_idx
             where file_idx in (select min(file_idx) from post_file group by post_idx)
             and cart.user_idx = %s'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, user_idx)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
        
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['title'] = row[1]
        temp_dict['price'] = row[2]
        temp_dict['location'] = row[3]
        data_list.append(temp_dict)
    print(data_list)
    return data_list