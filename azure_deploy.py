# azure_deploy.py
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
import os

class AzureDeployer:
    def __init__(self, subscription_id):
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        self.resource_client = ResourceManagementClient(self.credential, subscription_id)
        self.container_client = ContainerInstanceManagementClient(self.credential, subscription_id)
    
    def create_resource_group(self, group_name="king-deepseek-rg", location="eastus"):
        try:
            rg_result = self.resource_client.resource_groups.create_or_update(
                group_name,
                {"location": location}
            )
            print(f"✅ Resource Group Created: {rg_result.name}")
            return rg_result.name
        except Exception as e:
            print(f"❌ Error creating resource group: {e}")
            return None
    
    def deploy_container(self, resource_group, container_group_name):
        try:
            container_group = self.container_client.container_groups.begin_create_or_update(
                resource_group,
                container_group_name,
                {
                    "location": "eastus",
                    "containers": [{
                        "name": "king-deepseek-app",
                        "image": "your-registry.azurecr.io/king-deepseek:latest",
                        "resources": {
                            "requests": {
                                "cpu": 1,
                                "memoryInGb": 2
                            }
                        },
                        "ports": [{"port": 5000}]
                    }],
                    "os_type": "Linux",
                    "ip_address": {
                        "type": "Public",
                        "ports": [{
                            "protocol": "TCP",
                            "port": 5000
                        }]
                    }
                }
            ).result()
            
            print(f"✅ Container Group Deployed: {container_group.name}")
            return container_group.ip_address.ip
        except Exception as e:
            print(f"❌ Error deploying container: {e}")
            return None

def deploy_to_azure():
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    deployer = AzureDeployer(subscription_id)
    
    print("Starting Azure Deployment...")
    
    # Create resource group
    rg_name = deployer.create_resource_group()
    
    if rg_name:
        # Deploy container
        ip_address = deployer.deploy_container(rg_name, "king-deepseek-cg")
        
        if ip_address:
            print(f"🎉 Azure Deployment Complete! Access your app at: http://{ip_address}:5000")
            return ip_address
    
    return None