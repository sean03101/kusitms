from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os
from product import product_dao
from datetime import datetime

product_blue = Blueprint('product_blue', __name__)

#메인페이지 1차
@product_blue.route('/home')
def main_page():
    data_new = product_dao.post_list(0)
    data_like = product_dao.post_list(1)
    print(session)
    html = render_template('main.html', data_new=data_new, data_like=data_like)
    return html

#검색 get 얘기가 필요..
@product_blue.route('/search', methods=['get'])
def search_posts():
    html = render_template('/search_result') #검색 결과 페이지
    return html

#등록페이지 얘기가 필요..
@product_blue.route('/register')
def register_post():
    html = render_template('register.html')
    return html

#상품 업로드 틀   
@product_blue.route('/upload_post', methods=['post'])
def upload_post():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 1
    
    #title = request.form['title']
    title = 'title'
    description_tags = request.form['describe']
    price = request.form['price']
    category = request.form['category']
    size = request.form['size']
    brand = request.form['brand']
    gender = request.form['gender']
    certificate = request.form['isguarantee']
    receipt = request.form['isreceipt']
    post_file = request.files['file']
    img_count = 1

    post_dir = current_app.config['POST_FILE']
    
    print(description_tags)
    
    tags = ''
    if '#' in description_tags:
        text_list = description_tags.split(' ')

        for word in text_list:
            if '#' in word:
                tags += word[1:]+' '

    post_idx = product_dao.add_post(user_idx, title, description_tags, tags, price, category, size, brand, gender, certificate, receipt, img_count)
    
    f_name = datetime.now().strftime("%Y%m%d_")+'{post_idx}'.format(post_idx=post_idx)+secure_filename(post_file.filename)
    f_location = os.path.join(post_dir,f_name)
    post_file.save(f_location)
    product_dao.add_post_file(post_idx, 1, f_location)

    return 'OK'

#상품 삭제?

#상세페이지 컬럼 정해야
@product_blue.route('/post/post_id=<post_idx>', methods=['get'])
def post_detail(post_idx):
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    post_detail = product_dao.post_detail(post_idx)

    if post_detail['comment_count'] != 0:
        comments = product_dao.post_comment(post_idx)
        post_detail['comments'] = comments
        
    if product_dao.check_user_like(user_idx, post_idx):
        post_detail['user_like'] = 'Y'
    else:
        post_detail['user_like'] = 'N'
        
    if not product_dao.check_sub(user_idx, post_detail['user_idx']):
        post_detail['sub_yn'] = 'N'
    else:
        post_detail['sub_yn'] = 'Y'
            
    html = render_template('detail.html', data=post_detail)
    return html


@product_blue.route('/upload_comment', methods=['post'])
def upload_comment():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    post_idx = request.form['post_idx']
    comment_text = request.form['text']
    comment_count = request.form['count']
    
    product_dao.add_comment(post_idx, user_idx, comment_text)
    product_dao.update_comment_count(post_idx, int(comment_count)+1)
    
    return 'OK'
    
#코멘트 삭제? 사용안할수도 있음..
@product_blue.route('/delete_comment', methods=['post'])
def delete_comment():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        return 'NO'
    
    post_idx = request.form['post_idx']
    comment_idx = request.form['comment']
    
    product_dao.delete_comment(comment_idx)
    
    return 'OK'

#구독페이지 1차
@product_blue.route('/subscribe')
def subscribe_list():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    post_list = product_dao.sub_post_list(user_idx)
    
    if not post_list:
        html = render_template('subscribe.html', post_list=False)
        return html
    
    for post in post_list:
        if post['comment_count'] != 0:
            comments = product_dao.post_comment(post['post_idx'])
            post['comments'] = comments        
    html = render_template('subscribe.html', post_list=post_list)
    return html
 
#구독추가와 취소를 동시에? 같은버튼?
@product_blue.route('/subscription_update', methods=['post'])
def add_subscription():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    followed = request.form['user_idx'] #maybe get?
    
    checked_idx = product_dao.check_sub(user_idx, followed)
    
    if not checked_idx:
        product_dao.add_sub(user_idx, followed)
        return 'ADD'
    else:
        product_dao.delete_sub(user_idx, followed)
        return 'DEL'
    
    return 'OK'


#위시리스트페이지
@product_blue.route('/bookmark')
def wishlist():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
        
    data = product_dao.get_wishlist(user_idx)
    html = render_template('like.html', post_list=data)
    return html

#위시리스트 업데이트
@product_blue.route('/wishlist_update', methods=['post'])
def add_wishlist():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
        
    post_idx = request.form['post_idx']

    checked_idx = product_dao.check_wish(user_idx, post_idx)
    
    if not checked_idx:
        product_dao.add_wish(user_idx, post_idx)
        return 'ADD'
    else:
        product_dao.delete_wish(user_idx, post_idx)
        return 'DEL'
    
    return 'OK'