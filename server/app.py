#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User, ArticlesSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class IndexArticle(Resource):
    
    def get(self):
        articles = [ArticlesSchema().dump(article) for article in Article.query.all()]
        return articles, 200

class ShowArticle(Resource):

    def get(self, id):
        session['page_views'] = 0 if not session.get('page_views') else session.get('page_views')
        session['page_views'] += 1

        if session['page_views'] <= 3:

            article = Article.query.filter(Article.id == id).first()
            article_json = ArticlesSchema.dump(article)

            return make_response(article_json, 200)

        return {'message': 'Maximum pageview limit reached'}, 401

class Login(Resource):
    """Log a user in by username and remember them in the session cookie."""

    def post(self):
        # Read the username from the JSON body of the request
        username = (request.get_json() or {}).get('username')

        # Usernames are unique, so we can look the user up directly
        user = User.query.filter(User.username == username).first()

        # Challenge: respond sensibly when no user matches the username
        if not user:
            return {'error': 'User not found'}, 404

        # Store the user's id in the session; Flask signs it into a cookie
        session['user_id'] = user.id

        return UserSchema().dump(user), 200

class Logout(Resource):
    """Log the current user out by clearing their id from the session."""

    def delete(self):
        session['user_id'] = None

        return {}, 204

class CheckSession(Resource):
    """Return the logged-in user, so the login survives a page refresh."""

    def get(self):
        user_id = session.get('user_id')

        # A missing or cleared user_id means nobody is logged in
        if not user_id:
            return {}, 401

        user = User.query.filter(User.id == user_id).first()

        # The session may point at a user that no longer exists
        if not user:
            return {}, 401

        return UserSchema().dump(user), 200

api.add_resource(ClearSession, '/clear')
api.add_resource(IndexArticle, '/articles')
api.add_resource(ShowArticle, '/articles/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
