#!/usr/bin/env python3
 
import datetime
from flask import Flask, render_template, request, Response,jsonify
from flask_kerberos import init_kerberos
from flask_kerberos import requires_authentication
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base,Post

import os

DEBUG=True

app = Flask(__name__)
#Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


@app.route('/')
@requires_authentication
def home(user):
	return jsonify({
        "user":user.split('@')[0]
    })


@app.route('/post',methods=["GET", "POST"])
@requires_authentication
def postHandle(user):
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        details = data.get('details')
        category = data.get('category')
        author = user.split('@')[0]
        date = data.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        post = Post(title=title, details=details, category=category, author=author,date=date)
        session = Session()
        session.add(post)
        session.commit()
        id = post.id
        session.close()
        return jsonify({
        	'id': id,
        	'title': post.title,
        	'details': post.details,
        	'category': post.category,
        	'author': post.author,
        	'date': post.date
    })
    else:
        session = Session()
        posts = session.query(Post).all()
        session.close()
        posts_list = []
        for post in posts:
            post_dict = {
        	    'id': post.id,
            	'title': post.title,
            	'details': post.details,
            	'category': post.category,
            	'author': post.author,
            	'date': post.date.isoformat()
        	}
            posts_list.append(post_dict)
        return jsonify({
        "posts" : posts_list
        })
                              
@app.route('/post/<int:post_id>', methods=['GET', 'DELETE'])
@requires_authentication
def post(user,post_id):
    # Get the post from the database
    session = Session()
    post = session.query(Post).filter_by(id=post_id).first()
    session.close()

    if not post:
        # Return a 404 error if the post doesn't exist
        return jsonify({'error': 'Post not found'}), 404

    if request.method == 'GET':
        # Return the post data as JSON
        return jsonify({
            'id': post_id,
            'title': post.title,
            'details': post.details,
            'category': post.category,
            'author': post.author,
            'date': post.date.isoformat()
        })

    elif request.method == 'DELETE':
        # Delete the post from the database
        session = Session()
        session.delete(post)
        session.commit()
        session.close()

        # Return a 204 status code to indicate success
        return '', 204

if __name__ == '__main__':
	init_kerberos(app,service='host',hostname='server.projet.tn')
	app.run(host='0.0.0.0',port=8080,debug=DEBUG)
