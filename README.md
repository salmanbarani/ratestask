# Rate Task

This project was created using domain domain driven archetecture and is pip installable and can be used in any python project.

## setup Steps

1. clone the project you can type `git clone https://github.com/salmanbarani/ratestask.git` <br>
2. then type `cd ratestask/`<br>
3. then type `make build` type build the project then `make up` to run the project.
4. your project now is running but before testing you need rename one column name( I didn't like the name), let's do it by hand.

- first type `docker ps` you must a prompt like this.<br>

```
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS                          PORTS                                       NAMES
f766cbd5cf67   ratestask-app        "/bin/sh -c 'flask r…"   5 minutes ago   Up 3 minutes                    0.0.0.0:5005->80/tcp, :::5005->80/tcp       ratestask-app-1
dfdd4c8e4dc5   ratestask-postgres   "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes                    0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgres
```

- we need conainer id of `ratestask-postgres` which is `dfdd4c8e4dc5`, yours might be different. we need it to connect to postgresql.<br>

* copy `CONTAINER ID` of `ratestask-postgres` in your clipboard and paset it in the `<container-id>` section of below command
* `docker exec -e PGPASSWORD=ratestask -it <container-id> psql -U postgres` then hit run
* then type `ALTER TABLE prices RENAME COLUMN day TO date;`
* then exit by typing `exit`.
* NOTE: it's a good idea to change above steps (changing column name) or such things in one scripts file, and run it in docker, I just add it here to make it clear what we changed from db.

* now you can run tests by typing `make test` <br>
* you request the endpoint in below command

```
curl "http://127.0.0.1:5005/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
```
