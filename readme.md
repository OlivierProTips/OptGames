# CTF Games

## Prerequisites

- Install docker
```bash
sudo apt update
sudo apt install lsb-release gnupg2 apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/debian.gpg
sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
sudo apt install docker.io docker-compose-plugin -y
sudo adduser $USER docker
```

- Install python
```bash
sudo apt install python3 python3.11-venv apt install python3.11-venv
```

(Optional, if you need CTF to be accessible from Internet)
- Enable challenge ports on router
- Enable reverse proxy

## Steps

1. Create data folder
    ```bash
    mkdir data
    ```
2. From admin folder launch scripts
    ```bash
    python3 fill_challenges.py
    python3 admin_password.py
    python3 add_users.py
    ```
3. Launch container
    ```bash
    docker compose up -d --build --force-recreate
    ```

## Challenge structure

In admin/challenges

```
Challenge_name
├── description.txt
├── file
│   ├── file1
│   ├── file2
│   └── ...
└── flag.txt
```

|                 |                                                                                   |        |           |
| --------------- | --------------------------------------------------------------------------------- | ------ | --------- |
| Challenge_name  | The name of the challenge. It will be the title of the card                       | folder | mandatory |
| description.txt | Contains the description of the challenge                                         | file   | mandatory |
| flag.txt        | Contains the flag of the challenge                                                | file   | mandatory |
| file            | Contains the files for the challenge. A download button will be added to the card | folder | optional  |