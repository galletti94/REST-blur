from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine(os.environ['DATABASE_URL'])
app = Flask(__name__)
api = Api(app)

class Models_id(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('SELECT * FROM models')
        return {'models': [i[0] for i in query.cursor.fetchall()]}


class Models_weight(Resource):
    def get(self, model_type):
        conn = db_connect.connect()
        query = conn.execute('SELECT weights FROM models WHERE model_type= %s' (model_type))
        return {'weights': [i[0] for i in query.cursor.fetchall()]}

class Images(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('SELECT * FROM images')
        return {'images': [i[0] for i in query.cursor.fetchall()]}

    def post(self):
        conn = db_connect.connect()
        img = request.json['img']
        label = request.json['label']
        try:
            query = conn.execute('INSERT INTO images(img, label) VALUES (%s, %s)' (img, label))
            return {'status':'success'}
        except Exception e:
            return {'status':'error %s' e}



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
