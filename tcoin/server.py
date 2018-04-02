from flask import Flask, request, redirect, url_for, jsonify,send_from_directory, render_template
from werkzeug.utils import secure_filename
from block_chain import *
import os

UPLOAD_FOLDER = "../tcoin/uploaded_data"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'gif', 'mp3', 'mp4'])
curr_blockchain = BlockChain()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('add_block'))
    return render_template('index.html')

@app.route('/add_block', methods=['GET'])
def add_block():
    curr_blockchain.append_block_chain()
    return 'File added to chain!'

# @app.route('/add_block', methods=['GET'])
# def add_block():
#     curr_blockchain.append_block_chain()
#     curr_blockchain.convert_and_move()
#     curr_blockchain.save_current_chain()
#     return "file moved!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)