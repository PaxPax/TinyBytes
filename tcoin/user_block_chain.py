import hashlib as hasher
import datetime
import sys
import json
import io
import os
import requests
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import jsonify
from flask import send_from_directory
from node_config import NODE_MINER

app= Flask(__name__)

class User_Chain:
    
    def __init__(self, index, time_stamp, data, previous_hash):
        self.difficulty = 1
        self._nounce = 0
        self.award = 1
        self.index = index
        self.time_stamp = time_stamp
        self.data = data
        self.previous_hash = previous_hash
        self._hash = self.calculate_hash()
    
    def calculate_hash(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.time_stamp) + str(self.data) + str(self.nounce) + str(self.previous_hash) + str(self.award)).encode('utf-8'))
        return str(sha.hexdigest())
    
    def json_block(self):
        my_json = json.dumps({'index': self.index, 'time_stamp': str(self.time_stamp), 'data': self.data, 
        'hash': self.hash, 'previous_hash': self.previous_hash, 'award': self.award})
        return my_json + "\n"

    def proof_of_work(self):
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
    genesis_block = User_Chain(0, datetime.datetime.now().time(), "genesis", "genesis_hash")
    return genesis_block


BLOCK_CHAIN = []
BLOCK_CHAIN.append(create_genesis_block)

@app.route('/grab_json')
def get_data():
    james = requests.get('http://127.0.0.1:5000/gimmmie').content
    string_james = "".join(map(chr, james))

    with open("./user_node_data.json", "a") as outfile:
        json.dumps(string_james, outfile)

    return "File OK!"

@app.route('/hash_data')
def patch_data():

    
    return "hey"
#NOTE the length of a block is 185

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88)