#!flask/bin/python


from __future__ import with_statement
from contextlib import closing

# all the imports
import os

from werkzeug import *
import sqlite3
import json
from werkzeug.utils import secure_filename
from js import *
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

from models import *


# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
#Windos
#UPLOAD_FOLDER = 'C:\Users\comp-79\PycharmProjects\guap\uploads'
UPLOAD_FOLDER = 'static/Upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
    return render_template('/admin/brands.html', brands=brands)


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
        brand = Brand(name=request.form['name'], country=request.form['country'])
        flush()
        url = url_for('edit_brands')
        return redirect(url)
    else:
        return render_template('create_brand.html')


@app.route('/admin/brands/delete', methods=['POST'])
@db_session
def delete_brand_id():
    brand = Brand[request.form['id']]
    brand.delete()
    url = url_for('edit_brands')
    return redirect(url)


@app.route('/admin/clients')
@db_session
def edit_clients():
    return render_template('clients.html')


@app.route('/admin/clothing')
@db_session
def edit_goods():
    clothing = Clothing.select().order_by(Clothing.name)

    return render_template('/admin/clothing.html', clothing=clothing)


@app.route('/admin/clothing/create', methods=['GET', 'POST'])
@db_session
def create_clothing_name():
    if request.method == 'POST':
        # category = Category[request.form['Category']]
        # brand = Brand(name=request.form['name'], country= request.form['country'])
        file = request.files['File']
        #cat= Category[request.form['Category']]
        #rc = Category(name=request.form['Category'])
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #name,ext = os.path.splitext(savepath)
            savepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            name,ext = os.path.splitext(savepath)
            file.save(savepath)
            #image = Images(name=filename, type="pix", path=savepath, Clothing=request.form['name'])
            #return redirect(url_for('uploaded_file',
            #filename=filename))
        clothing = Clothing(name=request.form['name'], price=request.form['price'], category=request.form['Category'],
                            brand=request.form['Brand'])
        flush()
        image = Images(name=filename, type=ext, path=savepath, Clothing=clothing.id)
        flush()
        url = url_for('edit_goods')
        return redirect(url)
    else:
        brands = Brand.select().order_by(Brand.name)
        Categories = Category.select().order_by(Category.name)
        return render_template('/admin/create_clothing.html', brands=brands, categories=Categories)


@app.route('/contacts')
@db_session
def index():
    return render_template("contacts.html")

@app.route('/get_categories')
@db_session
def get_categories():
    categories = Category.select().order_by(Category.name)

    return to_json(db, categories, include=[Category.clothing, Category.clothing] )

@app.route('/catalog')
@db_session
def get_catalog():
    categories = Category.select().order_by(Category.name)
    return render_template('catalog.html', categories=categories)



@app.route('/catalog/<name>')
@db_session
def clothing(name):
    cat = Category.get(name=name)
    return render_template('clothing.html', cat=cat)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

