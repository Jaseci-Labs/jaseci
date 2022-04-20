## Locust Load Test for JASECI API

### Install Python 3.8 
Install Python from offical Python Website

```console
https://www.python.org/downloads/release/python-380/
```

### Install Locust 

Locust is an easy-to-use, distributed, user load testing tool. It is intended for load-testing web sites (or other systems) and figuring out how many concurrent users a system can handle.

The idea is that during a test, a swarm of locust users will attack your website. The behavior of each user is defined by you using Python code, and the swarming process is monitored from a web UI in real-time. This will help you battle test and identify bottlenecks in your code before letting real users in.

Locust is completely event-based, and therefore it’s possible to support thousands of concurrent users on a single machine. In contrast to many other event-based apps it doesn’t use callbacks. Instead it uses light-weight processes, through gevent. Each locust swarming your site is actually running inside its own process (or greenlet, to be correct). This allows you to write very expressive scenarios in Python without complicating your code with callbacks.

```console
pip install locust
```

#### Install Pandas

```console
pip install pandas
```



#### Install Locust Plugins

```console
pip install locust_plugins
```

### Create Users for Load test

To add users for load test , Edit the addUsers.csv files with new users in the format specified .

After that run below command

```console
locust -f createUsers.py
```

Go to the link specified in console, e.x http://0.0.0.0:8089 and put the number of user same as what you added in csv file and run the application



### Run Locust Load test through browser

```console
locust -f app.py
```

Once you’ve started Locust using one of the above command lines, you should open up a browser and point it to http://127.0.0.1:8089. Then you should be greeted with something like this

### Run Locust Load test via headless 

You can run locust without the web UI - for example if you want to run it in some automated flow, like a CI server - by using the --headless flag together with -u and -r:

```console
locust -f app.py -u 2 -r 1 -t 5s --headless --print-stats --host=<Your Jaseci API URL>
```

where

-u specifies the number of Users to spawn, and 
-r specifies the hatch rate (number of users to spawn per second).


### Run Locust via Docker

Coming Soon

