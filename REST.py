from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from json import dumps
import os
import psycopg2
from urllib import parse
import hashlib


app = Flask(__name__)
#app.config['SESSION_TYPE']= 'memcached'
#app.config['SECRET_KEY']= 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    def get(self):
        cursor = conn.cursor()
        model_type = "digits"
        query = 'SELECT * FROM models'
        cursor.execute(query)
        for i in cursor.fetchall():
            res = {"model_id":i[0], "model_type":i[1], "model_activation":i[2], "model_wih":i[3], "model_who":i[4], "model_input_layer":i[5], "model_hidden_layer":i[6], "model_output_layer":i[7]}
            break
        return res

class Images(Resource):
    def get(self):
        cursor = conn.cursor()
        query = 'SELECT * FROM images'
        cursor.execute(query)
        return {'images': [{"img_id":i[0], "img":i[1], "img_label":i[2], "img_type":i[3]} for i in cursor.fetchall()]}
    
    def post(self):
        cursor = conn.cursor()
        img = request.args.get('img')
        img_label = request.args.get('img_label')
        img_type = request.args.get('img_type')
        query = 'INSERT INTO images(img, img_label, img_type) VALUES (%s, %s, %s)'
        try:
            cursor.execute(query, (img, img_label, img_type))
            conn.commit()
            return {'status':'success'}
        except:
            return {'status':'failed'}
        
        
api.add_resource(Models_id, '/models_id/')
api.add_resource(Models_weights, '/model_digits/')
api.add_resource(Images, '/images/')

if __name__ == '__main__':
    app.run(debug=True)
