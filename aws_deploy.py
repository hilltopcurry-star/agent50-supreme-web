# aws_deploy.py
import boto3
import os
import time
from botocore.exceptions import ClientError

class AWSDeployer:
    def __init__(self):
        self.ec2 = boto3.resource('ec2')
        self.ecs = boto3.client('ecs')
        self.elbv2 = boto3.client('elbv2')
        
    def create_infrastructure(self):
        print("🚀 Creating AWS Infrastructure...")
        
        # Create VPC
        vpc = self.ec2.create_vpc(CidrBlock='10.0.0.0/16')
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "king-deepseek-vpc"}])
        vpc.wait_until_available()
        
        print(f"✅ VPC Created: {vpc.id}")
        
        # Create Internet Gateway
        ig = self.ec2.create_internet_gateway()
        vpc.attach_internet_gateway(InternetGatewayId=ig.id)
        
        # Create Route Table
        route_table = vpc.create_route_table()
        route_table.create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig.id
        )
        
        return vpc.id, ig.id

    def create_ecs_cluster(self, cluster_name="king-deepseek-cluster"):
        try:
            response = self.ecs.create_cluster(clusterName=cluster_name)
            print(f"✅ ECS Cluster Created: {cluster_name}")
            return response['cluster']['clusterArn']
        except ClientError as e:
            print(f"❌ Error creating cluster: {e}")
            return None

# Deployment script
def deploy_to_aws():
    deployer = AWSDeployer()
    
    print("Starting AWS Deployment...")
    
    # Create infrastructure
    vpc_id, ig_id = deployer.create_infrastructure()
    
    # Create ECS cluster
    cluster_arn = deployer.create_ecs_cluster()
    
    print("🎉 AWS Deployment Setup Complete!")
    return {
        'vpc_id': vpc_id,
        'ig_id': ig_id,
        'cluster_arn': cluster_arn
    }