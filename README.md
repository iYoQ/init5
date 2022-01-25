# init5


## Start

#### 1) Create .env.dev file
    env file to be in VAR=VAL format

#### 2) Build image

    docker-compose build

#### 2) Run container

    docker-compose up
    
#### 3) Move on

    http://127.0.0.1:8000/api/v1/swagger/

#### 4) Create superuser

    docker exec -it init5_web_1 python manage.py createsuperuser
                                                        
#### 7) Clear db

    docker-compose down -v
