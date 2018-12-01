# Hawk writeups by Seyptoo.

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/48/6/1543657344-capture-du-2018-12-01-10-41-55.png)](https://hackthebox.eu/)

Informations
----
    Ip : 10.10.10.102       Created : mrh4sh
    Level : Easy            Base Points : 30
    
Nmap Scan
----
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
    
**[*] We have 4 open ports, 21, 22, 80 and 8082.**


Check Version
----
[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/48/6/1543658376-capture-du-2018-12-01-10-59-23.png)](https://hackthebox.eu)
**We can see that we have 2 HTTP 
servers and an FTP server which we can 
access anonymously.**

FTP Access and transfert
----
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

**We have access to the FTP server, we can see that there is a hidden file and we transfer it to our physical machine.**

