from flask import Flask, request, send_file
from sam.sam import run_sam

app = Flask(__name__)

@app.route('/sam', methods = ['POST'])
def sam():
    x_coord = request.args.get('x_coord')
    y_coord = request.args.get('y_coord')
    file = request.files['image']
    file.save('static/input.jpg')
    run_sam(x_coord, y_coord)
    return send_file('static/mask.jpg', mimetype='image/jpeg')


@app.route('/get_bitmask', methods = ['GET'])
def get_bitmask():
    return send_file('static/bitmask.txt')