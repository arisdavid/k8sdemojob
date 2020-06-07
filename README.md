
## Kubernetes Job Demo

### Setup
* Docker-for-Desktop installed and running
* Ensure the Enable Kubernetes checkbox is selected in the docker settings
* Kubernetes / Kubectl installed - https://kubernetes.io/docs/tasks/tools/install-kubectl/
* For Mac users using Minikube is highly recommended 

### Build a docker image
```
docker build -t shuffler:latest -f shuffler/Dockerfile .
```

### Run the program
```
python3 -u task_executor.py <input_string>
```

#### Screenshots

#### Commands
![Commands](https://github.com/arisdavid/k8sdemojob/blob/master/screenshots/commands.png)

#### YAML to Python Equivalent
![YAMLTOPYTHON](https://github.com/arisdavid/k8sdemojob/blob/master/screenshots/yaml_to_python.png)