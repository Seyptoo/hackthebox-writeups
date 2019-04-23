# Able writeups by Seyptoo.

Scan TCP
----

Let's start by doing a port scan.

    root@Seyptoo:~/htb/wizard/box/Able# nmap -sT -p 1-65535 -oA nmap/able 192.168.0.21

    Starting Nmap 7.01 ( https://nmap.org ) at 2019-04-23 20:19 CEST
    Nmap scan report for 192.168.0.21
    Host is up (0.0016s latency).
    Not shown: 65533 closed ports
    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http
    MAC Address: 08:00:27:16:E2:52 (Oracle VirtualBox virtual NIC)

    Nmap done: 1 IP address (1 host up) scanned in 3.22 seconds
    root@Seyptoo:~/htb/wizard/box/Able# nmap -sT -p22,80 -sC -sV -oA nmap/able 192.168.0.21

    Starting Nmap 7.01 ( https://nmap.org ) at 2019-04-23 20:20 CEST
    Nmap scan report for 192.168.0.21
    Host is up (0.00049s latency).
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 47:2c:be:2f:88:6f:21:72:ff:a3:0b:3d:12:f0:25:72 (RSA)
    |_  256 a3:ab:98:7a:f4:d0:54:17:13:3a:05:7e:53:e6:bc:18 (ECDSA)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html; charset=UTF-8).
    MAC Address: 08:00:27:16:E2:52 (Oracle VirtualBox virtual NIC)
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 8.86 seconds
    
As you can see, there are two open ports ssh and http.

Scan UDP
----

We will also do a UDP scan on the server. As you can see below there is the SNMP protocol that is open, and public so we can enumerate afterwards.

    root@Seyptoo:~/htb/wizard/box/Able# nmap -sU -oA -sC -sV nmap/udp 192.168.0.21 --min-rate 10000
    Starting Nmap 7.01 ( https://nmap.org ) at 2019-04-23 20:25 CEST
    Nmap scan report for 192.168.0.21
    Host is up (0.0011s latency).
    PORT    STATE SERVICE VERSION
    161/udp open  snmp    SNMPv1 server; net-snmp SNMPv3 server (public)
    | snmp-hh3c-logins: 
    |_  baseoid: 1.3.6.1.4.1.25506.2.12.1.1.1
    | snmp-info: 
    |   enterprise: net-snmp
    |   engineIDFormat: unknown
    |   engineIDData: 6c5ddc433219bf5c00000000
    |   snmpEngineBoots: 11
    |_  snmpEngineTime: 19m20s
    | snmp-sysdescr: Linux Able 4.15.0-47-generic #50-Ubuntu SMP Wed Mar 13 10:44:52 UTC 2019 x86_64
    |_  System uptime: 19m21.44s (116144 timeticks)
    MAC Address: 08:00:27:16:E2:52 (Oracle VirtualBox virtual NIC)
    Service Info: Host: Able

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 2.43 seconds

