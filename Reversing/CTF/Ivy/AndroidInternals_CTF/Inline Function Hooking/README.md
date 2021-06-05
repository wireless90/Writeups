# Inline Function Hooking

Get the [executable here](https://github.com/wireless90/AndroidInternalsCTF/tree/main/Inline%20Function%20Hooking)

- Add a hook at the end of the `pick_number` function. 
- You can save your hook at `some_space` function. 
- The hook that you add must print the return value of `pick_number` function. 
- Then, give this number as an input to the program in order to reveal the flag. 
- **Do not edit any other part of the program or try to reverse decrypt function.**

Lets try to run the application, `a.out`.
```sh
root@hammerhead:/data/local/tmp # ./a.out           
Enter number: 123
wrong number :(
```

So it looks like we need to hook the function `pick_number` and get the number to solve this challenge.

Before we start writing the hook, we need to know where to hook?

The instruction says to:
> Add a hook at the end of the pick_number function.

Lets open up the binary in IDA for static analysis and find the address of the end of the `pick_number` function.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2jix9edapc1iz7uby905.png)
 

We can see that the end of the `pick_number` function lies around the address `0x000009D0`.

We can also see that the instruction at that address is `POP {R11, PC}`. Remember this, we will be referring to this later.

Lets ensure that is the right address by using `gdb` to perform dynamic analysis.

We will be using `gdbserver` in our android and debug the binary `a.out` remotely using our `gdb-multiarch` client on our host.

In our android, lets feed the program some random number

```sh
root@hammerhead:/data/local/tmp # ./gdbserver localhost:6666 a.out 1234
Process a.out created; pid = 12547
Listening on port 6666

```

In our host, we need to port forward port 6666 first.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/inlineFunctionHooking]
└─$ adb forward tcp:6666 tcp:6666 

                                                                                                                                                                             
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/inlineFunctionHooking]
└─$ gdb-multiarch

gef➤  target remote localhost:6666
Remote debugging using localhost:6666
warning: Architecture rejected target-supplied description
Reading /data/local/tmp/a.out from remote target...
warning: File transfers from remote targets can be slow. Use "set sysroot" to access files locally instead.
Reading /data/local/tmp/a.out from remote target...
Reading symbols from target:/data/local/tmp/a.out...
Reading /system/bin/linker from remote target...
Reading /system/bin/linker from remote target...
Reading symbols from target:/system/bin/linker...

gef➤  

```

We have connected to our binary `a.out`.

Lets print the address of `pick_number`. 

```sh
gef➤  p &pick_number
$1 = (<text variable, no debug info> *) 0x2a000980 <pick_number>

```

IDA said that the end of the `pick_number` function is at `0x000009D0` while GDB says it starts at `0x2a000980`.

From this we can deduce that the end of the `pick_number` function is at `0x2A0009D0`.

Lets verify it by printing out the instruction at that address.

```sh
gef➤  x/i 0x2a0009d0
   0x2a0009d0 <pick_number+80>: pop     {r11, pc}
```

This is what IDA showed as well, so this is the right address.

We are going to overwrite this instruction with a `branch` instruction. We want to branch to our shellcode.

The tips for this exercise was to put our shellcode at
> You can save your hook at `some_space` function.

Thus, we need to find out the address of `some_space` function. Lets do this using `GDB` as well.

```sh
gef➤  p &some_space
$1 = (<text variable, no debug info> *) 0x2a0009e4 <some_space>
```
Great, so we know the place to put our shell code is at `0x2a0009e4`.

We also, as stated previously, want to put a jump instruction to our shell code therefore replacing `0x2a0009d0 <pick_number+80>: pop     {r11, pc}`.

So in general, our hooking shell code is gonna look like.

# Shellcode Header
1) branch to shellcode

# Shellcode
2) Save registers that we going to use
3) Create a file to save return value from `pick_number`
4) Write the return value to the file
5) Close the file

# ShellCode Footer
6) Pop back the registers that were previously saved
7) Write the original instruction that was replaced, `pop {r11, pc}`
8) Jump back to the original function 

Our `hook.s` looks like

```nasm
.data
shellcodeHeader:
//Place at 0x2A0009D0
        b shellcode

comeBackHereAfterEverything:


.text
//Place at 0x2A0009E4
shellcode:
        push {r1, r2}
        push {r0} //R0 Contains the number

        //Create file
        mov r7, #8 //creat syscall
        mov r1, #1 //write permission
        adr r0, file_name
        svc #0

        push {r0} //contains the FD

        //WRITE
        mov r7, #4 //write syscall
        mov r2, #4 //4 bytes
        add r1, sp, #4 //buff
        svc #0 // call write

        //CLOSE
        pop {r0} //pops the fd
        mov r7, #6
        svc #0

Override:
        pop {r0}
        pop {r1, r2}

        //original instruction
        pop {r11, pc}
        b comeBackHereAfterEverything

        file_name: .asciz "answer"
                                                    
```

Thus we will save the number into a file called `answer`.

We can't just compile it now. We need as linker script to tell the linker which section of the code goes to which part of the memory.

Our `.data` section is going to be at address `0x2A0009D0`.

Our `.text` section is going to be at address `0x2A0009E4`.


The linker script, `linker_script.ld` thus looks like
```nasm
SECTIONS
{
  . = 0x2A0009D0;
  .data : { *(.data) }

  . = 0x2A0009E4;
  .text : { *(.text) }
}
```

Lets compile it. To make it easier, I created my commands into a shellscript file.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/inlineFunctionHooking]
└─$ vim commands.sh
                           
export ndk=/home/razali/Downloads/android-ndk-r21e/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/arm-linux-androideabi/bin

$ndk/as hook.s -o hook.o
$ndk/ld hook.o -T linker_script.ld -o hook
$ndk/objcopy -O binary --only-section=.data hook branch.bin
$ndk/objcopy -O binary --only-section=.text hook shellcode.bin


echo "==============XXD OUTPUT OF BRANCH======================"
echo "==============PUT IT AT 0x2A0009D0 =========================="
xxd branch.bin



echo "==============XXD OUTPUT OF Shellcode======================"
echo "==============PUT IT AT 0x2A0009E4 =========================="
xxd shellcode.bin

```

```sh
──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/inlineFunctionHooking]
└─$ ./commands.sh
==============XXD OUTPUT OF BRANCH======================
==============PUT IT AT 0x2A0009D0 ==========================
00000000: 0f00 00ea                                ....
==============XXD OUTPUT OF Shellcode======================
==============PUT IT AT 0x2A0009E4 ==========================
00000000: 0600 2de9 0400 2de5 0870 a0e3 0110 a0e3  ..-...-..p......
00000010: 3000 8fe2 0000 00ef 0400 2de5 0470 a0e3  0.........-..p..
00000020: 0420 a0e3 0410 8de2 0000 00ef 0400 9de4  . ..............
00000030: 0670 a0e3 0000 00ef 0400 9de4 0600 bde8  .p..............
00000040: 0088 bde8 ddff ffea 616e 7377 6572 0000  ........answer..

```

Now its time to patch our program. We are going to input all the above bytes at their respective addresses.

Open `a.out` using `IDA`.

Press the hotkey, `g`, which opens up the `Jump to Address` prompt.
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y0rbie6qi0oo2aijdby6.png)

Put the address  `0x000009D0` or `9d0` for short, and it will take you to the address where we want to put our `branch.bin`.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/df8rpybh2ampj2rzg4ur.png)

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5tzwkbb6eu934zfkvzpe.png)

Click on `Edit` > `Patch program` > `Change Byte`.

 
 ![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/iaqrlx15t0rvht12qfo5.png)

The xxd output suggested us to patch the bytes to `0F 00 00 EA` . But it seemed like it did not hit the shellcode location properly. I adjusted it slightly to `03 00 00 EA` and it worked, as you can see from the image above. It points to the `some_space` function directly.

Next, go to the `some_space` function and patched the bytes to the xxd output of `shellcode.bin`.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ppaxsmz9bejlsw3jydu3.png)


Once done, we are going to apply the patches to the file.
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n8d17pdjk5wgjnphr68o.png)
 
 Next, we will push the patched program to our android device.
```sh
──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/inlineFunctionHooking]
└─$ adb push a.out /data/local/tmp
a.out: 1 file pushed. 0.2 MB/s (44552 bytes in 0.185s)
```

I will then launch `a.out`

```sh
root@hammerhead:/data/local/tmp # chmod +x a.out                                                                 
root@hammerhead:/data/local/tmp # ./a.out                                                                            
Enter number:      
```

`a.out` will have now picked a number and store it in our file `answer`.

From my host , i will use adb to `cat` out the file..

```sh
──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/inlineFunctionHooking]
└─$ adb shell "su -c cat /data/local/tmp/answer" > answer
                                                                                                                     
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/inlineFunctionHooking]
└─$ xxd answer                                           
00000000: 807f 6cfc    
```

Great, now this is probably a signed integer in little-endian format. I went online to convert it.

The website I went to was [here](https://www.binaryconvert.com/result_unsigned_int.html?hexadecimal=FC6C7F80).

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2v4lxcg40v8ewugrwci1.png)

Then I got the flag.

```sh
root@hammerhead:/data/local/tmp # ./a.out                                                                            
Enter number: 4234968960                                                                                             
You did it!
The flag is: "peter_pan"
```
 