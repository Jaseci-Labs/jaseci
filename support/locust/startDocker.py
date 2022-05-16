import docker
import json

client = docker.from_env()

def getConfig():
    confData = json.load(open("test.json", 'r'))
    return confData

def runLocust(hostName : str, containerName : str, testSRC: str, userNum: int, spawnRate: int, duration: str):
    global client
    con = client.containers.create(
            image = "locust-jac-test",
            name = containerName,
            environment = {
                "LOCUST_HOST": hostName,
                "LOCUST_TEST_SRC": testSRC,
                "LOCUST_USER_NUMBER": str(userNum),
                "LOCUST_SPAWN_RATE": str(spawnRate),
                "LOCUST_DURATION": duration
                },
            )
    return con

def defaultizeConf(conf):
    return {
            'hostName' : conf.get('hostName', '172.17.0.1:8888'),
            'containerName': conf.get('containerName', None),
            'testSRC': conf.get('testSRC'),
            'userNum': conf.get('userNum'),
            'spawnRate': conf.get('spawnRate'),
            'duration': conf.get('duration')
            }

def runConfLocust(conf):
    return runLocust(
            hostName=conf['hostName'],
            containerName=conf['containerName'],
            testSRC=conf['testSRC'],
            userNum=conf['userNum'],
            spawnRate=conf['spawnRate'],
            duration=conf['duration']
            )

def waitAll(containerList):
    for container in containerList:
        container.wait()

containers = []
confList = getConfig()
for conf in confList:
    defConf = defaultizeConf(conf)
    container = runConfLocust(defConf)
    container.start()
    containers.append(container)

waitAll(containers)
