NAME=${PWD##*/} 

all: stop build run

stop:
	- docker-compose stop

build:
	docker-compose build

run:
	docker-compose up -d
