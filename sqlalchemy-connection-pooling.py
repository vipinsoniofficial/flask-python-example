from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
from sqlalchemy import create_engine

from sqlalchemy.pool import SingletonThreadPool


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///one.db'
app.config['SQLALCHEMY_BINDS'] = {'one': 'sqlite:///one.db', 'two': 'sqlite:///two.db', 'three': 'sqlite:///three.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool': QueuePool,
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)

engine = create_engine('sqlite:///one.db', poolclass=SingletonThreadPool)

engine1 = db.create_engine('sqlite:///one.db', {"poolclass": QueuePool, "pool_use_lifo": True})
Session = sessionmaker(bind=engine1)
session1 = Session()

'''
Pool size : allowed connection
max overflow : additional connection
"pool_pre_ping": liveness of connection
'''
engine2 = db.create_engine('sqlite:///two.db', {"connect_args": {"pool_size": 5, "max_overflow": 20}, "pool_pre_ping": True})
Session = sessionmaker(bind=engine2)
session2 = Session()

# Disabling pooling using NullPool
engine3 = db.create_engine('sqlite:///three.db', {"poolclass": QueuePool})
# connection = engine3.connect()
Session = sessionmaker(bind=engine3)
session3 = Session()
connection = session3.connect()

'''

def getConnection():
    try:
        return engine3.connect()
    except:
        return False


mypool = QueuePool(getConnection(), max_overflow=10,pool_size=5)
conn = mypool.connect
session3 = Session(bind=conn)
'''


class One(db.Model):
    __bind_key__ = 'one'
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return 'id: {}'.format(self.id)


class Two(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return 'id: {}'.format(self.id)


class Three(db.Model):
    __bind_key__ = 'three'
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return 'id: {}'.format(self.id)


@app.route('/')
def index():
    #second = Two(id=119)
    #session2.add(second)
    #session2.commit()
    '''
    one = One(id=116)
    session1.add(one)
    session1.commit()
    '''

    three = Three(id=117)

    connection.execute(
        session3.add(three),
        session3.commit())
    connection.close()
    return 'Added to second table!!!'


@app.route('/get', methods=['GET'])
def get_all():
    db1 = One.query.all()
    print('One db:', db1)
    db2 = Two.query.all()
    print('Two db:', db2)
    db3 = Three.query.all()
    print('Three db:', db3)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)