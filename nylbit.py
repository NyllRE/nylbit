from hashlib import sha256
from time import time


class Block:

	def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
		# this keeps track of the position of the block within the blockchain
		self.index = index

		# this is the number produced during the creation of a new block (called mining)
		self.proof_no = proof_no

		# this refers to the hash of the previous block within the chain
		self.prev_hash = prev_hash

		# this gives a record of all transactions completed, such as the quantity bought
		self.data = data

		# this places a timestamp for the transactions
		self.timestamp = timestamp or time()

	# will generate the hash of the blocks using the above values
	@property
	def calculate_hash(self):
		block_of_string = "{}{}{}{}{}".format(self.index, self.proof_no,
											  self.prev_hash, self.data,
											  self.timestamp)

		return sha256(block_of_string.encode()).hexdigest()

	def __repr__(self):
		return "{} - {} - {} - {} - {}".format(self.index, self.proof_no,
											   self.prev_hash, self.data,
											   self.timestamp)


class BlockChain:

	def __init__(self):
		# this variable keeps all blocks
		self.chain = []

		# this variable keeps all the completed transactions in the block
		self.current_data = []
		self.nodes = set()

		# this method will take care of constructing the initial block
		self.construct_genesis()

	def construct_genesis(self):
		self.construct_block(proof_no=0, prev_hash=0)

	def construct_block(self, proof_no, prev_hash):
		block = Block(
			# this represents the length of the blockchain
			index=len(self.chain),

		 	# the caller method passes them
			proof_no=proof_no,
			prev_hash=prev_hash,

			# this contains a record of all the transactions that are not included in any block on the node
			data=self.current_data)

		# self.current_data is used to reset the transaction list on the node. If a block has been constructed and the transactions allocated to it, the list is reset to ensure that future transactions are added into this list. And, this process will take place continuously
		self.current_data = []

		# this method joins newly constructed blocks to the chain
		self.chain.append(block)

		return block
		
	@staticmethod
	def check_validity(block, prev_block):
		if prev_block.index + 1 != block.index:
			return False

		elif prev_block.calculate_hash != block.prev_hash:
			return False

		elif not BlockChain.verifying_proof(block.proof_no,
											prev_block.proof_no):
			return False

		elif block.timestamp <= prev_block.timestamp:
			return False

		else: return True

	def new_data(self, sender, recipient, quantity):
		self.current_data.append({
			'sender': sender,
			'recipient': recipient,
			'quantity': quantity
		})
		return True

	@staticmethod
	def proof_of_work(last_proof):
		'''this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
			f is the previous f'
			f' is the new proof
			'''
		proof_no = 0
		while BlockChain.verifying_proof(proof_no, last_proof) is False:
			proof_no += 1

		return proof_no


	@staticmethod
	def verifying_proof(last_proof, proof):
		#verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?

		guess = f'{last_proof}{proof}'.encode()
		guess_hash = sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"

	@property
	def latest_block(self):
		return self.chain[-1]
