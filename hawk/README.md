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
    Discovered open port 5435/tcp on 10.10.10.102
    
   
