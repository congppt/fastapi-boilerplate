# FastAPI - SQLAlchemy Boilerplate

## Description
This project is a back-end boilerplate for monolithic application. 
It's built with FastAPI & SQLAlchemy framework in Python.

## Project Structure
A fully implemented project will have this following structure

```
.
├── ...
├── alembic/
├── logs/
├── scripts/
│   ├── local/
│   └── shared/
├── src/
│   ├── auth/
│   ├── background_job/
│   ├── config/
│   ├── constants/
│   ├── db/
│   ├── logger/
│   ├── middlewares
│   ├── services/
│   ├── storage/
│   ├── user/
│   ├── ...
│   ├── utils/
│   ├── dependencies.py
│   └── main.py
├── .env
├── .gitignore
├── alembic.ini
├── config.json
├── config.local.json
├── docker-compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt
```
- `alembic`: 
- `scripts`: 
- `src`: 
- `src/auth`: 
- `env`: 
- `logs`: 
- `middleware`: 
- `schemas`: 
- `routers`: 
- `templates`: 
- `utils`: 
- .env: 
- .gitignore
- main.py:
- README.md: this file
- requirements.txt: lists the Python dependencies that need to be installed for the project.

## Installation
Follow these steps to install and run the project:
1. Clone the project from its repository:
```bash
git clone https://github.com/congppt/fastapi-boilerplate.git
```
2. Navigate into the project directory:
```bash
cd fastapi-boilerplate
```
3. Create virtual environment
```bash
python -m venv .venv
```
4. Active virtual environment
```bash
.venv/Scripts/activate
```
5. Install the required Python packages.
```bash
pip install -r requirements.txt
```
6. Unit test:
```bash
pytest --capture=no
```
7. Run the FastAPI server:
```bash
uvicorn main:app --reload
```
## Deployment with Docker
1. Push image into registry via:
   - Step 1: Login into registry
       ```bash
       docker login [your.registry.ip:port]
       ```
   - Step 2: Add this line to Docker's daemon.json file and restart the Docker Daemon:
   (C:\ProgramData\Docker\config\daemon.json on windows, /etc/docker/daemon.json on linux)
     ```bash
     { 
         "insecure-registries":["[your.registry.ip:port]"]
     }
     ```
   - Step 3: run file to push image for development enviroment:
     ```bash
     ./push_image_development.sh
     ```
     or push image for production environment
     ```bash
     ./push_image_production.sh
     ```
   - Step 4: Check image push successful

2. On server copy file `docker-compose.yml` and folder `logs` (first time setup) ***If you are in 10.39.125.26:8000, change that ip by localhost for step 1***
   - Step 1: Login into registry
    ```bash
    docker login [your.registry.ip:port]
    ```
    - Step 2: On docker-compose file, update environmental variables as needed:
        + SQLALCHEMY_DATABASE_URL: postgreql://{username}:{password}@{hostname}:{port}/{database_name} (Connection string)
3. On server run command to start service:
    ```bash
    ./start.sh
    ```
4. Logs
    ```bash
    ./log.sh
    ```
5. SSH container
    ```bash
    ./ssh.sh
    ```

### Handle the situation when the registry is down.
1. Run `build_local_image.sh` on local -> Select environment to build file {image}.tar
2. Use WinSCP to connect to the account scp of server -> Move the file {image}.tar at local working project directory to the user scp directory on the server.
3. At working directory on Server run `start_from_local_image.sh`

### Rollback Script Instructions
#### 1. Rollback on Server:
1. Run `rollback.sh`
2. Enter the Git commit ID to rollback.
#### 2. Rollback from Local:
1. Run `rollback_from_local.sh`
    - Select Git version or default to the latest.
2. Choose environment to build (default: development).
3. Select to push image to registry (default) or build a .tar file.
4. After rollback:
    - If pushed to registry, run `start.sh` on server.
    - If .tar file, run `start_from_local_image.sh` on server.

## Migrate update DB
1. Update model in /src/db/models
2. Create file migration: 
```bash
alembic revision --autogenerate -m "[migration_name]"
```

If you need to revert latest database migration, use the command:
```bash
alembic downgrade -1
```

## Authors
- Pham Phuc Thanh Cong - Email: congppt2002@gmail.com