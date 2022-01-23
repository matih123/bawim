import random
import string
import json
import hashlib
from bawim import app
from flask import make_response, request, jsonify
from bawim.users_list import users

global_key = 'Re2LPGUMEKa34ik1uhHOBMoc'
print_token = False
get = lambda request, value : request.form.get(value)

class Passwords():
    @staticmethod
    def read():
        with open('passwords.txt', 'r') as f:
            passwords = [line.replace('\n', '') for line in f.readlines()]
        return passwords

    @staticmethod
    def add(password):
        with open('passwords.txt', 'a') as f:
            f.write('\n' + password)

class Tokens():
    @staticmethod
    def generate(user_id):
        plaintext = (str(user_id) + users[user_id]['username'] + users[user_id]['email'])[::-1]
        token = ''
        alphabet = string.ascii_letters + string.digits + '@.'
        sbox = '2k8PseIuF.YTWUovx6BqbnOyQ@5dtERZKMc3iwg7jLN40lzpJmrHAShVaf1XCG9D'
        
        for char in plaintext:
            token += sbox[(alphabet.index(char) + 13) % len(alphabet)]

        return token

    @staticmethod
    def verify(token, user_id):
        plaintext = ''
        alphabet = string.ascii_letters + string.digits + '@.'
        sbox = '2k8PseIuF.YTWUovx6BqbnOyQ@5dtERZKMc3iwg7jLN40lzpJmrHAShVaf1XCG9D'
        
        for char in token:
            plaintext += alphabet[(sbox.index(char) - 13) % len(alphabet)]

        if plaintext[::-1] == str(user_id) + users[user_id]['username'] + users[user_id]['email']:
            return True
        else:
            return False

def find_user_id(username):
    for u in users:
        if u['username'] == username:
            return users.index(u)
    return None

@app.route('/', methods=['GET'])
def home():
    r = make_response('BAWIM - Aplikacja Bank', 200)
    r.mimetype = 'text/plain'
    return r

#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc http://localhost:5000/get_app_version
#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc https://bawim.tk/get_app_version
@app.route('/get_app_version', methods=['POST'])
def get_app_version():
    if get(request, 'key') == global_key:
        r = make_response('REST API for banking app, version 1.0.0', 200)
    else:
        r = make_response('Bad key.', 400)
        
    r.mimetype = 'text/plain'
    return r

#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc http://localhost:5000/user/0
#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc https://bawim.tk/user/0
@app.route('/user/<int:user_id>', methods=['POST'])
def user(user_id):
    if get(request, 'key') == global_key:
        if 0 <= user_id < len(users):
            basic_data = {'username': users[user_id]['username'], 'user_key': users[user_id]['user_key']}
            r = make_response(jsonify(basic_data), 200)
            r.mimetype = 'application/json'
        else:
            r = make_response('User does not exist.', 400)
            r.mimetype = 'text/plain'
    else:
        r = make_response('Bad key.', 400)
        r.mimetype = 'text/plain'

    return r

#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d user_key=VkCrRJTzU0NQoHXheBy48EB1 http://localhost:5000/user_data/0
#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d user_key=VkCrRJTzU0NQoHXheBy48EB1 https://bawim.tk/user_data/0
@app.route('/user_data/<int:user_id>', methods=['POST'])
def user_data(user_id):
    if get(request, 'key') == global_key and get(request, 'user_key') == users[user_id]['user_key']:
        if 0 <= user_id < len(users):
            r = make_response(jsonify(users[user_id]), 200)
            r.mimetype = 'application/json'
        else:
            r = make_response('User does not exist.', 400)
            r.mimetype = 'text/plain'
    else:
        r = make_response('Bad key.', 400)
        r.mimetype = 'text/plain'

    return r

#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d password=12345 http://localhost:5000/login/admin
#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d password=12345 https://bawim.tk/login/admin
@app.route('/login/<username>', methods=['POST'])
def login(username):
    user_id = find_user_id(username)
    if get(request, 'key') == global_key:
        if user_id is not None:
            if get(request, 'password') in Passwords.read() and user_id == 386:
                session_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(51))
                session_id = session_id[0:12] + '-' + session_id[13:25] + '-' + session_id[26:38] + '-' + session_id[39:51]
                success_data = {'username': 'admin', 'user_id': 386, 'status': '200 OK', 'session_id': session_id}
                r = make_response(jsonify(success_data), 200)
                r.mimetype = 'application/json'
            else:
                error_data = {'error_message': 'Invalid username or password.', 'username': username, 'user_id': user_id, 'status': '400 ERROR'}
                r = make_response(jsonify(error_data), 400)
                r.mimetype = 'application/json'
        else:
            r = make_response('User does not exist.', 400)
            r.mimetype = 'text/plain'     
    else:
        r = make_response('Bad key.', 400)
        r.mimetype = 'text/plain'

    return r

#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc http://localhost:5000/reset_password/0
#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc https://bawim.tk/reset_password/0
@app.route('/reset_password/<int:user_id>', methods=['POST'])
def reset_password(user_id):
    if get(request, 'key') == global_key:
        address, username = users[user_id]["email"], users[user_id]['username']
        token = Tokens.generate(user_id)
        success_data = {'username': username, 'user_id': user_id, 'status': '200 OK', 'message': f'Email with token {token if print_token else ""} and password reset information was sent to {address}.'}
        r = make_response(jsonify(success_data), 200)
        r.mimetype = 'application/json'
    else:
        r = make_response('Bad key.', 400)
        r.mimetype = 'text/plain'

    return r

#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d new_password=12345 http://localhost:5000/set_password/0/tokenabc
#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d new_password=12345 https://bawim.tk/set_password/0/tokenabc
@app.route('/set_password/<int:user_id>/<token>', methods=['POST'])
def set_password(user_id, token):
    if get(request, 'key') == global_key:
        new_password = get(request, 'new_password')
        if new_password is not None:
            if Tokens.verify(token, user_id) and user_id == 386:
                Passwords.add(new_password)
                success_data = {'user_id': user_id, 'status': '200 OK', 'message': f'New password for user_id={user_id} was set to {new_password}.'}
                r = make_response(jsonify(success_data), 200)
                r.mimetype = 'application/json'
            else:
                r = make_response('Received token is not correct.', 400)
                r.mimetype = 'text/plain'
        else:
            r = make_response('Please specify new password.', 400)
            r.mimetype = 'text/plain'
    else:
        r = make_response('Bad key.', 400)
        r.mimetype = 'text/plain'

    return r

#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d billing_token=[] -d json={\"billing_token\":[]} http://localhost:5000/set_premium_account/0
#curl -i -X POST -d key=Re2LPGUMEKa34ik1uhHOBMoc -d billing_token=[] -d json={\"billing_token\":[]} http://bawim.tk/set_premium_account/0
@app.route('/set_premium_account/<int:user_id>', methods=['POST'])
def set_premium_account(user_id):
    key_in_json = None
    try: key_in_json = json.loads(request.form.get('json'))['key']
    except: pass

    if get(request, 'key') == global_key or key_in_json == global_key:
        billing_token1 = get(request, 'billing_token')
        billing_token2 = None
        try:
            billing_token2 = json.loads(request.form.get('json'))['billing_token']
        except: pass
        
        if billing_token2 is not None: 
            billing_token = billing_token2
        elif billing_token1 is not None:
            billing_token = billing_token1
        else: 
            billing_token = ''

        hashed = ''
        try:
            md5 = hashlib.new('md5', usedforsecurity=False)
            md5.update(billing_token.encode('utf-8'))
            hashed = md5.hexdigest()
        except: pass

        for i, char in enumerate(hashed):
            print(i, char)
            if char != str(i % 10):
                r = make_response('Bad billing token.', 400)
                r.mimetype = 'text/plain'
                break
        else:
            users[user_id]['account_type'] = 'premium'
            success_data = {'user_id': user_id, 'status': '200 OK', 'message': f'Account type for user_id={user_id} was set to premium.'}
            r = make_response(jsonify(success_data), 200)
            r.mimetype = 'application/json'
    else:
        r = make_response('Bad key.', 400)
        r.mimetype = 'text/plain'

    return r
