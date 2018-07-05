# Tutorial showing use of MemCachier with Django+Docker+ECS

This is code to go with a [MemCachier
tutorial](https://blog.memcachier.com/2018/06/27/django-docker-ecs-tutorial/)
showing how to use Docker, ECS and MemCachier with a simple Django
application.

The repository contains the following subdirectories:

- `thumbnailer-basic`: basic Django application;
- `thumbnailer-ecs-no-caching`: Django application for deployment to
  ECS with Docker (no caching);
- `thumbnailer-ecs-caching`: Django application for deployment to ECS
  with Docker (caching using MemCachier);
- `benchmarking`: performance measurement code using Node.js and
  [Webdriver.io](http://webdriver.io).
