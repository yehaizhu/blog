from flask import Blueprint

main = Blueprint('main', __name__)

import forms,views






# @main.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)
