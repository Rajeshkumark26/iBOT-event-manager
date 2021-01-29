from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/img/<path:path>')
def get_image(path):
    image_path = os.path.join(os.getcwd(),str(path))

    return send_file(image_path, mimetype='image/gif')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)