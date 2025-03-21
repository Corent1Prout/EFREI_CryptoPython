from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify, request
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Test-Commit11

user_key = None
f = None

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Test-Commit11


@app.route('/set_key/', methods=['POST'])
def set_key():
    global user_key, f
    data = request.get_json()
    if 'key' not in data:
        return jsonify({'error': 'Please provide a key.'}), 400

    user_key = data['key'].encode()  # Convertir la clé en bytes

    try:
        f = Fernet(user_key)  # Créer une instance de Fernet avec la clé fournie
        return jsonify({'message': 'Key set successfully.'}), 200
    except Exception as e:
        return jsonify({'error': f'Invalid key: {str(e)}'}), 400
      
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    global f
    if f is None:
        return jsonify({'error': 'Key not set. Please set a key first.'}), 400
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str
  
@app.route('/decrypt/<string:token>')
def decryptage(token):
    global f
    if f is None:
        return jsonify({'error': 'Key not set. Please set a key first.'}), 400
    try:
        token_bytes = token.encode()  # Conversion str -> bytes
        valeur_decryptee = f.decrypt(token_bytes)  # Décryptage
        return f"Valeur décryptée : {valeur_decryptee.decode()}"  # Retourne la valeur déchiffrée
    except Exception as e:
        return f"Erreur lors du déchiffrement : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)                                                                                                                        
