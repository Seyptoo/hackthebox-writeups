# Curling writeups by Seyptoo.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/13/6/1553953753-capture-du-2019-03-30-14-49-00.png)]

Nmap Scan
----

    Starting Nmap 7.01 ( https://nmap.org ) at 2019-03-30 14:55 CET
    Nmap scan report for 10.10.10.150
    Host is up (0.045s latency).
    Not shown: 998 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 8a:d1:69:b4:90:20:3e:a7:b6:54:01:eb:68:30:3a:ca (RSA)
    |_  256 9f:0b:c2:b2:0b:ad:8f:a1:4e:0b:f6:33:79:ef:fb:43 (ECDSA)
    80/tcp open  http?
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 193.48 seconds
    
Alors concrètement il y'a 2 ports ouvert le SSH pour le 22 et le HTTP pour le 80. Nous allons un peu énumérer sur le serveur web.

HTTP
----

Quand nous envoyions une rêquete HTTP avec curl, on peut constater que il y'a un fichier spécial nommé secret.txt. Nous allons essayer de lire ce fichier texte.

    root@Computer:~/htb/writeup/Curling# curl http://10.10.10.150
    [...SNIP...]
    </body>
      <!-- secret.txt -->
    </html>
    root@Computer:~/htb/writeup/Curling# curl http://10.10.10.150/secret.txt
    Q3VybGluZzIwMTgh
    root@Computer:~/htb/writeup/Curling# curl http://10.10.10.150/secret.txt -s|base64 -d
    Curling2018!
    
Ceci ressemble à un mot de passe, probablement pour le CMS. Il y'a aussi un nom d'utilisateur dans un article ça pourrais nous servir.

[![forthebadge made-with-python](https://cdn.discordapp.com/attachments/556442801085218827/561556044367527979/unknown.png)]

J'ai pas encore lancé de gobuster je vais lancé ça automatiquement.

Gobuster
----
    root@seyptoo-Aspire-E5-721:~/htb/writeup/Curling# gobuster -w /usr/share/wordlist/directory-list-2.3-medium.txt -u http://10.10.10.150 -o output-gobuster.log

    Gobuster v1.4.1              OJ Reeves (@TheColonial)
    =====================================================
    =====================================================
    [+] Mode         : dir
    [+] Url/Domain   : http://10.10.10.150/
    [+] Threads      : 10
    [+] Wordlist     : /usr/share/wordlist/directory-list-2.3-medium.txt
    [+] Output file  : output-gobuster.log
    [+] Status codes : 200,204,301,302,307
    =====================================================
    /images (Status: 301)
    /media (Status: 301)
    /templates (Status: 301)
    /modules (Status: 301)
    /bin (Status: 301)
    /plugins (Status: 301)
    /includes (Status: 301)
    /language (Status: 301)
    /components (Status: 301)
    /cache (Status: 301)
    /libraries (Status: 301)
    /tmp (Status: 301)
    /layouts (Status: 301)
    /administrator (Status: 301)

 Nous avons beaucoup de dossiers, on va s'intéréssé à la page d'administration, le CMS utilisé est Joomla. J'ai essayer avec plusieurs utilisateur notamment avec admin, administrator etc.. et finalement l'utilisateur est floris et le mot de passe est Curling2018!.
 
 Username : floris
 Password : Curling2018
 
 

  
