import requests

from blockchain import BlockChain

blockchain = BlockChain()

# --------------------------- Testing The Blockchain Transactions ---------------------------------------------

def display_blockchain(chain):
    for block in chain:
        print(vars(block))


def testBlockTransactions():
    print("Length of Current blockchain is: {}".format(len(blockchain.chain)))
    display_blockchain(blockchain.chain)

    blockchain.mine_block('TestFarm', 'AAA', 'Farm', '2')
    print("\nAfter Mining . . .")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    display_blockchain(blockchain.chain)

    blockchain.mine_block('TestManufacturer', 'BBB', 'Manufacturer', '3')
    print("\nAfter One more Mining . . .")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    display_blockchain(blockchain.chain)


if __name__ == "__main__":
    testBlockTransactions()
