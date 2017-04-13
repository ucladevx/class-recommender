# react_flask_dockerized
A dockerized version of flask and react

**If you have any questions message me on slack (@jcaip) and I'll update the README.**

# Layout
Basically the src folder contains the backend and the static folder contains the frontend. 
Flask + Gevent is used for the backend and a combination of Nginx + React is used for the frontend. 

# Running the application
To run, make sure you have [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed, and then clone the repo.
Then, simply run 

```make```

Which should spin up both of the containers. 

If you want to learn more about the structure of the project, take a look [here](https://jcaip.github.io/Dockerizing-Web-Applications/)

Essentially, docker lets us create containers - sort of like VM's but not entirely. This lets us manage dependencies easily and also deploy easily. 

Thanks to [Kevin Wang](https://github.com/xorkevin/) for the react code
