from flask import Blueprint, render_template
from config import Config

OPENAI_API_KEY = Config.OPENAI_API_KEY

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/hello')
def hello_template():
    return render_template('hello.html', name=OPENAI_API_KEY)
