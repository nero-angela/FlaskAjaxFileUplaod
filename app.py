from flask import Flask, render_template, jsonify, request, url_for
from datetime import datetime
from os import listdir
from os.path import isfile, join

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/image', methods=['GET'])
def get_image():
    # get all files from the static directory
    static_path = './static'
    files = [f'/static/{f}' for f in listdir(static_path) if isfile(join(static_path, f))]
    return jsonify({'images': files})


@app.route('/image', methods=['POST'])
def post_image():
    try:
        image = request.files['images']
        extension = image.filename.split('.')[-1]  # extension
        timestamp = int(datetime.now().timestamp())  # utc timestamp
        image_name = f'/static/{timestamp}.{extension}'  # save path
        image.save(f'.{image_name}')
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'result': 'fail', 'error': e})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
