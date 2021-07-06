from flask import Flask, request, Response
from flask_cors import CORS
from hashlib import md5
import time

app = Flask(__name__)
CORS(app)

def get_flag_length():
    time.sleep(0.05) # Throttling against brute-forcers
    flag = open('../flag.txt','r').read()
    return len(flag)

def get_flag_char(i):
    flag = open('../flag.txt','r').read()
    return flag[i].encode()

def checkflag(userflag):
    for i, c in enumerate(userflag):
        if get_flag_length() <= i:
            return False

        if c.encode() != get_flag_char(i):
            return False

    if get_flag_length() != len(userflag):
        return False

    return True

@app.route("/", methods=['GET'])
def index():
    userflag = request.args.get('flag')
    if not userflag:
        return Response("Missing flag", status=401)

    if checkflag(userflag):
        return Response("YOU DID IT!!!", status=200)
    else:
        return Response("Wrong flag. Characters supported: [a-z_{}]", status=401)
