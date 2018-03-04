import requests
import time
import base64
import ecdsa

class Wallet:
    URL = "htp://localhost:5000/transaction"

    def __init__(self, name=""):
        self._name = name
        if not name:
            self.create__our_wallet()
        else:
            self.greeting_message()

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def public_key(self):
        return self._public_key
    @public_key.setter
    def public_key(self, value):
        self._public_key = value
    
    @property
    def private_key(self):
        return self._private_key
    @private_key.setter
    def private_key(self, value):
        self._private_key = value
    
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value
    
    def greeting_message(self):
        user_response = ""
        while user_response != 'q':
            user_response = input("1: Create Wallet \n 2: Send Transactions \n Press q to exit")
            if(user_response == "1"):
                self.create_wallet()
            elif(user_response == "2"):
                self.send_transactions()
    
    def create_wallet(self):
        ini_private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.private_key = ini_private_key.to_string().hex()
        ini_pub_key = ini_private_key.get_verifying_key()
        self.public_key = ini_pub_key.to_string().hex()

        print("Private Key: \n", self.private_key)
        print("Public Key \n", self.public_key)

        fout = open("./generated_wallet.txt", 'w')
        fout.write({"from": "initial", "to": "wallet", "amount": 0, "signature": "nope", "message": "Opening Wallet", "balance": 0} + "\n")
        fout.close()
        user_response = input("Save keys locally? y/n")
        if user_response == "y":
            out_file = open("./generated_keys.txt", 'w')
            out_file.write("Public key" + self.public_key + "\n")
            out_file.write("Private Key" + self.private_key + "\n")
            out_file.close()

        balance = 0
                

    def send_transactions(self):
        
        address_to = input("Please enter money destination")
        amount = input("Please enter the amount you want to send")
        sig,message = self.sign_ecdsa()
        if amount <= self.balance:
            payload = {"generating_address": self.public_key, "to": address_to, "amount": amount, "signature": sig.decode(), "message": message, "balance": 0}
            headers = {"Content-Type": "application/json"}
            self.balance -= amount
            requests.post(self.URL, json=payload, headers=headers)
    
    def sign_ecdsa(self):
        message = str(round(time.time()))
        byte_message = message.encode()
        ini_private_key = ecdsa.SigningKey.from_string(bytes.fromhex(self.private_key), curve=ecdsa.SECP256k1)
        signature = base64.b64decode(ini_private_key.sign(byte_message))
        return signature, message

    def recieve_transaction(self, address_from):

        recieved = requests.get(address_from)
        if (recieved.headers['content-type']== "application/json"):
            recieved_json = recieved.json()

            self.balance += recieved_json['balance']
            recieved_json['balance'] = self.balance
            fout = open("./generated_wallet.txt", 'a')
            fout.writeline(recieved_json)
            fout.close()
        else:
            print("The content type should be json")

    def send_anonymous_transaction(self, address_to, amount, block_hash):
        sig,message = self.sign_ecdsa()
        payload = {"from": self.public_key, "to": address_to, "amount": amount, "signature": sig.decode(), "message": message, "balance": 0, "block_hash": block_hash}
        headers = {"Content-Type": "application/json"}
        self.balance -= amount

        requests.post(self.URL, json=payload, headers=headers)

    def create__our_wallet(self):
        public_key = "key5ebb0da58b49ed281dbe62774bdb5dc31c4b606e1d727d86bc9eeadf87800e9b51a0ce5bdad05c29a0c1ed7b4d0c60dbf44a41ba5aac277b58b2ff2947092119"
        private_key = "Key1b8fcd718a33552f55b3695e334b9b83c50cd6b5780507f0666000db8b41de07"
        balance = 0
        fout = open("./masterWallet.txt", 'w')
        fout.write({"from": "initial", "to": "our_wallet", "amount": 0, "signature": "nope", "message": "Opening our wallet", "balance": 0})
        fout.close()
        


if __name__ == '__main__':
    my_wallet = Wallet()
