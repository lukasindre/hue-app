# hue-app

This simple app controls some of my lights at my house.  It is a docker compose stack, including a fastapi app, celery worker, and redis as a message broker.  

![coverage](coverage.svg)
You better appreciate this coverage badge, I skipped an arm workout for this.

## End Result
![lights](./assets/lights.MOV)

## Development

To run this app, you need docker installed.  You also should run 
```sh
cp .env.skel .env
```
and fill in the values appropriately.

Running `make run` will build and run the docker compose stack, which should set you on the path to righteousness and lighteousness.

~~I have not yet ran this off of the box that i wrote it on, but once i do, i'll update this readme with full instructions.~~ I ran this on a different box, just get yourself some docker and you're good to go with `make run`.

Having said that, this app is also super specific to the type of lights I have, as they're configured in [the app's config file](./app/config/local.yaml).  The amount of time it would take me to build out self-discovery, and a bunch of other fancy things, does not provide enough value to have my wife yell at me for playing these computer games /s.

Merry Christmas!