import hashlib as hasher
import datetime
import sys
import json
import io
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import jsonify
from flask import send_from_directory

from wallet import Wallet
from node_config import NODE_MINER, NODE_URL, OTHER_NODES

UPLOAD_FOLDER = "../tcoin/uploaded_data"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'gif', 'mp4'])

app= Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
"""
http://flask.pocoo.org/docs/0.12/patterns/fileuploads/ example code was used for the home route and allowed_file
both are considered free use.
"""
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
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
            test_c = BlockChain()
            test_c.add_block()
            test_c.write_chain_to_file()
            test_c.write_gathered_bytes()  
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/gimmmie')
def gimmmie():
    with open('data.txt', 'r') as outfile:
        json_data = outfile.read()
    return jsonify(json_data)

class Block:
    def __init__(self, index, time_stamp, data, previous_hash):
        """
            difficulty: how many zeroes will the has need in front in order to be considered valid
            nounce: is a garbage value that allows us to try many combinations for a valid hash
            award: is the 'money' they receive for finding a valid hash
            time_stamp: will be at the time of the found valid hash
            data: is our broken up file into bytes
            previous_hash: is last blocks current hash *********important********
            hash: is a sha256 algo we look through to find a certain amount of zeroes in front
        """
        self.difficulty = 1
        self._nounce = 0
        self.award = 1
        self.index = index
        self.time_stamp = time_stamp
        self.data = data
        self.previous_hash = previous_hash
        self._hash = self.calculate_hash()

    def calculate_hash(self):
        """
            except for the genesis hash this method will be called multiple times
            until the amount of zeroes infront match the digit difficulty
        """
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.time_stamp) + str(self.data) + str(self.nounce) + str(self.previous_hash) + str(self.award)).encode('utf-8'))
        return str(sha.hexdigest())
    
    def json_block(self):
        """
            used to easily access certain parts of data we need
            will also be used for to give other miners a chance to solve our algorithm
        """
        my_json = json.dumps({'index': self.index, 'time_stamp': str(self.time_stamp), 'data': self.data, 
        'hash': self.hash, 'previous_hash': self.previous_hash, 'award': self.award})
        return my_json


    def proof_of_work(self):
        """
            example difficulty is at 1 so we just need a hash that has 1 zero in front
            0ldkfjdLKFjdufh3092jiJDFUIh293jdsfoJ092fdfj[valid]
            dlkfjiuh29jfiudslfkjsdoifjihdwfj089ud98f2oi[not valid]
        """
        current_difficulty = '0' * self.difficulty

        while(self.hash[ :self.difficulty] != current_difficulty):
            self.nounce += 1
            self.hash = self.calculate_hash()


    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, increase):
        self._hash = increase

    @property
    def nounce(self):
        return self._nounce

    @nounce.setter
    def nounce(self, increment):
        self._nounce = increment

def create_genesis_block():
    """
        called through our blockchain will be used to create the intial block that has
        garbage data because it's our genesis
    """
    genesis_block = Block(0, datetime.datetime.now().time(), "genesis", "genesis_hash")
    return genesis_block

class BlockChain:
    block_chain = []
    ourWallet = Wallet("OurWallet")

    def __init__(self):
        self.block_chain.append(create_genesis_block())
     
    def get_current_block(self):
        return self.block_chain[-1]

    def convert_file(self):
        """
            once the server is implemented that can handle file uploads
            this will be used to accept a file/ save the file in a directory/ then
            split the file into a array of bytes that will be consumed through our hash
        """
        byte_array = None
        try:
            with open("./uploaded_data/knight.png", "rb") as file_convert:
                new_file = file_convert.read()
                byte_array = bytearray(new_file)
        except:
            print("file not found")
        return byte_array

    def add_block(self):
        """
            the algo keeps adding blocks until the total byte array is consumed
        """
        byte_array = self.convert_file()
        if len(byte_array): 
            for x in range(len(byte_array)):
                old_block = self.get_current_block()
                next_index = old_block.index
                new_block = Block(next_index + 1,datetime.datetime.now().time(), byte_array[x], old_block.hash)
                new_block.proof_of_work()
                self.block_chain.append(new_block)

    def get_entire_chain(self):
        return self.block_chain[1:]
    
    """
        my_json = json.dumps({'index': self.index, 'time_stamp': str(self.time_stamp), 'data': self.data, 
        'hash': self.hash, 'previous_hash': self.previous_hash, 'award': self.award})
    """
    def write_chain_to_file(self):
        tmp_array = []
        for element in self.block_chain:
            bc_json = json.dumps([{'index': element.index, 'time_stamp': str(element.time_stamp), 'data': element.data, 
            'hash': element.hash, 'previous_hash': element.previous_hash, 'award': element.award}])
            tmp_array.append(bc_json)
            with open('master_node_data.json', 'w') as outfile:
                json.dump(tmp_array, outfile)

    # def write_chain_to_file(self):
    #     """
    #         takes our json blocks and saves them to a text file of the users current directory
    #     """
    #     for element in self.block_chain:
    #         bc_json = json.loads(element.json_block())
    #         with open('data.txt', 'a') as outfile:
    #             json.dump(bc_json, outfile)
    #             outfile.close()

    def grab_bytes_from_file(self):
        """
            opens a file and only grabs the relevant information of the bytes so that
            we may use another method to turn those bytes back into the original file
        """
        temp_byte_array = []
        current_chain = self.get_entire_chain()
        for index in range(len(current_chain)):
            json_me = json.loads(current_chain[index].json_block())
            temp_byte_array.append(int(json_me["data"]))
        return temp_byte_array
    
    def write_gathered_bytes(self):
        """
            when called the method call grab_bytes_from_file and then writes the file as
            a duplicate of the original source, the data is grabbed in sequential order
            other wise you won't end up with the same file
        """
        total_bytes = self.grab_bytes_from_file()
        open("./uploaded_data/knight.png", 'wb').write(bytes(total_bytes))

    def check_valid_match(self, user_address, miners_block):
        """
            after we /get the relevent information for them to begin minning their blocks
            we check to see if they match our blocks we created from users uploading files
            if we do we'll reward them with a coin as a thank you
        """
        for elements in self.block_chain:
            if miners_block.hash == elements.hash:
                print("reward them")
                self.ourWallet.send_anonymous_transaction("key5ebb0da58b49ed281dbe62774bdb5dc31c4b606e1d727d86bc9eeadf87800e9b51a0ce5bdad05c29a0c1ed7b4d0c60dbf44a41ba5aac277b58b2ff2947092119")

        
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)              
      
