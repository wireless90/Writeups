# Warmup - 50 points

It's important to warmup before physical activity.

Free hint, don't get used to it: XOR cipher was used for this flag's encryption with a single byte key.


# Let's Begin

So we practically need to find the key that was xored. Since its just 1 byte, its easy to bruteforce.

And the flag is always in the format if  `ivyctf{...}`.


So lets find the key that simply xors to match the first letter `i`.

```py
In [19]: def get_key(contents):
    ...:     for i in range(256):
    ...:         if ord(contents[0]) ^ i == ord('i'):
    ...:             return i
    ...:
    ...:
    ...:
    ...:
    ...:
```

Above is just a function that gets the content of the file and goes through the value of a byte, 0 to 255.
For each of the value, we xor it with the first letter and see if it hits the letter `i`.

Once we get the key, we simply xor it with the rest of the file.

```py
In [21]: def crack_flag(contents, key):
    ...:     flag = []
    ...:     for ch in contents:
    ...:         flag.append(chr(ord(ch) ^ key))
    ...:     print(''.join(flag))
```


Once we get our functions right, lets run them.

```py
In [23]: contents = open('flag.enc', 'r').read()

In [24]: crack_flag(contents, get_key(contents))
ivyctf{all_warmed_up_and_ready_to_go}
```

