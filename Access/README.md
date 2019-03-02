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
[SNIP]
 
 
