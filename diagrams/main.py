from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.iac import Ansible
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.queue import RabbitMQ
from diagrams.programming.framework import Django
from diagrams.programming.language import Python

with Diagram("MQ Cluster", show=False, direction="TB"):
    provisioner = Ansible("mgmt-core")

    metrics = Grafana("monitoring") >> Edge(color="firebrick", style="dashed") >> Prometheus("rabbitmq_exporter")

    producer = Django("Django App")
    consumer = Python("Celery worker")

    with Cluster("RabbitMQ 3-Node Cluster"):
        mq_cluster = [RabbitMQ("leader"),
                        RabbitMQ("follower_1"),
                        RabbitMQ("follower_2")]

    provisioner >> mq_cluster
    producer >> Edge(color="brown") >> mq_cluster << Edge(color="brown") << consumer
    mq_cluster <<  metrics


with Diagram("MQ Single", show=False, direction="TB"):
    provisioner = Ansible("mgmt-core")

    metrics = Grafana("monitoring") >> Edge(color="firebrick", style="dashed") >> Prometheus("rabbitmq_exporter")

    producer = Django("Django App")
    consumer = Python("Celery worker")

    with Cluster("RabbitMQ Single Node Cluster"):
        mq_cluster = [RabbitMQ("leader")]

    provisioner >> mq_cluster
    producer >> Edge(color="brown") >> mq_cluster << Edge(color="brown") << consumer
    mq_cluster <<  metrics
