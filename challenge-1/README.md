# keychain-mayhem
My first CTF challenge for picoCTF

## Keywords
- Web Exploitation
- SQL Injection
- PGP
- Base64
- Hidden Fields
- OSINT

## Set up steps

1) git clone this repository

2) cd into the repo and run the following command to set-up the docker
```
docker build -t keychain-mayhem .
```

3) To start the server, run the following command
```
docker run -it keychain-mayhem
```

4) You should now have access to the server on
```
http://<Docker ip>:5000
```


## Solution Approach

- Navigate to the login page
- Get in to find information about the developer and their interests
- Send encrypted commands