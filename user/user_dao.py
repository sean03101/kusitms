from connection.mysql_connect import get_connection
import pymysql


#check the db and things that we need
def add_user(id, name):
    sql = '''insert into user (id, name, sign_date)
             values (%s, %s, NOW())'''
    
    sql1 = '''select last_insert_id()'''
     
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id, name))
        conn.commit()
        cursor.execute(sql1)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    return result[0]

def user_login(id):
    sql = '''select user_idx from user where id=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, id)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return False
        
    return result[0]


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
        
    if not result:
        return False
    
    data = {}
    data['id'] = result[0]
    data['name'] = result[1]
    
    return data

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
    
    if not result:
        return False
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['location'] = row[1]
        temp_dict['sell_yn'] = row[2]
        data_list.append(temp_dict)
    print(data_list)
    return data_list


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
        
    if not result:
        return False
    
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


def add_cart(user_idx, post_idx):
    sql = '''insert into cart (user_idx, post_idx)
             values (%s, %s)'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        conn.commit()
    finally:
        if conn is not None: conn.close()
    
    return 'OK'

def delete_cart(user_idx, post_idx):
    sql = '''delete from cart where user_idx=%s and post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        conn.commit()
    finally:
        if conn is not None: conn.close()
    
    return 'OK'

def check_post(post_idx):
    sql = '''select posts.post_idx, title, price, location
             from posts inner join post_file on posts.post_idx=post_file.post_idx
             where posts.post_idx=%s
             and file_idx in (select min(file_idx) from post_file group by post_idx)'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, post_idx)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return False
    
    data = {}
    data['post_idx'] = result[0]
    data['title'] = result[1]
    data['price'] = result[2]
    data['location'] = result[3]
    
    return data