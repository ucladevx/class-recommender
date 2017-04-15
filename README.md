# react_flask_dockerized
A dockerized version of flask and react
a
**If you have any questions message me on slack (@jcaip) and I'll update the README.**

# Layout
Basically the src folder contains the backend and the static folder contains the frontend. 

Flask + Gevent is used for the backend and a combination of Nginx + React is used for the frontend. 

# Running the application
To run, make sure you have [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) installed, and then clone the repo.
Then, simply run 

```
make
```

Which should spin up both of the containers. 

After you see "attaching to ....." that means that you are ready to go.


If you navigate to localhost in your web browser, you should see a sample page with a black background. 

If you click on the button, "Hello World!" should be printed out to the console. 

In addition if you look at your terminal output, you should see a recorded GET request for src

# Front-end setup
Navigate to static and run `npm install`. This will install the npm dependencies needed. Next, navigate to the `src` directory and run `npm run build-dev`. This will start the development server so you can make changes to the front-end and see the results in real time. Note that you will have to restart the docker image for backend changes. 

# About the application

Essentially, docker lets us create containers - sort of like VM's but not entirely. This lets us manage dependencies easily and also deploy easily. 

Thanks to [Kevin Wang](https://github.com/xorkevin/) for the react code
