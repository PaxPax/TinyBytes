import hashlib as hasher
import json
import time
import os

class Block:
    def __init__(self, index, time_stamp, data, previous_hash, user_info):
        self.difficulty = 3
        self._nounce = 0
        self._data = data
        self._index = index
        self._time_stamp = time_stamp
        self._previous_hash = previous_hash
        self._user = user_info
        self._hash = self.calculate_hash()
    
    @property
    def user_info(self):
        return self._user
    @property
    def data(self):
        return self._data
    @data.setter
    def setter(self, value):
        self._data = value
    @property
    def nounce(self):
        return self._nounce
    @property
    def index(self):
        return self._index
    @property
    def time_stamp(self):
        return self._time_stamp
    @property
    def previous_hash(self):
        return self._previous_hash
    @property
    def hash(self):
        return self._hash
    @hash.setter
    def hash(self, value):
        self._hash = value
    @nounce.setter
    def nounce(self, increment):
        self._nounce = increment
    
    def calculate_hash(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.time_stamp) + str(self.data) + str(self.nounce) + self.previous_hash + self.user_info).encode('utf-8'))
        return sha.hexdigest()
    def to_json_block(self):
        create_json = json.dumps({'index': self.index, 'time_stamp': str(self.time_stamp), 'data': self.data, 
        'hash': self.hash, 'previous_hash': self.previous_hash})
        return create_json
    
    def give_ore(self):
        create_json = json.dumps({'index': self.index, 'time_stamp': str(self.time_stamp), 'data': self.data, 'previous_hash': self.previous_hash})
        return create_json
        # 'hash': self.hash

    def proof_of_work(self):
        curr_difficulty = '0' * self.difficulty
        while curr_difficulty != self.hash[  :self.difficulty]:
            self.nounce += 1
            self.hash = self.calculate_hash()

def create_genesis_block():
    """
        when the chain is created a initial block must be set
        these values are garbage data and have no bearing on the
        actual chain

        Args:
            none
        Returns: 
            a newly created block
    """
    genesis_block = Block(0, "Origin Time", "Origin Data", "Genesis Hash", "Central Node")
    return genesis_block

class BlockChain:
    block_chain = []

    def __init__(self):
        self.block_chain.append(create_genesis_block())

    def get_current_block(self):
        return self.block_chain[-1]
    def ignore_first_block(self):
        return self.block_chain[1:]

    def convert_and_move(self):
        """takes the current file of the directory
        and converts the file into a byte array then
        the file is moved to another directory to not be duplicated

        Args:
            none
        Returns:
            'Directory is Empty' if empty
            list: bytearray if media else b''
        """
        byte_array = None
        conversion_file = ".././uploaded_data/"
        current_dir = os.listdir(".././uploaded_data")
        if os.listdir(conversion_file):
            conversion_file += current_dir[0]
        else:
            exit
        try:
            with open(conversion_file, 'rb') as out_file:
                new_file = out_file.read()
                byte_array = bytearray(new_file)
            os.rename(conversion_file, ".././hashed_data/" + current_dir[0])
        except:
            print("Error"+ conversion_file  + "could not be opened")
        return byte_array

    def append_block_chain(self):
        """
        TODO: implement an actual user to attribute to the appropriate saved file
        Args: 
            <soon> the owner of the files name
        Return:
            none
        """
        bsUser = "bsUser"
        tmp_dic = self.bytes_for_consumption()
        for _key in tmp_dic:
            old_block = self.get_current_block()
            next_index = old_block.index +  1
            previous_hash = old_block.hash
            new_block = Block(next_index, time.time(), tmp_dic[_key], previous_hash, bsUser)
            new_block.proof_of_work()
            self.block_chain.append(new_block)


    def bytes_for_consumption(self):
        """
            instead of creating amount of blocks containing only a byte
            a grouping of bytes will be created and stored into a dictionary
            where each block will receive a list of bytes

        """
        tmp_list = []
        tmp_dic = {}
        tmp_key = "chunk"
        counter = 0
        byte_array = self.convert_and_move()

        for index in range(len(byte_array)):
            tmp_list.append(byte_array[index])
            if index % 100 == 0:
                tmp_dic[tmp_key] = tmp_list
                tmp_list = []
                tmp_key = "chunk" + str(counter)
                counter+=1
        tmp_dic['chunk'] = tmp_list
        return tmp_dic
    
    def save_current_chain(self):
        tmp_list = []
        for bs in self.block_chain:
            tmp_list.append(bs.to_json_block())
        with open('.././current_hash_block/central_node_data.json', 'w') as outfile:
            json.dump(tmp_list, outfile)