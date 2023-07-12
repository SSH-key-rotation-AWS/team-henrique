"""AWS metric publisher"""
import datetime
from Functions.Metric import Metric
from Functions.MetricPublisher import MetricPublisher
import boto3
import time

class AWSMetricPublisher(MetricPublisher):
    """Publishes Metric-specific data"""

    def __init__(self, name_space: str, instance_id: str, aws_region: str):
        """Instantiate the AWSMetricPublisher object.

        Args:
            name_space (str): The namespace of the metric.
            instance_id (str): The ID of the instance associated with the metric.
            aws_region (str): The AWS region to use for CloudWatch.
        """
        self._name_space = name_space
        self.cloud_watch = boto3.client("cloudwatch", region_name=aws_region)
        self._instance_id = instance_id

    def publish_metric(self, metric: Metric):
        """Publishes a metric to CloudWatch.

        Args:
            metric (Metric): The metric object to be published.
        """
        metric_name = metric.get_name()
        metric_value = metric.get_value()
        metric_unit = metric.get_unit()

        self.cloud_watch.put_metric_data(
            Namespace=self._name_space,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Dimensions": [
                        {"Name": "AWS_MetricPublisher", "Value": self._instance_id},
                    ],
                    "Unit": metric_unit,
                    "Value": metric_value,
                },
            ],
        )
    def retrieve_metric_data(self,metric:Metric,start_time:datetime.datetime,period:int):
        response = self.cloud_watch.get_metric_statistics(
    Namespace=self._name_space,
    MetricName=metric.get_name,
    StartTime=start_time,
    EndTime=datetime.datetime.now(),
    Period=period,
    )
        return response
    