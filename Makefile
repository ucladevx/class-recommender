NAME=${PWD##*/} 

all: stop build

stop:
	- docker-compose stop

build:
	docker-compose up -d

