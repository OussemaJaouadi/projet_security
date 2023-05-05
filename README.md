# Flask Kerberos Authentication

## About Project :

This project is a Flask application that uses Kerberos authentication. It is a simple application that allows you to login with your Kerberos credentials and then ..... (to be continued)

## Kerberos :

<hr>

### Introduction : 

Kerberos is a network authentication protocol used to provide secure authentication for client/server applications. It was developed by the Massachusetts Institute of Technology (MIT) in the 1980s and is now widely used in many environments, including corporate networks, academic institutions, and government agencies.

The Kerberos protocol uses a ticket-based system to authenticate users and authorize access to network resources. When a user attempts to access a network resource, the user's credentials are first verified by the Kerberos authentication server. If the credentials are valid, the authentication server issues a ticket-granting ticket (TGT), which the user can use to request a service ticket for a specific network resource.

The service ticket is then used to authenticate the user to the network resource and authorize access. The Kerberos protocol also provides mechanisms for encrypting communication between clients and servers to prevent eavesdropping and other forms of attack.

### How it works :

![Kerberos](./img/Kerberos.png)

1. The Kerberos authentication server verifies the user's credentials and sends a TGT encrypted with the user's secret key.
2. The user decrypts the TGT using their secret key and stores the TGT in memory.
3. The user sends a request to the Kerberos ticket-granting server (TGS) for a service ticket.
4. The TGS verifies the user's TGT and sends a service ticket encrypted with the service's secret key.
5. The user decrypts the service ticket using the TGT and their secret key and sends the decrypted service ticket to the service.
6. The service verifies the service ticket and grants the user access to the requested resource.

## Environment :

<hr>

### OS :

* [Ubuntu 20.04 LTS](/img/https://archive.org/download/ubuntu-20.04-desktop-amd64)

### Language and Framework :

* [Python 3.8.10](/img/https://www.python.org/downloads/release/python-3810/)

* [Flask 2.1.x](/img/https://flask.palletsprojects.com/en/2.1.x/) : micro web framework written in Python

### Configuration :

#### 1. Network :
    
* Network manager :
    ![](/img/NetworkManager.png)
* Create Custom Nat Network :
    ![](/img/CreateNat.png)
* Assign The Network to the VMs :
    ![](/img/Assign.png)
* Get the gateway :
    ![](/img/routeTable.png)
* Fix the IP of each machine :
    ![](/img/fix.png)
> 10.10.10.100 for kdc <br>
> 10.10.10.101 for server
* Disconnect and reconnect to apply settings
* And Finally :
    ![](/img/final.png)

> note those configuration were made originally on kali VM but the kali had many problems .

#### 2. OS update :

```bash
sudo apt update && sudo apt upgrade -y
```

##### 1 DNS(Domain Name Server)

```bash	
sudo nano /etc/hosts
```

And we add (for each machine) :

```bash
10.10.10.100    kdc.projet.tn       kdc
10.10.10.101    server.projet.tn    server
```

Then we set the **hostname** (for each machine) :

|  Machine Name |  hostname |
|---|---|
|  KDC | `sudo hostnamectl set-hostname kdc.projet.tn` |
| Server | `sudo hostnamectl set-hostname server.projet.tn` |

#### 2 Time Synchronization

When the client obtains a ticket from Kerberos, it includes in its message the current time of day. One of the three parts of the response from Kerberos is a timestamp
issued by the Kerberos server.

1. On KDC we install ntp

```bash
sudo apt install ntp -y
```

Then edit the  ``/etc/ntp.conf``  and add the lines below under the  ``# local users may interrogate the ntp server more closely``  section:

```bash
restrict 127.0.0.1
restrict ::1
restrict 10.10.10.100 mask 255.255.255.0
nomodify notrap
server 127.127.1.0 stratum 10
listen on *
```

2. On the server we install ntp & ntpupdate

```bash
sudo apt install ntp ntpdate -y
```

Then edit the  ``/etc/ntp.conf``  and add the lines below under the  ``# local users may interrogate the ntp server more closely``  section:

```bash
pool ntp.ubuntu.com
server 10.10.10.100
server obelix
```

3. Synchronize the time between **server** & **kdc**

```bash
# on the server
ntpdate -dv 10.10.10.100
```

![](/img/ntp.png)

##### 3 Configuration of **KDC**

1. Install packages

```bash	
sudo apt install krb5-kdc krb5-admin-server krb5-config -y
```	
During installation you will be prompted to enter the realm, kerberos server and administartive server and it would be in order:

|Prompt	|   value |
|---|---|
|   Realm   |	PROJET.TN |
|   Kerberos servers	|   kdc.projet.tn |
|   Administrative Service |	kdc.projet.tn |

![](/img/kerberos1.png)

> We choosed *.projet.tn as our domain but we can change it as we wish <br>
> Its capital sensitive.<br>
> View kdc settings with cat /etc/krb5.conf <br>
> The error failed to start kerberos 5 .. will not be a problem.

2. Add Kerberos database

```bash
sudo krb5_newrealm
```

3. Admin principal,host principal and generate its keytab 

* Principal : unique identity to which kerberos can assign tickets.
* keytab : stores long-term keys for one or more principals and allow server applications to accept authentifications from clients, but can alse be used to obtain initial credentials for clients .

```bash
kadmin.local                              # login as local admin
addprinc root/admin                       # add admin principal
addprinc -randkey host/kdc.projet.tn     # add host principal
ktadd host/kdc.projet.tn                 # generate host principal keytab
```

> Type ``q`` to exit

4. Grant admin principal all privileges

Edit the file ``/etc/krb5kdc/kadm5.acl``

```bash
root/admin * #uncomment this line
```

Then restart the kerberos service

```bash
sudo systemctl restart krb5-admin-server
```
> To check status we run ``sudo systemctl status krb5-admin-server``

![](/img/krbkdc.png)

##### 4 Configuration of **Server**

1. Install packages

```bash
sudo apt install krb5-user libpam-krb5 libpam-ccreds -y
```

During installation you will be prompted to enter the realm, kerberos server and administartive server and it would be in order:

|Prompt	|   value |
|---|---|
|   Realm   |	PROJET.TN |
|   Kerberos servers	|   kdc.projet.tn |
|   Administrative Service |	kdc.projet.tn |

2. Configure host principal and generate its keytab

```bash
sudo kadmin # login as admin (type password)
addprinc -randkey host/server.projet.tn # add host principal
ktadd host/server.projet.tn # generate host principal keytab
```
> Type ``q`` to exit

3. Add *test* user and create corresponding principal

```bash
sudo useradd -m -s /bin/bash tommy
sudo kadmin
addprinc tommy # add user principal
```

> Type ``q`` to exit

> We can create as many users as we want and just each time connecting to the kadmin and add them


##### 5 Flask Configuration

1. Install packages

```bash
pip install Flask
sudo apt install libkrb5-dev
pip install Flask-kerberos
pip install flask_bootstrap
pip install sqlalchemy
```

> Or we can `pip install -r requirements.txt` 

2. Install the project

```bash
git clone https://github.com/OussemaJaouadi/projet_security
sudo su
export KRB5_KTNAME=/etc/krb5.keytab
```	

To visualize your keytab,run the **ktutil** as root

```bash
ktutil
? #list all commands
read_kt /etc/krb5.keytab #read keytab
list #show principals
```

## Using the app 

<hr>

1. Before starting the main app, we need to change domain in each script to the one you chose

| Script  | line  |
|---|---|
| ./api/app.py  | 112  |
| ./consumer/app.py  | 6 |

2. Then we run the API app as **root** : 
    ```bash
    python3 api/app.py
    ```
3. Open another terminal tab and connect as user **tommy** (in our case) , get ticket and then open your front app :
    ```bash
    su tommy
    kinit
    python3 consumer/auth.py
    ```


## Resources :

- [https://ubuntu.com/server/docs/service-kerberos](/img/https://ubuntu.com/server/docs/service-kerberos)
- [https://web.mit.edu/kerberos/krb5-1.12/doc/admin/admin_commands/kadmin_local.html](/img/https://web.mit.edu/kerberos/krb51.12/doc/admin/admin_commands/kadmin_local.html)
- https://github.com/hamza-mahjoub/flask-kerberos-module
- https://flask-kerberos.readthedocs.io/en/latest/
