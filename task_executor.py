import logging
import argparse
import uuid

from kubernetes import client
from kubernetes import config

logging.basicConfig(level=logging.INFO)
config.load_kube_config()


class Kubernetes:
    def __init__(self):

        # Init Kubernetes
        self.core_api = client.CoreV1Api()
        self.batch_api = client.BatchV1Api()

    def create_namespace(self, namespace):

        namespaces = self.core_api.list_namespace()
        all_namespaces = []
        for ns in namespaces.items:
            all_namespaces.append(ns.metadata.name)

        if namespace in all_namespaces:
            logging.info(f"Namespace {namespace} already exists. Reusing.")
        else:
            namespace_metadata = client.V1ObjectMeta(name=namespace)
            self.core_api.create_namespace(
                client.V1Namespace(metadata=namespace_metadata)
            )
            logging.info(f"Created namespace {namespace}.")

        return namespace

    @staticmethod
    def create_container(image, name, pull_policy, args):

        container = client.V1Container(
            image=image,
            name=name,
            image_pull_policy=pull_policy,
            args=[args],
            command=["python3", "-u", "./shuffler.py"],
        )

        logging.info(
            f"Created container with name: {container.name}, "
            f"image: {container.image} and args: {container.args}"
        )

        return container

    @staticmethod
    def create_pod_template(pod_name, container):
        pod_template = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(restart_policy="Never", containers=[container]),
            metadata=client.V1ObjectMeta(name=pod_name, labels={"pod_name": pod_name}),
        )

        return pod_template

    @staticmethod
    def create_job(job_name, pod_template):
        metadata = client.V1ObjectMeta(name=job_name, labels={"job_name": job_name})

        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=metadata,
            spec=client.V1JobSpec(backoff_limit=0, template=pod_template),
        )

        return job


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Task Executor")
    parser.add_argument("input_string", help="Input String", type=str)
    args = parser.parse_args()

    job_id = uuid.uuid4()
    pod_id = job_id

    """ Steps 1 to 3 is the equivalent of the ./manifestfiles/shuffler_job.yaml """

    # Kubernetes instance
    k8s = Kubernetes()

    # STEP1: CREATE A CONTAINER
    _image = "shuffler:latest"
    _name = "shuffler"
    _pull_policy = "Never"

    shuffler_container = k8s.create_container(_image, _name, _pull_policy, args.input_string)

    # STEP2: CREATE A POD TEMPLATE SPEC
    _pod_name = f"my-job-pod-{pod_id}"
    _pod_spec = k8s.create_pod_template(_pod_name, shuffler_container)

    # STEP3: CREATE A JOB
    _job_name = f"my-job-{job_id}"
    _job = k8s.create_job(_job_name, _pod_spec)

    # STEP4: CREATE NAMESPACE
    _namespace = "jobdemonamespace"
    k8s.create_namespace(_namespace)

    # STEP5: EXECUTE THE JOB
    batch_api = client.BatchV1Api()
    batch_api.create_namespaced_job(_namespace, _job)



