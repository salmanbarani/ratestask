# Rate Task

This project was created using domain driven archetecture and is pip installable and can be used in any python project.

## setup Steps

1. To clone the project you can type `git clone https://github.com/salmanbarani/ratestask.git` <br>
2. Then type `cd ratestask/`<br>
3. Then type `make build` to build the project then `make up` to run the project.
4. The project is running now, but before testing you need to rename one column name( I didn't like the name), let's do it by hand.

- first type `docker ps` you must see a prompt like below.<br>

```
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS                          PORTS                                       NAMES
f766cbd5cf67   ratestask-app        "/bin/sh -c 'flask r…"   5 minutes ago   Up 3 minutes                    0.0.0.0:5005->80/tcp, :::5005->80/tcp       ratestask-app-1
dfdd4c8e4dc5   ratestask-postgres   "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes                    0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgres
```

- we need conainer id of `ratestask-postgres` which is `dfdd4c8e4dc5`, yours might be different. we need it to connect to postgresql.<br>

* copy `CONTAINER ID` of `ratestask-postgres` in your clipboard and paset it in the `<container-id>` section of below command
* `docker exec -e PGPASSWORD=ratestask -it <container-id> psql -U postgres` then hit enter to run.
* then type `ALTER TABLE prices RENAME COLUMN day TO date;`
* then exit by typing `exit`.

5.  NOTE: it's a good idea to change above steps (changing column name) or such things in one scripts file, and run it from `docker-compose`, I just add it here to make it clear what we changed from db.

6.  You can run tests by typing `make test` <br>
7.  Now you can request `localhost:5005/rates`. try below example.

```
curl "http://127.0.0.1:5005/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
```

8. to see all commands you can type `make help`
   <br><br>

## Description

I could create a simple flask app and connect it with DB, in that case the whole project would be less than 4 hours, but since as you mentioned in the email `Please treat this challenge as a chance to show off your best knowledge and original work.
` I decided to take extra effort to make it better.<br>
here's a short descriptions of this project.

1. This project was created using domain driven approach. `models` and `tests` are easy to read by any business person, so they can understand what's going on in the code.

2. the whole project consists of seperate layers that are decoupled and can be used apart from each other and each layer can only talk( has dependency ) with below layers, the only dependency is on Abstraaction. for exmaple:

- The flask main responsibility is processing requests, so it only talk with `service` layer and process the request. so `service` can be used by any other web frameworks.
- `service` can only talk with `models` and and `data` layers.

3.  `models` has no dependency with `database`, actually `database` has dependency with `models`. this has a huge beneift if we decided to change DB.

4.  the whole project is pip installable, so you can install it in any project.

5.  It's so easy to scale the project, for know I just implemented the requirements, but later it can be easily scalled.

6.  you can learn much more from reading the code but here's the flow.<br>

![Alt text](https://github.com/salmanbarani/ratestask/blob/trunk/Screenshot%20from%202023-04-01%2011-10-42.png?raw=true)
