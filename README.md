# Visual scheme https://miro.com/app/board/uXjVOMrB_1o=/?invite_link_id=561995038645

## For local testing you must start redis service and postgres service
- docker pull postgres
- docker run -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres --name=pgsql -d -p 5432:5432 postgres
- docker pull redis
- docker run -p 6379:6379 -d redis


## Later you must go in docker container with redis and set up password
In redis container: 
- redis-cli
- AUTH default password


## After this actions need to do the following steps:
- python -m scripts.migrate

## And start up 3 scripts, which are emulated different web-services
- python -m task_manager.main
- python -m instead_of_ml.main
- python -m responder.main

## After this steps you may send messages to your telegram bot




