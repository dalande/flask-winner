from flask import render_template

from . import index_blu


@index_blu.route('/index')
def hello():
    return render_template('index.html')

#
# @index_blu.route('/profile_page')
# def profile():
#     return render_template('profile_old.html')