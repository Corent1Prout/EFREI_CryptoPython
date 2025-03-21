from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Dictionnaire pour stocker les clés des utilisateurs (idéalement, utiliser une base de données)
keys = {}

@app.route('/')
def hello_world():
    return render_template('hello.html')
    
@app.route('/set_key/', methods=['GET'])
def set_key_get():
    global user_key, f
    key = request.args.get('key')

    if not key:
        return jsonify({'error': 'Please provide a key.'}), 400

    try:
        user_key = key.encode()
        f = Fernet(user_key)
        return jsonify({'message': 'Key set successfully.'}), 200
    except Exception:
        return jsonify({'error': 'Invalid key format.'}), 400

@app.route('/encrypt/', methods=['POST'])
def encryptage():
    user_id = request.remote_addr
    f = keys.get(user_id)

    if f is None:
        return jsonify({'error': 'Key not set. Please set a key first.'}), 400

    data = request.get_json()
    if 'value' not in data:
        return jsonify({'error': 'Please provide a value to encrypt.'}), 400

    valeur_bytes = data['value'].encode()
    token = f.encrypt(valeur_bytes)
    return jsonify({'encrypted_value': token.decode()})

@app.route('/decrypt/', methods=['POST'])
def decryptage():
    user_id = request.remote_addr
    f = keys.get(user_id)

    if f is None:
        return jsonify({'error': 'Key not set. Please set a key first.'}), 400

    data = request.get_json()
    if 'token' not in data:
        return jsonify({'error': 'Please provide a token to decrypt.'}), 400

    try:
        token_bytes = data['token'].encode()
        valeur_decryptee = f.decrypt(token_bytes)
        return jsonify({'decrypted_value': valeur_decryptee.decode()})
    except Exception:
        return jsonify({'error': 'Invalid token or decryption failed.'}), 400

if __name__ == "__main__":
    app.run(debug=True)
