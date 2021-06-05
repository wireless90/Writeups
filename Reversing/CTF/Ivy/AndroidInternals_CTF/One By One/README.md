# Off by One

Get the [executable here](https://github.com/wireless90/AndroidInternalsCTF/tree/main/One%20By%20One)

# Instructions

- Give the program the correct argument so it will print the flag. 
- Do not reverse the decrypt function or modify the program.


# Let's Begin

Let's take a look what type of file it is.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/offByOne]
└─$ file a.out
a.out: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, with debug_info, not stripped
```

It is an arm file, so let's push it to our android device.

```sh
──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/offByOne]
└─$ adb push a.out /data/local/tmp
* daemon not running; starting now at tcp:5037
* daemon started successfully
a.out: 1 file pushed. 0.2 MB/s (3392956 bytes in 13.310s)

```

Next, try to run it in our android device.

```sh
126|root@hammerhead:/data/local/tmp # chmod +x a.out
root@hammerhead:/data/local/tmp # ./a.out
usage: ./a.out <argument>
```

It requires an argument. I proceeded to give it a short and a long argument.

```sh
root@hammerhead:/data/local/tmp # ./a.out aaaa
You failed :(
root@hammerhead:/data/local/tmp # /a.out aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa                             
You failed :(

```

Both resulted in a failure.

Next, let's proceed to perform our static analysis using `IDA`.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b8l09eft80t16l3hk4si.png)
 
It seems like a very small program. So let's begin reversing from the start.

When performing static analysis, it is best to put lots of comments for each block of code.

I will be showing both `IDA` view and `nasm markdown` view as it might be more clearer.

Let's look at the beginning of the `main` function.
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4dat0yq4h2ch0m8zfrqi.png)


```nasm
; int __cdecl main(int argc, const char **argv, const char **envp)
EXPORT main
main

var_124= -0x124
var_120= -0x120
var_11C= -0x11C
var_115= -0x115
var_15= -0x15
var_14= -0x14
var_10= -0x10
var_C= -0xC

PUSH            {R4,R5,R11,LR}
ADD             R11, SP, #8
SUB             SP, SP, #0x120
MOV             R2, #0
STR             R2, [R11,#var_C]
STR             R0, [R11,#var_10]
STR             R1, [R11,#var_14]
LDR             R0, [R11,#var_10]
CMP             R0, #2
BGE             loc_857C
```
 
We know that,
`R0` - represents `argc`
`R1` - represents `argv`
`R2` - represents `envp`

Hence, lets rename our variables and add comments. The above block of code now looks like,

```nasm
; Attributes: bp-based frame

; int __cdecl main(int argc, const char **argv, const char **envp)
EXPORT main
main

var_124= -0x124
var_120= -0x120
var_11C= -0x11C
var_115= -0x115
var_15= -0x15
argv= -0x14
argc= -0x10
envp= -0xC

PUSH            {R4,R5,R11,LR}
ADD             R11, SP, #8
SUB             SP, SP, #0x120
MOV             R2, #0
STR             R2, [R11,#envp]
STR             R0, [R11,#argc]
STR             R1, [R11,#argv]
LDR             R0, [R11,#argc]
CMP             R0, #2  ; Checking if argc is >=2
BGE             loc_857C
```

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hyz14kpdnwqcmi97zk4v.png)
Since it branches based on whether we put in arguments, in our case, we are supplying `1` argument, which makes the `argc` count `2`. Hence the program branches to the right.

Lets take a look at the block on the right.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3objga8g68qxajek6s2d.png)

```nasm
loc_857C
LDR             R0, =(byte_6325B - 0x8588)
ADD             R0, PC, R0 ; byte_6325B
LDRB            R0, [R0]
STRB            R0, [R11,#var_15]
LDR             R0, [R11,#argv]
LDR             R0, [R0,#4] ; s
BL              strlen
CMP             R0, #0x100
BLS             loc_85BC
``` 

Reversing it produces, 
```nasm
This code executes when there are atleast 1 cmd line argument

loc_857C
LDR             R0, =(byte_6325B - 0x8588)
ADD             R0, PC, R0 ; byte_6325B
LDRB            R0, [R0]
STRB            R0, [R11,#var_15]
LDR             R0, [R11,#argv] ;
                        ; The below line gets the first argument
LDR             R0, [R0,#4] ; s
BL              strlen  ; gets the first argument and performs a strlen on it
CMP             R0, #0x100 ; Length of the first argument is compared against 256
BLS             loc_85BC ; Branch to the right if LOWER OR SAME than 256
```

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ns67c70ojetsvoiifib9.png)

Looking at the code on the left block, it says `Length higher than 256 is not allowed`. What if the length is `256`? We need to test the edge cases.

Let's now take a look at the block on the right.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/a9hxavlwkixz7k5fn55p.png)

```nasm
loc_85BC
ADD             R0, SP, #0x128+var_115
LDR             R1, [R11,#argv]
LDR             R1, [R1,#4]
BL              strcpy
LDRB            R1, [R11,#var_15]
CMP             R1, #0
BNE             loc_8604
``` 

Reversing it gives,

```nasm
Copies the first argument to the destination buffer

loc_85BC                ; dest to strcpy
ADD             R0, SP, #0x128+destBuffer
LDR             R1, [R11,#argv]
LDR             R1, [R1,#4] ; LOAD THE FIRST ARGUMENT as src to strcpy
BL              strcpy
LDRB            R1, [R11,#var_15]
CMP             R1, #0
BNE             loc_8604 ; if R1 is zero, we will get the flag!
```
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r9i06gwwlr10ozsfmgqr.png)
 
We can see that if R1 is `Not Equal` to `0`, we will fail to the right. Hence R1 has to be 0 in order for us to get the flag.

R1 gets its value from the stack variable `var_15`.
`var_15` gets its value from the previous block, from a `readonly` memory location named `=(byte_6325B - 0x8588)`. 

Let's hover our mouse over it to see what the `.rodata` contains.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9qfduag8ydetrucwwv2n.png)
 
It simply contains the number, `1`.

Hence, we know that `var_15` will contains the number `1` but we somehow need to make it become `0` in order for us to get the flag.

Lets take a look at the stack location of the variable, right at the start of main.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ijcmt431dwdzzmc91nej.png)

The code we looked at allows a max of `256` bytes to be written and the 2 variables are exactly 256 bytes from each other. Hence we need at least 257 characters to override into `var_15`. Moreover, the character that overrides `var_15` has to be 0 in order for us to get the flag.

The flaw here relies on `strcpy`. If we were to pass 256 characters, `strcpy` copies all 256 characters into the `buffer` and it also adds a `NULL`, `\0`, into the next position, the 257th position, to terminate the string. This 257th position happens to be our `var_15`.

Hence from our host machine, we can use python to quickly generate a string of length `256`.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/offByOne]
└─$ python -c 'print "a"*256'                            
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Then we can copy this string to our android.

```sh
root@hammerhead:/data/local/tmp # ./a.out aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

You did it!
The flag is: "off_by_one"


```

And we got the flag.