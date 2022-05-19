# Locust Load Test for JASECI
Locust is an easy-to-use, distributed, user load testing tool. It is intended for load-testing web sites (or other systems) and figuring out how many concurrent users a system can handle.

## Run Locust natively

### Install Locust
```console
pip install locust
```
### Configure the test
Create test users. This following script will prompt you for the jaseci server URL and number of test users you wish to create.
```bash
python create_users.py
```
Then create a folder in `sample_code/`. Set up a file `config.json` in the folder. Here is an example:
```json
{
    "walkers" : ["init"], 
    "src" : "walker.jac",
    "remote_actions" : ["http://flair-ner:80/"],
    "local_actions" : []
}
```

`walkers` is a list of walkers that you want to call (in sequence). `src` the name of the file that contains your code. `remote_actions` should contain a list of URLs of your remote services. `local_actions` should contain a list of names of your modules.

### Run the test
The program reads the environment variable `LOCUST_TEST_SRC` for the location of the test configuration and `LOCUST_HOST` for the jaseci server URL.
```bash
LOCUST_HOST='JASECI_URL' LOCUST_TEST_SRC='sample_code/<YOUR TEST>' locust -f run_jac.py
```

Go to the link specified in console, e.x http://0.0.0.0:8089 and specify the desired number of users for the load test and initiate the test. You can also change the server URL in the web UI.

## Run Locust with docker

### Set up the environment
Install docker
```bash
pip install docker
```
Build the custom docker image
```bash
docker build -t locust-jac-test .
```
**Note** If you are testing a localhost jaseci, please make sure that your Jaseci service is exposed to `0.0.0.0` since we are going to access the service from docker, not local. To achieve that, run
```bash
kubectl port-forward <JASECI POD NAME> 8888:80 --address="0.0.0.0"
```
### Configure the tests

**Note** Please make sure that you have configured the tests properly as we did in the previous section.

Since we are not going to open a Web UI this time, we need some more information. Please give all the information in `test.json`. Here is an example
```json
{
    "hostName": "http://172.17.0.1:8888",
    "testName": "simple",
    "testSRC": "sample_code/simple",
    "userNum": 5,
    "spawnRate": 1,
    "duration": "10s"
}
```
`hostName` gives the URL of the host. Note that `localhost` on the host computer is mapped to `172.17.0.1` inside docker containers. `testName` is a simple name for the test. It will be included in the name of the container and the result that we retrieve. `testSRC` specifies the path to the specific test configuration. `userNum` specifies the number of users that we need to spawn in this test. `spawnRate` specfies the speed that we spawn the users (How many users created in one second). `duration` sets the time length of the test.

### Run the test
To run the test
```bash
python start_docker.py
```
All the tests will be created inside a separate docker container. The containers are named `Locust_<TESTNAME>`. All the tests should be run in parallel. When all the tests are done, the python script automatically removes and kills all the containers.

### Retrieve the test data

All available data are retrieved after you ran the script. They should be available under `results/<testName>/`. `logs.txt` is the log of the test. `data.tar` file should contain four CSV files. They are directly from locust. 