from user import user_dao
from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
from werkzeug.utils import secure_filename
import datetime
import os

user_blue = Blueprint('user_blue', __name__)

#login page
@user_blue.route('/login')
def login():
    if 'user_idx' in session:
        return redirect('/home')
    html = render_template('/login.html')
    return html

#login post
@user_blue.route('/user_login_pro', methods=['post'])
def user_login():
    user_id = request.form['User_Id']
    user_name = request.form['User_Name']
    user_email = request.form['User_Email']
    user_img = request.form['User_Image_URL']
    
    if not user_dao.check_user(user_id):
        user_dao.add_user(user_id, user_name, user_email, user_img)
    
    user_idx = user_dao.user_login(user_id)
    
    if not user_idx:
        return 'NO'
    
    session['user_idx'] = user_idx
    session['login'] = 1
    
    print(user_idx)
    return 'OK'

#logout post if not?
@user_blue.route('/user_logout_pro')
def user_logout():
    session.clear()
    return 'OK'

#좋아요 업데이트
@user_blue.route('/like_update', methods=['post'])
def add_likepost():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    post_idx = request.form['post_idx']
    
    checked_idx = user_dao.check_like(user_idx, post_idx)
    
    result = {}
    
    if not checked_idx:
        user_dao.add_like(user_idx, post_idx)
        liked = user_dao.count_like(post_idx)
        user_dao.update_like_count(post_idx, liked+1)
        result['type'] = 'ADD'
        result['count'] = liked+1
        return result
    else:
        user_dao.delete_like(user_idx, post_idx)
        liked = user_dao.count_like(post_idx)
        user_dao.update_like_count(post_idx, liked-1)
        result['type'] = 'DEL'
        result['count'] = liked-1
        return result
    
    return result

#mypage, 다른사람 페이지 접근 시 고려해야함, 좋아요리스트?
@user_blue.route('/mypage')
def mypage():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 1
    
    user = user_dao.user_info(user_idx)
    mypost_list = user_dao.mypost_list(user_idx)
    likepost_list = user_dao.likepost_list(user_idx)

    html = render_template('mypage.html', user=user, post_list=mypost_list, like_list=likepost_list) #유저정보, 유저 포스트 정보, 판매유무 등
    return html
    
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

#장바구니 추가
@user_blue.route('/add_cart_pro')
def add_cart():
    user_idx = session['user_idx']
    post_idx = request.form['post_idx']
    
    user_dao.add_cart(user_idx, post_idx)
    
    return 'OK'

#장바구니 삭제
@user_blue.route('/delete_cart_pro')
def delete_cart():
    user_idx = session['user_idx']
    post_idx = request.form['post']
    
    user_dao.delete_cart(user_idx, post_idx)
    
    return 'OK'

#결제페이지 미완성!!
@user_blue.route('/payment')
def check_payment():
    if 'user_idx' in session:
        user_idx = session['user_idx']
    else:
        user_idx = 2
    
    data_list = user_dao.pay_list(user_idx)
    
    html = render_template('paycomplete.html', data_list=data_list)
    return html
        
