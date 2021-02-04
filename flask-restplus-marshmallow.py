from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from marshmallow import Schema, fields as mafields, post_load
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
api = Api(app)
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


a_language = api.model('Language', {'language': fields.String("the language."), 'framework': fields.String("The framework")})

languages = []
# python = {'language': 'python', 'id': 1}
python = TheLanguage(id=1, language='python', framework='Flask')
languages.append(python)
# db.session.add(python)
# db.session.commit()


@api.route('/language')
class Language(Resource):
    # @api.marshal_with(a_language, envelope='the_data')
    def get(self):
        all_users = TheLanguage.query.all()
        schema = LanguageSchema(many=True)
        # print(languages)
        return schema.dump(all_users)

    @api.expect(a_language)
    def post(self):
        schema = LanguageSchema()
        data = api.payload
        new_language = schema.load(data)
        print(new_language)
        data['id'] = len(languages) + 1
        languages.append(new_language)
        print(languages)

        new_entry = TheLanguage(data['id'], data['language'], data['framework'])
        db.session.add(new_entry)
        db.session.commit()
        return {'result': 'Language added'}, 201


@api.route('/language/<int:id>')
class LanguageModify(Resource):
    # @api.marshal_with(a_language, envelope='the_data')
    def get(self, id):
        user = TheLanguage.query.filter_by(id=id).first()
        schema = LanguageSchema()
        result_db = schema.dump(user)
        return result_db
        #schemas = LanguageSchema(many=True)
        #result = schemas.dump(languages)
        #for l in result:
         #   if l['id'] == id:
          ##     return result_db
        #else:
         #   return 'Not Available'

    @api.expect(a_language)
    def put(self, id):
        data = api.payload
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
        '''
        data = api.payload
        user = TheLanguage.query.filter_by(id=id).first()
        schema = LanguageSchema()
        result_db = schema.dump(user)
        print(result_db['language'], result_db['framework'])
        print(type(result_db['language']))
        print('user', type(user))
        # print(result_db)
        print(data)

        # data['id'] = id
        # new = TheLanguage(data['id'], data['language'], data['framework'])
        user['language'] = result_db['language']
        user['framework'] = result_db['framework']

        db.session.commit()
        return user
        '''
        '''
        schema = LanguageSchema(many=True)
        result = schema.dump(languages)
        for l in result :
            if l['id'] == id:

                print(data)
                l['language'] = data['language']
                l['framework'] = data['framework']
                print(l)
                languages[id-1] = l
                return {'result': 'Updated'}, 201
        else:
            return 'Not Available'
        '''

    def delete(self, id):
        user = TheLanguage.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'result': 'Deleted'}, 201
        else:
            return 'Not Available'
        '''
        schema = LanguageSchema(many=True)
        result = schema.dump(languages)
        for l in result:
            if l['id'] == id:
                del languages[id-1]
                return {'result': 'Deleted'}, 201
        else:
            return 'Not Available'
            '''


if __name__ == '__main__':
    app.run(debug=True)