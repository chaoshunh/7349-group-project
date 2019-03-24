from uuid import uuid4

import requests

import MySQLdb

from flask import Flask, jsonify, url_for, request

import logging

from blockchain import BlockChain

def database_connect():
    try:
        connection = MySQLdb.Connection(host='localhost', user='root', passwd='Eng12ner', db='blockchaindb')
        cursor = connection.cursor()
        logging.warning("Connection established")
    except Exception as e:
        print("Error [%r]" % (e) )
    finally:
        if cursor:
            cursor.close() 
    #conn = sqlite3.connect('blockchain.db')
    #conn.row_factory = dict_factory
    #cursor = conn.cursor()
    return conn, cursor


app = Flask(__name__)

blockchain = BlockChain()

node_address = uuid4().hex  # Unique address for current node

@app.route('/')
def index():
    return "This is a sample rest service"

@app.route('/create-transaction', methods=['POST'])
def create_transaction():
    """
    Input Payload:
    {
        "entityId": 0,
        "entityName": "miner_name",
        "certificate": "miner_certificate",
        "entityType": "miner_type",
        "downstreamEntityId": "miner_downstreamid"
    }
    """
    transaction_data = request.get_json()

    index = blockchain.create_new_transaction(**transaction_data)

    response = {
        'message': 'Transaction has been submitted successfully',
        'block_index': index
    }

    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block(node_name, node_certificate, node_type, node_downstreamid)

    response = {
        'message': 'Successfully Mined the new Block',
        'block_data': block
    }
    return jsonify(response)


@app.route('/chain', methods=['GET'])
def get_full_chain():
    response = {
        'chain': blockchain.get_serialized_chain
    }
    return jsonify(response)


@app.route('/sync-chain', methods=['GET'])
def consensus():

    def get_neighbour_chains():
        neighbour_chains = []
        for node_address in blockchain.nodes:
            resp = requests.get(node_address + url_for('get_full_chain')).json()
            chain = resp['chain']
            neighbour_chains.append(chain)
        return neighbour_chains

    neighbour_chains = get_neighbour_chains()
    if not neighbour_chains:
        return jsonify({'message': 'No neighbour chain is available'})

    longest_chain = max(neighbour_chains, key=len)  # Get the longest chain

    if len(blockchain.chain) >= len(longest_chain):  # If our chain is longest, then do nothing
        response = {
            'message': 'Chain is already up to date',
            'chain': blockchain.get_serialized_chain
        }
    else:  # If our chain isn't longest, then we store the longest chain
        blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
        response = {
            'message': 'Chain was replaced',
            'chain': blockchain.get_serialized_chain
        }

    return jsonify(response)


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=5000, type=int)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True)
