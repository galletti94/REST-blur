from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine(os.environ['DATABASE_URL'])
app = Flask(__name__)
api = Api(app)










if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
