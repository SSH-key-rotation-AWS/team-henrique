from AWS_Cloudwatch import AWS_Cloudwatch
import time 

region = "us-east-1"
name_space = "AWS CLOUD TEST"

cloudwatch = AWS_Cloudwatch(region,name_space)




def test_time_generation_metric():
    for i in range(5):
        with cloudwatch.key_generation_time_metric(instance_id="first_instance",metric_name="time to generate key"):
            print("currently in context manager")
            time.sleep(100)
            print("Leaving....")



def test_count_metric():
    for i in range(5):
        time.sleep(100)
        cloudwatch.key_count_metric(metric_name="Key Counts",instance_id="Second_instance")

test_time_generation_metric()
test_count_metric()








    