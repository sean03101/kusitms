from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os
from product import product_dao

product_blue = Blueprint('product_blue', __name__)

#메인페이지 1차
@product_blue.route('/')
def main_page():
    data_new = product_dao.post_list(0)
    data_like = product_dao.post_list(1)
    
    html = render_template('main.html', data_new=data_new, data_like=data_like)
    return html

#검색페이지get

#등록페이지
@product_blue.route('/post')
def register_post():
    html = render_template('register.html') #필요한거 없을듯..? user 정보?

#상품 업로드    
@product_blue.route('/upload_post', methods=['post'])
def upload_post():
    
    return 'OK'


#상세페이지
@product_blue.route('/post/post_id=<post_idx>', methods=['get'])
def post_detail(post_idx):
    detail = product_dao.post_detail(post_idx)
    html = render_template('', data=data)
    return html


#구독페이지 1차
@product_blue.route('/subscribe')
def subscribe_list():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    post_list = product_dao.sub_post(user_idx)
    for post in post_list:
        if post['comment_count'] != 0:
            comments = product_dao.post_comment(post['post_idx'])
            post['comments'] = comments        
    html = render_template('subscribe.html', post_list=post_list) #user, 구독 리스트(이미지 등), 좋아요, 댓글 등
    return html
 
#구독추가

#구독취소

#위시리스트페이지

#위시리스트추가

#위시리스트취소