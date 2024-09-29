from flask import Flask, request, send_file, jsonify
from flask import Flask, request, send_file, jsonify
from sam.sam import run_sam
from db.get_attributes import get_attributes
from db.get_embedding import get_embedding
from db.search import query_by_vector
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods = ['POST'])
@cross_origin()
def process():
    x_coord = int(float(request.args.get('x')))
    y_coord = int(float(request.args.get('y')))
    print(x_coord, y_coord)
    file = request.files["file"]
    print(request.get_data())

    file.save('static/input.jpg')
    run_sam(x_coord, y_coord)
    attribute_json = get_attributes('static/mask.jpg')
    embedding_vector = get_embedding(attribute_json)
    result = query_by_vector(attribute_json, embedding_vector)
    print(result)
    return jsonify(result)


@app.route('/get_bitmask', methods = ['GET'])
def get_bitmask():
    return send_file('static/bitmask.txt')