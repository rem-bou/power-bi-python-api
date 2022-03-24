import logging
import json
import time
import secrets

from power_bi_api_client import PowerBIAPIClient

pbi_client = PowerBIAPIClient(
    secrets.tenant_id,
    secrets.client_id,
    secrets.client_secret,
)

logging.basicConfig(level=logging.INFO)

create_workspace = pbi_client.create_workspace('Testing Environment [Dev]')
time.sleep(5)
set_workspace_capacity = pbi_client.set_workspace_capacity('Testing Environment [Dev]', {"capacityId": "4846741C-9AC0-456B-A0F2-6BA8C4D1D720"})
time.sleep(5)
import_pbix_file = pbi_client.import_file_into_workspace('Testing Environment [Dev]', False, 'SharePointListDemo.pbix', 'SharePointListDemo')
time.sleep(5)
create_pipeline = pbi_client.create_pipeline('Testing Environment')
time.sleep(5)
assign_pipeline_workspace = pbi_client.assign_pipeline_workspace('Testing Environment', 'Testing Environment [Dev]', 0)
time.sleep(5)
deploy_pipeline_test = pbi_client.deploy_all_pipeline_stage('Testing Environment', 'Testing Environment [Test]', '4846741C-9AC0-456B-A0F2-6BA8C4D1D720', "Dev")
time.sleep(5)
deploy_pipeline_prod = pbi_client.deploy_all_pipeline_stage('Testing Environment', 'Testing Environment [Prod]', '4846741C-9AC0-456B-A0F2-6BA8C4D1D720', "Test")
time.sleep(5)
add_user_workspace = pbi_client.add_user_to_workspace('Testing Environment [Dev]', {"identifier": "admin@M365x51939963.onmicrosoft.com", "groupUserAccessRight": "Admin", "principalType": "User"})
time.sleep(5)
add_user_pipeline = pbi_client.add_user_to_pipeline('Testing Environment', {"identifier": "admin@M365x51939963.onmicrosoft.com", "pipelineUserAccessRight": "Admin", "principalType": "User"})

print (create_workspace)
print (set_workspace_capacity)
print (import_pbix_file)
print (create_pipeline)
print (assign_pipeline_workspace)
print (deploy_pipeline_test)
print (deploy_pipeline_prod)
print (add_user_workspace)
print (add_user_pipeline)
