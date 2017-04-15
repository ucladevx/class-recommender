NAME=${PWD##*/} 

all: stop build run

stop:
	- docker-compose stop

build:
	- source /src/secrets.sh
	docker-compose build

run:
	docker-compose up
