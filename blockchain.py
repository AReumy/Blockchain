import hashlib
import json
from time import time

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # genesis block: 最も最初のブロックを生成
        self.new_block(previous_hash=1, proof=100)

    # 新しいブロックを生成
    # ブロックを生成する時、以前のブロックのハッシュを保存
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 現在のトランザクションリストをリセット
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):

        # sender: 送信アドレス
        # recipient: 受信アドレス
        # amount: お金の量
        # 3つのパラメータの値を伝達を受けてトランザクションリストに追加
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    # 作業証明(POW): 新しいブロックを作成したり、採掘する方法
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof * proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # このコードで作業証明をする時、いつもハッシュ化した値の前の4つを0000で維持
        # これを難易度と呼ばれる
        # ブロックでこれをdifficultyと言って、0000をNonceと呼ばれる
        return guess_hash[:4] == "0000"