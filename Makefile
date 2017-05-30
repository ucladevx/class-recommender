NAME=${PWD##*/} 

all: stop build run

stop:
	- docker-compose stop

build:
	docker-compose build --no-cache

run:
	docker-compose up
