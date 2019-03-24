import time
import hashlib
import MySQLdb

from block import Block

class BlockChain(object):  
      
    def __init__(self):  
        self.chain = []  
        self.current_node_transactions = []  
        self.create_genesis_block()  
      
    def create_genesis_block(self):  
        self.create_new_block(proof=0, previous_hash=0)
  
    def create_new_block(self, proof, previous_hash):  
        block = Block(
            index=len(self.chain),
            proof=proof,
            previousHash=previous_hash,
            transactions=self.current_node_transactions
        )
        self.current_node_transactions = []  # Reset the transaction list

        self.chain.append(block)
        return block
  
    def create_new_transaction(self, entityId, entityName, certificate, entityType, downstreamEntityId):  
        self.current_node_transactions.append({
            'entityId': entityId,
            'entityName': entityName,
            'certificate': certificate,
            'entityType': entityType,
            'downstreamEntityId': downstreamEntityId
        })
        return True

    def mine_block(self, miner_name, miner_certificate, miner_type, miner_downstreamId ):
        # Sender "0" means that this node has mined a new block
        # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
        self.create_new_transaction(
            entityId="0",
            entityName = miner_name,
            certificate = miner_certificate,
            entityType = miner_type,
            downstreamEntityId = miner_downstreamId
        )

        last_block = self.get_last_block

        last_proof = last_block.proof
        proof = self.create_proof_of_work(last_proof)

        last_hash = last_block.getHashBlock
        block = self.create_new_block(proof, last_hash)

        return vars(block)  # Return a native Dict type object

        Generate "Proof Of Work"

        A very simple `Proof of Work` Algorithm -
            - Find a number such that, sum of the number and previous POW number is divisible by 7
        """
        proof = previous_proof + 1
        while not BlockChain.is_valid_proof(proof, previous_proof):
            proof += 1

        return proof

    @staticmethod
    def is_valid_proof(proof, previous_proof):
        return (proof + previous_proof) % 7 == 0

    @property  
    def get_last_block(self):  
        return self.chain[-1]

    @property
    def get_serialized_chain(self):
        return [vars(block) for block in self.chain]

    @staticmethod
    def writetodb(index, proof, previous_hash, transactions):
        try:
            connection = MySQLdb.Connection(host='localhost', user='root', passwd='@g9gtP&O2912', db='blockchain')
            cursor = connection.cursor()
            sql = """INSERT INTO transaction (block_index,proof,previous_hash,transactions) VALUES (%d,%d,'%s',"%s")""" % (index,proof,previous_hash,transactions)
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print("Error [%r]" % (e) )
        finally:
            if cursor:
                cursor.close() 

#from flask import Flask

#app = Flask(__name__)

#@app.route('/create-transaction', methods=['POST'])

#def create_transaction():
#    pass

#app.run(debug=True)
