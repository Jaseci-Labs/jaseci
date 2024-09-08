import atexit
import os
import docker
import json

client = docker.from_env()
containerList = []


def getConfig(testConfigName: str):
    confData = json.load(open(testConfigName, "r"))
    return confData


def runLocust(
    hostName: str,
    containerName: str,
    testName: str,
    testSRC: str,
    userNum: int,
    spawnRate: int,
    duration: str,
):
    global client
    volume = {
        os.path.abspath("sample_code"): {"bind": "/locust/sample_code", "mode": "rw"}
    }
    con = client.containers.create(
        image="locust-jac-test",
        name=containerName,
        environment={
            "LOCUST_HOST": hostName,
            "LOCUST_TEST_SRC": testSRC,
            "LOCUST_USER_NUMBER": str(userNum),
            "LOCUST_SPAWN_RATE": str(spawnRate),
            "LOCUST_DURATION": duration,
            "LOCUST_TEST_NAME": testName,
        },
        volumes=volume,
    )
    return con


def defaultizeConf(conf):
    return {
        "hostName": conf.get("hostName", "172.17.0.1:8888"),
        "testName": conf.get("testName"),
        "testSRC": conf.get("testSRC"),
        "userNum": conf.get("userNum"),
        "spawnRate": conf.get("spawnRate"),
        "duration": conf.get("duration"),
        "containerName": f"Locust_{conf.get('testName')}",
    }


def runConfLocust(conf):
    return runLocust(
        hostName=conf["hostName"],
        containerName=conf["containerName"],
        testSRC=conf["testSRC"],
        userNum=conf["userNum"],
        spawnRate=conf["spawnRate"],
        duration=conf["duration"],
        testName=conf["testName"],
    )


def waitAll():
    global containerList
    for _, container in containerList:
        container.wait()


def killAll():
    global containerList
    print("Killing and removing all the containers.")
    for _, container in containerList:
        try:
            container.kill()
        except Exception:
            pass
    for _, container in containerList:
        container.remove()


def retrieveLogs(path: str, container):
    f = open(os.path.join(path, "logs.txt"), "w")
    f.write(str(container.logs()))
    f.close()


def retrieveCSV(path: str, container):
    bits, _ = container.get_archive("/locust/csv/")
    f = open(os.path.join(path, "data.tar"), "wb")
    for chunk in bits:
        f.write(chunk)
    f.close


def retrieveData():
    global containerList
    for name, container in containerList:
        path = os.path.join("results", name)
        os.makedirs(path, exist_ok=True)
        retrieveCSV(path, container)
        retrieveLogs(path, container)


atexit.register(killAll)
configName = input("Name of your test configuration:")
confList = getConfig(configName)

for conf in confList:
    defConf = defaultizeConf(conf)
    container = runConfLocust(defConf)
    container.start()
    containerList.append((defConf["testName"], container))

waitAll()
retrieveData()
