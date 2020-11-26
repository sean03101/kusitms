from connection.mysql_connect import get_connection
import pymysql


#check the db and things that we need
def add_user(user_id, user_name, user_email, user_img):
    sql = '''insert into user (id, name, email, user_img, sign_date)
             values (%s, %s, %s, %s, NOW())'''
    
    sql1 = '''select last_insert_id()'''
     
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, user_name, user_email, user_img))
        conn.commit()
        cursor.execute(sql1)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    return result[0]

def check_user(user_id):
    sql = '''select * from user where id=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, user_id)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return False
    return True

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
    sql = '''select id, name, email, user_img from user where user_idx=%s'''
    
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
    data['email'] = result[2]
    data['img'] = result[3]
    
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

def likepost_list(user_idx):
    sql = '''select like_idx, posts.post_idx, location
             from like_posts inner join posts on posts.post_idx=like_posts.post_idx
             inner join post_file on posts.post_idx=post_file.post_idx
             where file_idx in (select min(file_idx) from post_file group by post_idx)
             and like_posts.user_idx=%s'''
             
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
        temp_dict['like_idx'] = row[0]
        temp_dict['post_idx'] = row[1]
        temp_dict['location'] = row[2]
        data_list.append(temp_dict)
    
    return data_list

def check_like(user_idx, post_idx):
    sql = '''select like_idx from like_posts
             where user_idx=%s and post_idx=%s'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    if not result:
        return False
    
    return result[0]

def count_like(post_idx):
    sql = '''select post_like from posts where post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, post_idx)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return 0
    
    return result[0]

def update_like_count(post_idx, like_count):
    sql = '''update posts set post_like=%s where post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (like_count, post_idx))
        conn.commit()
    finally:
        if conn is not None: conn.close()
        
    return 'OK'

def add_like(user_idx, post_idx):
    sql = '''insert into like_posts (user_idx, post_idx, datetime)
             values (%s, %s, NOW())'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        conn.commit()
    finally:
        if conn is not None: conn.close()
    
    return 'OK'

def delete_like(user_idx, post_idx):
    sql = '''delete from like_posts where user_idx=%s and post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, post_idx))
        conn.commit()
    finally:
        if conn is not None: conn.close()
        
    return 'OK'

def cart_list(user_idx):
    sql = '''select posts.post_idx, user.user_idx, email, title, price, location
             from cart inner join posts on posts.post_idx = cart.post_idx
             inner join post_file on posts.post_idx = post_file.post_idx
             inner join user on posts.user_idx = user.user_idx
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
        temp_dict['uesr_idx'] = row[1]
        temp_dict['user_email'] = row[2]
        temp_dict['title'] = row[3]
        temp_dict['price'] = row[4]
        temp_dict['location'] = row[5]
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

def pay_list(user_idx):
    sql = '''select posts.post_idx, user.user_idx, email, title, price, location
             from cart inner join posts on posts.post_idx = cart.post_idx
             inner join post_file on posts.post_idx = post_file.post_idx
             inner join user on posts.user_idx = user.user_idx
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
        temp_dict['uesr_idx'] = row[1]
        temp_dict['user_email'] = row[2]
        temp_dict['title'] = row[3]
        temp_dict['price'] = row[4]
        temp_dict['location'] = row[5]
        data_list.append(temp_dict)
    print(data_list)
    return data_list