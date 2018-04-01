from flask import Flask, request, redirect, url_for, jsonify,send_from_directory, render_template
from werkzeug.utils import secure_filename
from block_chain import *
from pymongo import MongoClient

UPLOAD_FOLDER = ".././uploaded_data"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'gif', 'mp3'])
curr_blockchain = BlockChain()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
client = MongoClient()
db = client.fileshare

def allowed_file(filename):
    # db.reviews.insert_one({"uer": "JohnJohn", "passrd": "crapshoot"})
    # print(db.reviews.find())
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
            return 'file upload worked!'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
    <input type="textfield">Name to associate with file</input>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload_move', methods=['GET'])
def upload_move():
    curr_blockchain.convert_and_move()
    return "file moved!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)