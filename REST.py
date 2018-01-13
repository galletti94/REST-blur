from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from json import dumps
import os
import psycopg2
from urllib import parse
import hashlib


app = Flask(__name__)
app.config['SESSION_TYPE']= 'memcached'
app.config['SECRET_KEY']= 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db_connect = SQLAlchemy(app)

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

db_connect.init_app(app)

class Models_id(Resource):
    def get(self):
        cursor = conn.cursor()
        query = 'SELECT * FROM models'
        cursor.execute(query)
        return {'models': [i[0] for i in cursor.fetchall()]}


class Models_weights(Resource):
    def get(self, model_type):
        cursor = conn.cursor()
        query = 'SELECT model_weights FROM models WHERE model_type= %s'
        cursor.execute(query, (model_type))
        return {'weights': [i[0] for i in cursor.fetchall()]}

class Images(Resource):
    def get(self):
        cursor = conn.cursor()
        query = 'SELECT * FROM images'
        cursor.execute(query)
        return {'images': [{"id":i[0], "img":i[1], "label":i[2]} for i in cursor.fetchall()]}

    def post(self):
        cursor = conn.cursor()
        img = request.json['img']
        label = request.json['label']
        query = 'INSERT INTO images(img, label) VALUES (%s, %s)'
        try:
            cursor.execute(query, (img, label))
            conn.commit()
            return {'status':'success'}
        except Exception as e:
            return {'status':e}


api.add_resource(Models_id, '/models_id/')
api.add_resource(Models_weights, '/models_weights/<model_type>')
api.add_resource(Images, '/images/')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
