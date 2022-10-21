# Preparation

Before you can run this package, you should run the following command to install the dependency:
```bash
pip install prometheus-api-client
```

# Usage

This package helps to wrap up the k8s monitoring in Python. To initialize the system, you first need to the URL to the Prometheus server.
```Python
p = Promon("http://clarity31.eecs.umich.edu:8082")
```

Then there are multiple functions that you can use in this class. An example is
```Python
p.disk_free_bytes()
```

This function returns the size of free space in each node (bytes).
