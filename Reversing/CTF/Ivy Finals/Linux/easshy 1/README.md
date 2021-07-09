easshy
150
ssh ctf@ctf.dart.com.sg -p 2310

Password: gqeoczoksv

```sh
                                                                                                                        
┌──(razali㉿razali)-[~]
└─$ ssh ctf@192.168.40.199 -p 2310
ctf@192.168.40.199's password: 

Permission denied, please try again.
ctf@192.168.40.199's password: 
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 5.4.0-51-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

ctf@easshy:~$ pwd
/home/ctf
ctf@easshy:~$ ls
flagchecker
ctf@easshy:~$ file flagchecker 
flagchecker: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=3e1765451e74cafe7c3d53ec7c03def4f8fb9101, for GNU/Linux 3.2.0, stripped
ctf@easshy:~$ ./flagchecker 
Good job, you have the flag!
ctf@easshy:~$ ls
flagchecker

```

```sh
D:\My Documents\Writeups\Reversing\CTF\Ivy Finals\Linux\easshy 1>scp -P 2310 ctf@192.168.40.199:./flagchecker .
ctf@192.168.40.199's password:
flagchecker                                                                           100%   13KB   1.2MB/s   00:00

```



