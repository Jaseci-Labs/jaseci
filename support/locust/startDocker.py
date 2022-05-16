import docker

client = docker.from_env()

def runLost(hostName : str):
    global client
    con = client.containers.run(
            image = "locust-jac-test",
            environment = {
                "LOCUST_HOST": hostName
                },
            )
    return con


runLost("http://localhost:8888")
