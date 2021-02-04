from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from marshmallow import Schema, fields as mafields, post_load
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///langs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)


class TheLanguage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(40))
    framework = db.Column(db.String(40))

    def __init__(self, id, language, framework):
        self.id = id
        self.language = language
        self.framework = framework

    def __repr__(self):
        return 'id:{}   {} is the language. {} is the framework.'.format(self.id, self.language, self.framework)


class LanguageSchema(Schema):
    id = mafields.Integer()
    language = mafields.String()
    framework = mafields.String()

    @post_load
    def create_language(self, data, **kwargs):
        return Language(**data)

###############################################################################


authorizations = {
    'apikey': {
        'type': 'apikey',
        'in': 'header',
        'name': 'X-API-KEY'
        }
}


api = Api(app, authorization=authorizations, version='1.0', title='Data API', description='A simple Data Storing API',)
ns = api.namespace('language', description='CRUD operations')
a_language = api.model('Language', {'language': fields.String("the language."), 'framework': fields.String("The framework")})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message': 'Token is missing'}, 401

        if token != 'token':
            return {'message': 'Your token is wrong!!!'}, 401

        print('Token: {}'.format(token))
        return f(*args, ** kwargs)

    return decorated


languages = []
# python = {'language': 'python', 'id': 1}
python = TheLanguage(id=1, language='python', framework='Flask')
checkpoint = True
if not checkpoint:
    languages.append(python)
    db.session.add(python)
    db.session.commit()


class Work:
    @property
    def get_all(self):
        all_users = TheLanguage.query.all()
        schema = LanguageSchema(many=True)
        # print(languages)
        return schema.dump(all_users)

    def new(self, data):
        schema = LanguageSchema()
        new_language = schema.load(data)
        print(new_language)
        data['id'] = len(TheLanguage.query.all()) + 1
        languages.append(new_language)
        print(languages)

        new_entry = TheLanguage(data['id'], data['language'], data['framework'])
        db.session.add(new_entry)
        db.session.commit()
        return {'result': 'Language added'}, 201

    def get_id(self,id):
        user = TheLanguage.query.filter_by(id=id).first()
        schema = LanguageSchema()
        result_db = schema.dump(user)
        return result_db

    def update(self, id, data):
        user = TheLanguage.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            data['id'] = id
            new_entry = TheLanguage(data['id'], data['language'], data['framework'])
            db.session.add(new_entry)
            db.session.commit()
            return {'result': 'Deleted'}, 201
        else:
            return 'Not Available'

    def delete_id(self, id):
        user = TheLanguage.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'result': 'Deleted'}, 201
        else:
            return 'Not Available'


work = Work()


@ns.route('/')
class Language(Resource):

    @ns.doc(security='apikey')
    # @ns.marshal_with(a_language)
    @token_required
    def get(self):
        return work.get_all

    @ns.doc(security='apikey')
    @ns.expect(a_language)
    def post(self):
        return work.new(api.payload)


@ns.route('/<int:id>')
class LanguageModify(Resource):
    # @api.marshal_with(a_language, envelope='the_data')
    def get(self, id):
        return work.get_id(id)

    @ns.expect(a_language)
    def put(self, id):
        return work.update(id, api.payload)

    def delete(self, id):
        return work.delete_id(id)


if __name__ == '__main__':
    app.run(debug=True)
