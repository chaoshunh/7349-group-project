import time
import hashlib

class Block(object):
    def __init__(self, index, proof, previousHash, records):
        self.index = index
        self.proof = proof
        self.previousHash = previousHash
        self.dataRecords = records
        self.timestamp = time.time()
        
    @property
    def getHashBlock(self):
        blockStr = "{}{}{}{}{}".format(self.index, self.proof, self.previousHash, self.dataRecords, self.timestamp)
        return hashlib.sha256(blockStr.encode()).hexdigest()
        
