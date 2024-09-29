from flask import Flask
from sam.sam import run_sam

app = Flask(__name__)


@app.route('/sam', methods = ['GET'])
def sam():
    return run_sam()