
key_file = open("./generated_keys.txt", "r")
garbage_1 = key_file.readline().split()

NODE_MINER = garbage_1[1]

NODE_URL = "http://localhost:5000"

OTHER_NODES = []