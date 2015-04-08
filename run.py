#!flask/bin/python


from __future__ import with_statement
from contextlib import closing

# all the imports
import sqlite3
import json
from js import *
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from models import *

 
# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)



app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.before_request
def before_request():
    pass
 
@app.teardown_request
def teardown_request(exception):
    pass

@app.route('/')
@db_session
def show_entries():
    return render_template('index.html')

@app.route('/admin')
@db_session
def show_adminpan():
    return render_template('admin.html')

@app.route('/admin/brands')
@db_session
def edit_brands():
    brands = Brand.select().order_by(Brand.name)
    return render_template('brands.html', brands=brands)

@app.route('/admin/brands/<id>', methods=['GET', 'POST'])
@db_session
def edit_brand_name(id):
    brand = Brand[id]
    if request.method == 'POST':
        brand.name = request.form['name']
        brand.country = request.form['country']
    return render_template('edit_brand.html', brand=brand)

@app.route('/admin/brands/create', methods=['GET', 'POST'])
@db_session
def create_brand_name():
    if request.method == 'POST':
        brand = Brand(name=request.form['name'], country= request.form['country'])
        flush()
        url = url_for('edit_brands')
        return redirect(url)
    else:
        return render_template('create_brand.html')





@app.route('/admin/clients')
@db_session
def edit_clients():
    return render_template('clients.html')

@app.route('/admin/goods')
@db_session
def edit_goods():
    return render_template('goods.html')

@app.route('/contacts')
@db_session
def index():
    return render_template("contacts.html")

@app.route('/catalog')
@db_session
def get_categories():
    categories = Category.select().order_by(Category.name)
    return render_template('catalog.html', categories=categories)

@app.route('/catalog/<name>')
@db_session
def clothing(name):
    cat = Category.get(name=name)
    return render_template('clothing.html', cat=cat)


if __name__ == '__main__':



	app.run(host='0.0.0.0',debug = True)

