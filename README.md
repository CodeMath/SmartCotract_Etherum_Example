## Ethereum Smart Contract Example on Django
This project is based on Django for Ethreum Smart contract example.

Before start project, need to ethereum test net or private net.


1. Version 1.0.0
    - Use a JSON-RPC Server.
    - Simple testing for transaction and generate new account.
    - Github login and auto-generate address. (Password is so simple. because it is a just test!)
    - After testing, user make a password for address.(Not now)


more information [geth](https://geth.ethereum.org) or [Metamask](https://metamask.io)


## Build status
[![Build Status](https://travis-ci.org/CodeMath/SmartCotract_Etherum_Example.svg?branch=ver-1.0.0)](https://travis-ci.org/CodeMath/SmartCotract_Etherum_Example)
[![django_version](https://img.shields.io/badge/django%20versions-2.0%2B-blue.svg)](https://github.com/CodeMath/SmartCotract_Etherum_Example)
![license](https://img.shields.io/github/license/mashape/apistatus.svg)



## Tech/framework used
<b>Django Project</b>
- Required python3.x+ and Django 2.x+


## Installation
<b>Required Ethereum test net or private net.</b>


```
$ git clone git@github.com:CodeMath/SmartCotract_Etherum_Example.git
$ cd eth_testnet
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

<b>Make a eth_testnet/configure.py</b>
configure.py is a github token and address, password.



#### Anything else that seems useful

## Contribute & License

Anyone can become a contributor!

MIT License © [codemath](https://github.com/CodeMath)