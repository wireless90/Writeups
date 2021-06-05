# Size Might Matter

Get the [apk](https://github.com/wireless90/AndroidInternalsCTF/tree/main/Size%20Might%20Matter) here.

- Find the flag by giving the correct argument to a.out. 
- Do not reverse the decrypt function or modify the executable.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/sizeMightMatter]
└─$ chmod +x a.out    
                                                                                                                                                                                                                                             
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/sizeMightMatter]
└─$ ./a.out 
zsh: exec format error: ./a.out
                                                                                                                                                                                                                                             
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/sizeMightMatter]
└─$ file a.out                                                                                                                                                                                                                         126 ⨯
a.out: ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /system/bin/linker, with debug_info, not stripped
```

As this is an `arm` executable, we need to run it in android. I used adb to push it to my android device and run it.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/sizeMightMatter]
└─$ adb devices                                                                                                                                                                                                                          1 ⨯
List of devices attached
03abf751093c269f        device

```
Check that your android device is connected using the above command.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/sizeMightMatter]
└─$ adb push a.out /data/local/tmp
a.out: 1 file pushed. 0.2 MB/s (44352 bytes in 0.179s)
```
Push the executable `a.out` into the temp folder of the android device.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/sizeMightMatter]
└─$ adb shell                     
shell@hammerhead:/ $ su
root@hammerhead:/ # cd /data/local/tmp
root@hammerhead:/data/local/tmp # ./a.out                                      
usage: ./a.out <arg>
```

Seems like we need to feed it an argument

```sh
root@hammerhead:/data/local/tmp # ./a.out aaaa
Value less or equal 0 is not allowed.
root@hammerhead:/data/local/tmp # ./a.out 5555                                 
Value 5555 defined.
root@hammerhead:/data/local/tmp # ./a.out 5555555555555555555555555555555555555555555555555555555555555555555
Value 65535 defined.
```

Seems like the maximum "defined" was up to `65535` which is `0xffff` 2 bytes long. We still do not have much clue on what to do  to get the flag.

So lets open the executable in IDA and perform some static analysis.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pcw8bxeuxe50pdff9lz3.png)

I have highlighted the block of code in green which indicates the path that we need to take to decrypt and print the flag.



Comments are very important when performing static analysis. So we will look at each block and try to figure what what is being done and ensure to put in comments in IDA.

Lets work backwards.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rwlwhahuo3242trb1oaa.png)

So our target is to reach the green block. Lets take a look at the red block of code. 

```asm
LDRH R0, [R11 ,#var_E]
```

`LDRH` loads the last 2 bytes of the right operand into the left operand. 

Note: As this is a 32-bit executable, these are 4 byte registers thus `LDRH` would take half of it, `2 bytes`.

It then checks if this is 0. If its 0, we get the flag! Remember earlier when we did the large `5555555555....` input, we got 0xffff (2bytes) as `"defined"`.

What if we crafted an input of `0x10000`, where the last 2 bytes are `0x0000`?

Let's try that.

`0x10000` is 65536 in decimal.

```sh
root@hammerhead:/data/local/tmp # ./a.out 65536                                
You did it!
The flag is: "1337"
```

And we got the flag!

I learnt that its better not to reverse the whole binary sometimes. Just working backwards first would help.