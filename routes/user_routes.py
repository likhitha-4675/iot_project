from flask import Blueprint, request, session, redirect
from models import user_models

user_router = Blueprint('user_router', __name__)

@user_router.route('/')
def home():
    return redirect('/user_register')

@user_router.route('/user_register', methods=['GET', 'POST'])
def user_register():
    return user_models.user_register_route(request, session)

@user_router.route('/enter_otp', methods=['GET', 'POST'])
def enter_otp():
    return user_models.enter_otp_route(request, session)

@user_router.route('/user_dashboard')
def user_dashboard():
    return user_models.user_dashboard_route(session)

@user_router.route('/logout')
def logout():
    return user_models.logout_route(session)
