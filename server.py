from flask import Flask, jsonify, request
from uuid import uuid4

# 前に作成したブロックチェーンのモデュールをこのファイルから使用
from blockchain import Blockchain

# ノードのインスタンス化
app = Flask(__name__)

# そのノードのグローバル固有アドレスを生成
node_identifier = str(uuid4()).replace('-', '')

# ブロックチェーンのインスタンス化
blockchain = Blockchain()


# サーバーに新しいブロックを採掘するため知らせ
@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"


# ブロックをための新しいトランザクションを生成
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json(force=True)

    # 必要なフィールドが‘POST’データにあるかどうかをチェック
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # トランザクションを生成
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}

    return jsonify(response), 201


# ブロックチェーンの全体を返還
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)