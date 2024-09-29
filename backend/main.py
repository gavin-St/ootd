from flask import Flask, request, send_file
from sam.sam import run_sam
from db.get_attributes import get_attributes
from db.get_embedding import get_embedding
from db.search import query_by_vector
import json

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def process():
    x_coord = request.args.get('x')
    y_coord = request.args.get('y')
    file = request.files['image']
    file.save('static/input.jpg')
    run_sam(x_coord, y_coord)
    attribute_json = get_attributes('static/mask.jpg')
    embedding_vector = get_embedding(attribute_json)
    result = query_by_vector(attribute_json, embedding_vector)
    print(result)
    return result


@app.route('/get_bitmask', methods = ['GET'])
def get_bitmask():
    return send_file('static/bitmask.txt')