import json
import tempfile
import os
import subprocess
import time

def find_instance_id(spot_instance_request_id):
    instance = None
    while not instance:
        result = subprocess.check_output(['aws', 'ec2', 'describe-spot-instance-requests', '--spot-instance-request-ids', spot_instance_request_id])
        result = result.decode('utf-8')
        result = json.loads(result)
        print("RESULT", result)
        print("RESULT", result['SpotInstanceRequests'][0]['Status']['Code'])
        if result['SpotInstanceRequests'][0]['Status']['Code'] == 'fulfilled':
            return result['SpotInstanceRequests'][0]['InstanceId']
        time.sleep(0.5)

def describe_instance(instance_id):
    result = subprocess.check_output(['aws', 'ec2', 'describe-instances', '--instance-ids', instance_id])
    result = result.decode('utf-8')
    result = json.loads(result)
    return result

def restart_instance(instance_id):
    subprocess.check_output([])

def launch (ami="ami-52261e32", instance_type="g2.2xlarge"):
    instance_spec = {
        'ImageId': ami,
        'KeyName': 'my_aws_key',
        'SecurityGroupIds': ['sg-32aadc76'],
        'InstanceType': instance_type,
        'Placement': {
            'AvailabilityZone': 'us-west-1b'
        }
    }
    with tempfile.NamedTemporaryFile() as f:
        f.write(json.dumps(instance_spec).encode('utf-8'))
        f.flush()
        result = subprocess.check_output(['aws', 'ec2', 'request-spot-instances', '--instance-count', '1', '--spot-price', '0.35', '--launch-specification', 'file://' + os.path.join(tempfile.gettempdir(), f.name), '--type', 'one-time'])
        result = result.decode('utf-8')
        result = json.loads(result)
        request_id = result['SpotInstanceRequests'][0]['SpotInstanceRequestId']
        # terminate spot instance unless it's kept alive...
        instance_id = find_instance_id(request_id)
        print('found instance id', instance_id)

launch()
