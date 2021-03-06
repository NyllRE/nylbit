from nylbit import BlockChain

blockchain = BlockChain()

print("***Mining nylbit about to start***")
print(blockchain.chain)

last_block = blockchain.latest_block
last_proof_no = last_block.proof_no
proof_no = blockchain.proof_of_work(last_proof_no)

blockchain.new_data(
    sender="Nyll Test",  # it implies that this node has created a new block
    recipient="Nyll Bool",  # let's send Quincy some coins!
    # creating a new block (or identifying the proof number) is awarded with 1
    quantity=1,
)

last_hash = last_block.calculate_hash
block = blockchain.construct_block(proof_no, last_hash)

print("***Mining nylbit has been successful***")
print(blockchain.chain)
