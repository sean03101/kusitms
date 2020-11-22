from connection.mysql_connect import get_connection
import pymysql


#input column 수정
def add_post(user_idx, title):
    sql = '''insert into posts(user_idx, title, written_time)
             values(%s, %s, now())'''
    
    sql1 = '''select last_insert_id()'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_idx, title))
        conn.commit()
        cursor.execute(sql1)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
        
    return result[0]


def add_post_file(post_idx):
    sql = '''insert into post_file(post_idx, file_type, location)
             values (%s, %s, %s)'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (post_idx, file_type, location))
        conn.commit
    finally:
        if conn is not None: conn.close()
    
    return 'OK'


#order by need, dict
def post_list(order_type):
    sql = '''select posts.post_idx, posts.user_idx, post_like, location
            from posts inner join post_file on posts.post_idx=post_file.post_idx
            where file_idx in (select min(file_idx) from post_file group by post_idx)'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if order_type == 0:
            sql += ' order by posts.post_idx desc'
            cursor.execute(sql)
        else:
            sql += ' order by post_like desc'
            cursor.execute(sql)
        
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return False
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['user_idx'] = row[1]
        temp_dict['post_like'] = row[2]
        temp_dict['img_url'] = row[3]
        data_list.append(temp_dict)
    print(data_list)
    return data_list

#dict
def post_detail(post_idx):
    sql = '''select * from posts where post_idx=%s'''
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, post_idx)
        result = cursor.fetchone()
    finally:
        if conn is not None: conn.close()
    
    return result

def sub_post(user_idx):
    sql = '''select posts.post_idx, posts.user_idx, title, description, tags, post_like, location, comment_count 
             from posts inner join post_file on posts.post_idx=post_file.post_idx
             where posts.user_idx in (select followed from user_follow where following=%s)
             and file_idx in (select min(file_idx) from post_file group by post_idx)'''
             
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
        temp_dict['user_idx'] = row[1]
        temp_dict['title'] = row[2]
        temp_dict['description'] = row[3]
        temp_dict['tags'] = row[4]
        temp_dict['post_like'] = row[5]
        temp_dict['img_url'] = row[6]
        temp_dict['comment_count'] = row[7]
        data_list.append(temp_dict)    
    print(data_list)
    return data_list    
        
def post_comment(post_idx):
    sql = '''select post_idx, user_idx, text from comment
             where post_idx=%s order by comment_idx'''
             
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, post_idx)
        result = cursor.fetchall()
    finally:
        if conn is not None: conn.close()
    
    if not result:
        return False
    
    data_list = []
    for row in result:
        temp_dict = {}
        temp_dict['post_idx'] = row[0]
        temp_dict['user_idx'] = row[1]
        temp_dict['text'] = row[2]
        data_list.append(temp_dict)    
    print(data_list)
    return data_list


#test, not in notion to
def get_wishlist(user_idx):
    sql = '''select posts.post_idx, posts.user_idx, title, description, tags, post_like, location, comment_count 
             from posts inner join post_file on posts.post_idx=post_file.post_idx
             where posts.post_idx in (select post_idx from wishlist where user_idx=%s)
             and file_idx in (select min(file_idx) from post_file group by post_idx)'''

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
        temp_dict['user_idx'] = row[1]
        temp_dict['title'] = row[2]
        temp_dict['description'] = row[3]
        temp_dict['tags'] = row[4]
        temp_dict['post_like'] = row[5]
        temp_dict['img_url'] = row[6]
        temp_dict['comment_count'] = row[7]
        data_list.append(temp_dict)    
    print(data_list)
    return data_list  