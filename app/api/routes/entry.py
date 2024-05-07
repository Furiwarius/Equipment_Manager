from flask import (Blueprint, render_template, request)

entry = Blueprint('entry', __name__, url_prefix='/', template_folder='app/templates')

# Главная страница
@entry.route('/index')
@entry.route('/')
def home_page():
  '''
  Домашнаяя страница
  '''
  return "It is index page"


@entry.route('/registration')
def registration():
  '''
  Страница регистрации
  '''
  return "Страница регистрации"


@entry.route('/authorization')
def authorization():
  '''
  Страница авторизации
  '''
  return "Страница авторизации"


@entry.route('/<login>')
def private_office():
  '''
  Личный кабинет пользователя
  '''
  return "Страница пользователя"