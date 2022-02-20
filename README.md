# Visual scheme https://miro.com/app/board/uXjVOMrB_1o=/?invite_link_id=561995038645

## For local testing you must execute following steps
- Create .env file  like .env.example in the root of your project. (Use your own bot-token)
- use command `docker compose up`
## After this you must run servers simulating server with ML and server to send response
In the prototype, all services in the same docker container
- `docker exec -it prototype-web-1 /bin/sh -c 'python -m balabola.main'`
- `docker exec -it prototype-web-1 /bin/sh -c 'python -m responder.main'`
## After this steps you may send messages to your telegram bot
commands:
- /start - to start using bot
- /cel to see list of available celebrities
- /help - to see format, how send messages

Balabola (https://yandex.ru/lab/yalm) handles one message about 3-10 seconds, you can turn it off if you want 
and send to user default answer






