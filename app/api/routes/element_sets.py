from flask import (Blueprint, render_template, request)


elements = Blueprint('elements', __name__, url_prefix='/<login>/', template_folder='app/templates')


@elements.route('/tools')
def tools():
  '''
  Страница со всеми инструментами
  '''
  return "Страница со всеми инструментами"


@elements.route('/constructions')
def construction():
  '''
  Страница с объектами
  '''
  return "Страница с объектами"


@elements.route('/workers')
def workers():
  '''
  Страница с инструментами
  '''
  return "Страница с инструментами"