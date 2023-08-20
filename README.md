# A.M.S 
### Assets Management System


About AMS
---------
This software is going to be used for assets management according to ISMS ISO27001.


Want to use this project?
-------------------------

### Development

Uses the default Django development server.

1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
2. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "web" folder is mounted into the container and your code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Update the environment variables in the *docker-compose.yml*, *.env.db.prod* and *.env.prod* files.
2. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.


TODO
----
1. Separate Celery Beat Worker from Django application.
2. Fix problem with tracerout and libpcap.
3. Test inventory api through coreapi
4. Develop agent project for windows 

