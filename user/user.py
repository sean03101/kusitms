from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os

user_blue = Blueprint('user_blue', __name__)

#login page
@user_blue.route('/login')
def login():
    html = render_template('/login.html')
    return html

#join post
@user_blue.route('/user_join_pro', methods=['post'])
def user_join():
    return 'OK'

#login post
@user_blue.route('/user_login_pro', methods=['post'])
def user_login():
    return 'OK'

#logout post if not?
@user_blue.route('/user_logout_pro', methods=['post'])
def user_logout():
    return 'OK'

#mypage, 다른사람 페이지 접근 시 고려해야함
@user_blue.route('/mypage')
def mypage():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 1
    
    user = user_dao.user_info(user_idx)
    post_list = user_dao.mypost_list(user_idx)

    #html = render_template('mypage.html', user=user, post_list=post_list) #유저정보, 유저 포스트 정보, 판매유무 등
    return post_list[0]
    
#장바구니
@user_blue.route('/cart')
def shopping_cart():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    cart_list = user_dao.cart_list(user_idx)
    html = render_template('shoppingcart.html', cart_list=cart_list) #장바구니 리스트 및 정보
    return html


#좋아요페이지

#결제페이지