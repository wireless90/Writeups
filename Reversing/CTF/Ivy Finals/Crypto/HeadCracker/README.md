# HeadCracker - 300 points

The best tool to crack this custom cipher with is your head. Just don't literally crack your head.


# Let's Begin

Let's first see what type of file we are dealing with.
```sh
┌──(razali㉿razali)-[~/Documents/Ivy/Finals/crypto]
└─$ file flag.enc          
flag.enc: data

It seems like a gibberish file.                                                                                                                                                                                                                                             
┌──(razali㉿razali)-[~/Documents/Ivy/Finals/crypto]
└─$ cat flag.enc           
���>����`

AJW:�AW��J�`����

>ϩ��                                                                                                                                                                                                                                             
┌──(razali㉿razali)-[~/Documents/Ivy/Finals/crypto]
└─$ xxd flag.enc 
00000000: cfe4 4108 c73e 8bcf 06ea 9c60 0a0a 4106  ..A..>.....`..A.
00000010: 4a57 3a9c 0641 579a ea06 4a9c 6086 06cf  JW:..AW...J.`...
00000020: 1606 16c7 cf0a 0a06 3ecf a99c d7         ........>....

```

Since the question wants us to manually crack the file, i'm pretty sure its either `rot` based cipher or perhaps
a `substitution` cipher.

I know that the flag has the format of `ivyctf{...}`.

Lets look at the hex position of `{`, it has a value of `8b`.
The position of `}` has the value of `d7`. Thus its definitely not a rot based cipher as i expected them to be 1 byte apart but `8b` and `d7` are too far apart.

So I did a script to guess the flag using `substitution` cipher.

Firstly, to open the file


```py

file = open('flag.enc', 'rb').read()

```

Next I converted it to hex.

```py

bytes_list = []
for byte in file:
    value = ord(byte)
    hex_value = hex(value)[2:]
    hex_value = hex_value if len(hex_value) == 2 else '0'+hex_value
    bytes_list.append(hex_value)
	
```

I also wanted to know the number of occurances of each hex value, just to get an overall
understanding of which character appears the most.

```py
occurances = {}

for byte in bytes_list:
    if byte in occurances:
        occurances[byte] = occurances[byte] + 1
    else:
        occurances[byte] = 1


import pprint

pprint.pprint(occurances)
```

Finally, I created a loop to allow me to replace hex values to thier guessed letter.

```py
while True:
    print("The flag is now ")
    print(''.join(bytes_list))
    byte = raw_input("Which byte do you want to replace: ")
    replacement = raw_input("What is the replacement character? [a-z_{}]: ")
    bytes_list = [b if b != byte else replacement for b in bytes_list]

```

Let's run the script. It first displays the occurances.
```sh
┌──(razali㉿razali)-[~/…/Ivy/Finals/crypto/headcracker]
└─$ python cracker.py
{'06': 7,
 '08': 1,
 '0a': 4,
 '16': 2,
 '3a': 1,
 '3e': 2,
 '41': 3,
 '4a': 2,
 '57': 2,
 '60': 2,
 '86': 1,
 '8b': 1,
 '9a': 1,
 '9c': 4,
 'a9': 1,
 'c7': 2,
 'cf': 5,
 'd7': 1,
 'e4': 1,
 'ea': 2}
 ```
 Since the flag starts with `ivyctf{...}`, the `...` could be [a-z] and underscore.
 Thus i predicted the highest occurance to be an underscore.
 
 ```
The flag is now 
cfe44108c73e8bcf06ea9c600a0a41064a573a9c0641579aea064a9c608606cf160616c7cf0a0a063ecfa99cd7
Which byte do you want to replace: 06
What is the replacement character? [a-z_{}]: _
The flag is now 
cfe44108c73e8bcf_ea9c600a0a41_4a573a9c_41579aea_4a9c6086_cf16_16c7cf0a0a_3ecfa99cd7
```
Then i proceeded to fill in `ivyctf{}`.

```
Which byte do you want to replace: cf
What is the replacement character? [a-z_{}]: i
The flag is now 
ie44108c73e8bi_ea9c600a0a41_4a573a9c_41579aea_4a9c6086_i16_16c7i0a0a_3eia99cd7
Which byte do you want to replace: e4
What is the replacement character? [a-z_{}]: v
The flag is now 
iv4108c73e8bi_ea9c600a0a41_4a573a9c_41579aea_4a9c6086_i16_16c7i0a0a_3eia99cd7
Which byte do you want to replace: 41
What is the replacement character? [a-z_{}]: y
The flag is now 
ivy08c73e8bi_ea9c600a0ay_4a573a9c_y579aea_4a9c6086_i16_16c7i0a0a_3eia99cd7
Which byte do you want to replace: 08
What is the replacement character? [a-z_{}]: c
The flag is now 
ivycc73e8bi_ea9c600a0ay_4a573a9c_y579aea_4a9c6086_i16_16c7i0a0a_3eia99cd7
Which byte do you want to replace: c7
What is the replacement character? [a-z_{}]: t
The flag is now 
ivyct3e8bi_ea9c600a0ay_4a573a9c_y579aea_4a9c6086_i16_16ti0a0a_3eia99cd7
Which byte do you want to replace: 3e
What is the replacement character? [a-z_{}]: f
The flag is now 
ivyctf8bi_ea9c600a0ay_4a573a9c_y579aea_4a9c6086_i16_16ti0a0a_fia99cd7
Which byte do you want to replace: 8b
What is the replacement character? [a-z_{}]: {
The flag is now 
ivyctf{i_ea9c600a0ay_4a573a9c_y579aea_4a9c6086_i16_16ti0a0a_fia99cd7
Which byte do you want to replace: d7
What is the replacement character? [a-z_{}]: }
The flag is now 
ivyctf{i_ea9c600a0ay_4a573a9c_y579aea_4a9c6086_i16_16ti0a0a_fia99c}
```

Notice the `i16`, since its only 2 letters, it should either be `is` or `it`.
Let's try `is`.

```
Which byte do you want to replace: 16
What is the replacement character? [a-z_{}]: s
The flag is now 
ivyctf{i_ea9c600a0ay_4a573a9c_y579aea_4a9c6086_is_sti0a0a_fia99c}
```

Notice `sti0a0a`, its a 4 letter word `sti**` where the last 2 character are the same. I guessed it as `still`.

```
Which byte do you want to replace: 0a
What is the replacement character? [a-z_{}]: l
The flag is now 
ivyctf{i_ea9c60lly_4a573a9c_y579aea_4a9c6086_is_still_fia99c}
```
Next i noticed the 4 letter word which starts with `y`, `y579aea`. I guessed it as `your`.

```
Which byte do you want to replace: 57
What is the replacement character? [a-z_{}]: o
The flag is now 
ivyctf{i_ea9c60lly_4ao3a9c_yo9aea_4a9c6086_is_still_fia99c}
Which byte do you want to replace: 9a
What is the replacement character? [a-z_{}]: u
The flag is now 
ivyctf{i_ea9c60lly_4ao3a9c_youea_4a9c6086_is_still_fia99c}
Which byte do you want to replace: ea
What is the replacement character? [a-z_{}]: r
The flag is now 
ivyctf{i_r9c60lly_4ao3a9c_your_4a9c6086_is_still_fia99c}
```

Next I noticed the 6 letter word, `r9c60lly`, which looks like `really`.

```
Which byte do you want to replace: 9c
What is the replacement character? [a-z_{}]: e
The flag is now 
ivyctf{i_re60lly_4ao3ae_your_4ae6086_is_still_fia9e}
Which byte do you want to replace: 60
What is the replacement character? [a-z_{}]: a
The flag is now 
ivyctf{i_really_4ao3ae_your_4aea86_is_still_fia9e}

```

Next I noticed `4aea86`. `*ea*`. Since the title of the excercise is `HeadCracker`, i guessed it as `head`.

```
Which byte do you want to replace: 4a
What is the replacement character? [a-z_{}]: h
The flag is now 
ivyctf{i_really_ho3ae_your_hea86_is_still_fia9e}
Which byte do you want to replace: 86
What is the replacement character? [a-z_{}]: d
The flag is now 
ivyctf{i_really_ho3ae_your_head_is_still_fia9e}
```.

With that the rest of it is pretty much self explanatory.
```
Which byte do you want to replace: 3a
What is the replacement character? [a-z_{}]: p
The flag is now 
ivyctf{i_really_hope_your_head_is_still_fia9e}
Which byte do you want to replace: a9
What is the replacement character? [a-z_{}]: n
The flag is now 
ivyctf{i_really_hope_your_head_is_still_fine}
```

This was fun to solve!
