# Access writeups by Seyptoo.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/12/6/1553333910-capture-du-2019-03-23-10-37-40.png)

Informations
----
    Ip : 10.10.10.111        Created by : felamos
    Level : Medium           Base Points : 20

Scan nmap
----
    PORT     STATE SERVICE     VERSION
    22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 87:7b:91:2a:0f:11:b6:57:1e:cb:9f:77:cf:35:e2:21 (RSA)
    |_  256 b7:9b:06:dd:c2:5e:28:44:78:41:1e:67:7d:1e:b7:62 (ECDSA)
    139/tcp  open  netbios-ssn Samba smbd 3.X (workgroup: FROLIC)
    445/tcp  open  netbios-ssn Samba smbd 3.X (workgroup: FROLIC)
    9999/tcp open  http        nginx 1.10.3 (Ubuntu)
    |_http-server-header: nginx/1.10.3 (Ubuntu)
    |_http-title: Welcome to nginx!
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Host script results:
    |_nbstat: NetBIOS name: FROLIC, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
    | smb-os-discovery: 
    |   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
    |   Computer name: frolic
    |   NetBIOS computer name: FROLIC
    |   Domain name: 
    |   FQDN: frolic
    |_  System time: 2019-03-23T14:57:44+05:30
    | smb-security-mode: 
    |   account_used: guest
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    |_smbv2-enabled: Server supports SMBv2 protocol

Alors il y'a 4 ports open, le 22 pour le SSH, le 139 et 445 pour le Samba, et le port 9999 pour le HTTP qui tourne sous nginx. Une enumération par défault.

HTTP 9999
----
N'oubliez pas d'attribuer le domaine sur le fichier /etc/hosts. Pour justement avoir accéder à la box et au serveur HTTP sans problème.
[![forthebadge made-with-python](https://media.discordapp.net/attachments/556442801085218827/558951107431235596/unknown.png)

    root@Computer:~/htb/box/Frolic/gobuster# /usr/bin/gobuster -w /usr/share/wordlist/directory-list-2.3-medium.txt -u http://forlic.htb:9999/ -x php,html -o output_file

    Gobuster v1.4.1              OJ Reeves (@TheColonial)
    =====================================================
    =====================================================
    [+] Mode         : dir
    [+] Url/Domain   : http://forlic.htb:9999/
    [+] Threads      : 10
    [+] Wordlist     : /usr/share/wordlist/directory-list-2.3-medium.txt
    [+] Output file  : output_file
    [+] Status codes : 204,301,302,307,200
    [+] Extensions   : .php,.html
    =====================================================
    /admin (Status: 301)
    /test (Status: 301)
    /dev (Status: 301)
    /backup (Status: 301)

Comme vous pouvez le voir il y'a un dossier /admin, /test, /backup et /dev, nous allons un peu regarder le dossier /admin de plus près.

[![forthebadge made-with-python](https://cdn.discordapp.com/attachments/556442801085218827/558962528311443466/unknown.png)
Comme vous pouvez le voir, il y'a un fichier javascript /login.js donc dans ce fichier il y'a sans doute le nom d'utilisateur et le mot de passe.





