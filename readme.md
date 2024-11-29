# CTF Games

## Steps

1. Create data folder
    ```bash
    mkdir data
    ```
2. Create a venv and install requirements
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. From admin folder launch scripts
    ```bash
    python3 fill_challenges.py
    python3 admin_password.py
    python3 add_users.py
    ```
4. Update compose
    Utiliser `getent group docker` pour avoir le GID du group docker
5. Launch container
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