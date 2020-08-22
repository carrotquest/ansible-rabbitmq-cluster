from diagrams import Cluster, Diagram
from diagrams.onprem.iac import Ansible
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.queue import RabbitMQ
from diagrams.programming.framework import Django
from diagrams.programming.language import Python

with Diagram("MQ Cluster", show=False):
    provisioner = Ansible("mgmt-core")

    metrics = Prometheus("rabbitmq_exporter")
    metrics << Grafana("monitoring")

    producer = Django("Django App")
    consumer = Python("Celery worker")

    with Cluster("RabbitMQ 3-Node Cluster"):
        mq_cluster = [RabbitMQ("leader"),
                        RabbitMQ("follower_1"),
                        RabbitMQ("follower_2")]

    provisioner >> mq_cluster
    producer >> mq_cluster >> consumer
    mq_cluster >> metrics


with Diagram("MQ Single", show=False):
    provisioner = Ansible("mgmt-core")

    metrics = Prometheus("rabbitmq_exporter")
    metrics << Grafana("monitoring")

    producer = Django("Django App")
    consumer = Python("Celery worker")

    with Cluster("RabbitMQ Single Node Cluster"):
        mq_cluster = RabbitMQ("leader")

    provisioner >> mq_cluster
    producer >> mq_cluster >> consumer
    mq_cluster >> metrics
