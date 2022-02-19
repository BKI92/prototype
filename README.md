# Visual scheme https://miro.com/app/board/uXjVOMrB_1o=/?invite_link_id=561995038645

## For local testing you must start redis service and postgres service
- Create .env like env.example in the root of your project
- use command docker compose up

## Afrter this you must run servers simulating server with ML and server to response
- docker exec -it prototype_web_1 /bin/sh -c 'python -m instead_of_ml.main'
- docker exec -it prototype_web_1 /bin/sh -c 'python -m responder.main'
## After this steps you may send messages to your telegram bot




