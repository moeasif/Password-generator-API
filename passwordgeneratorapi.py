import random
import string
import json
from flask import Flask, jsonify, request

app = Flask(__name__)
PASSWORD_FILE = "saved_passwords.json"

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def save_password(name, password):
    try:
        with open(PASSWORD_FILE, "r") as file:
            passwords = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        passwords = {}
    
    passwords[name] = password
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

@app.route('/generate-password', methods=['GET'])
def get_password():
    length = request.args.get('length', default=12, type=int)
    name = request.args.get('name', default=None, type=str)
    password = generate_password(length)
    
    if name:
        save_password(name, password)
    
    return jsonify({"password": password})

@app.route('/saved-passwords', methods=['GET'])
def get_saved_passwords():
    try:
        with open(PASSWORD_FILE, "r") as file:
            passwords = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        passwords = {}
    return jsonify(passwords)

if __name__ == '__main__':
    app.run(debug=True, port=5000)