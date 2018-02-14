import json
import tempfile
import os
import subprocess
import time

def describe (instance_id):
    sh('aws ec2 describe-instances --instance-id ' + instance_id)


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
        result = subprocess.check_output(['aws', 'ec2', 'request-spot-instances', '--instance-count', '1', '--spot-price', '0.5', '--launch-specification', 'file://' + os.path.join(tempfile.gettempdir(), f.name), '--type', 'one-time'])
        # should look something like {'SpotInstanceRequests': [{'LaunchSpecification': {'InstanceType': 'g2.2xlarge', 'SecurityGroups': [{'GroupName': 'ssh-only', 'GroupId': 'sg-32aadc76'}], 'Placement': {'AvailabilityZone': 'us-west-1b'}, 'KeyName': 'my_aws_key', 'Monitoring': {'Enabled': False}, 'ImageId': 'ami-52261e32'}, 'SpotInstanceRequestId': 'sir-4jtgf1jg', 'State': 'open', 'ProductDescription': 'Linux/UNIX', 'SpotPrice': '0.500000', 'CreateTime': '2018-02-14T03:24:17.000Z', 'InstanceInterruptionBehavior': 'terminate', 'Type': 'one-time', 'Status': {'Code': 'pending-evaluation', 'UpdateTime': '2018-02-14T03:24:17.000Z', 'Message': 'Your Spot request has been submitted for review, and is pending evaluation.'}}]}

        return json.loads(result.decode('utf-8'))

print(launch())
