# Access writeups by Seyptoo.

[![forthebadge made-with-python](https://image.noelshack.com/fichiers/2019/09/6/1551530466-capture-du-2019-03-02-13-40-56.png)](https://image.noelshack.com/fichiers/2019/09/6/1551530466-capture-du-2019-03-02-13-40-56.png)

Informations
----
    Ip : 10.10.10.98       Created by : egre55
    Level : Very easy            Base Points : 20
    
Scan Nmap
----
    PORT   STATE SERVICE VERSION
    21/tcp open  ftp     Microsoft ftpd
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_Can't get directory listing: TIMEOUT
    23/tcp open  telnet?
    80/tcp open  http    Microsoft IIS httpd 7.5
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/7.5
    |_http-title: MegaCorp
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
    
 Après avoir effectué le scan, nous avons 3 ports ouverts, le (21) pour le FTP, le (23) pour le telnet, et le (80) pour le httpd. Le FTP peut être accéder en tant que anonymous donc nous allons essayer d'énumérer.
 
FTP Enumeration
----
Pour la connexion au serveur FTP, l'utilisateur et le mot de passe 'anonymous:anonymous'.

    root@Computer:~/htb/writeup/Access# ftp 10.10.10.98
    Connected to 10.10.10.98.
    220 Microsoft FTP Service
    Name (10.10.10.98:root): anonymous
    331 Anonymous access allowed, send identity (e-mail name) as password.
    Password:
    230 User logged in.
    Remote system type is Windows_NT.
    ftp>
 
 La connexion c'est déroulais avec succès donc essayons de lister les fichiers dans le dossier.

    ftp> ls
    200 PORT command successful.
    125 Data connection already open; Transfer starting.
    08-23-18  08:16PM       <DIR>          Backups
    08-24-18  09:00PM       <DIR>          Engineer
    226 Transfer complete.
    ftp>
    
Comme vous pouvez le voir, il y'a un dossiers Backups et un dossier Engineer. Dans le dossier Backups il y'a un fichier mdb, pour les bases de données, et dans le dossier Engineer il y'a un fichier zip. Donc nous allons transférer c'est fichiers vers notre machine physique avec la commande **mget [file]**, avant de transférer nous devons passer de ASCII à BINAIRE.

    ftp> ls
    200 PORT command successful.
    125 Data connection already open; Transfer starting.
    08-23-18  08:16PM              5652480 backup.mdb
    226 Transfer complete.
    ftp> binary
    200 Type set to I.
    ftp> mget backup.mdb
    mget backup.mdb? y
    200 PORT command successful.
    125 Data connection already open; Transfer starting.
    226 Transfer complete.
    5652480 bytes received in 7.70 secs (716.7322 kB/s)
    ftp> cd ..
    250 CWD command successful.
    ftp> cd Engineer
    250 CWD command successful.
    ftp> ls
    200 PORT command successful.
    125 Data connection already open; Transfer starting.
    08-24-18  12:16AM                10870 Access Control.zip
    226 Transfer complete.
    ftp> mget "Access Control.zip"
    mget Access Control.zip? y
    200 PORT command successful.
    125 Data connection already open; Transfer starting.
    226 Transfer complete.
    10870 bytes received in 0.83 secs (12.7677 kB/s)
    ftp> 

Voilà les fichiers ont été transférer avec succès, sans aucun problème donc nous pouvons quitter le serveur FTP. Et d'énumérer c'est fichiers.

Enumeration MDB
----
