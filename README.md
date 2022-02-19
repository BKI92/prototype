# Visual scheme https://miro.com/app/board/uXjVOMrB_1o=/?invite_link_id=561995038645

## For local testing you must execute following steps
- Create .env like .env.example in the root of your project
- use command `docker compose up`
## Afrter this you must run servers simulating server with ML and server to response
In the prototype, they are all in the same docker container (so they will be on different servers)
- `docker exec -it prototype_web_1 /bin/sh -c 'python -m instead_of_ml.main'`
- `docker exec -it prototype_web_1 /bin/sh -c 'python -m responder.main'`
## After this steps you may send messages to your telegram bot




