#!/usr/bin/env python

import logging

from pbi_rest_client.utils.utils import Utils
from pbi_rest_client.config import BaseConfig
from pbi_rest_client.capacities import Capacities
from pbi_rest_client.rest_client import RestClient
from pbi_rest_client.workspaces import Workspaces
from pbi_rest_client.pipelines import Pipelines
from pbi_rest_client.dataflows import Dataflows
from pbi_rest_client.datasets import Datasets
from pbi_rest_client.dashboards import Dashboards
from pbi_rest_client.gateways import Gateways
from pbi_rest_client.reports import Reports
from pbi_rest_client.imports import Imports

logging.basicConfig(level=logging.INFO)

client = RestClient()
utils = Utils()
config = BaseConfig()
capacities = Capacities(client.authz_header, client.token, client.token_expiration)
# workspaces = Workspaces(client.authz_header, client.token, client.token_expiration)
workspaces = Workspaces()
pipelines = Pipelines(client.authz_header, client.token, client.token_expiration)
dataflows = Dataflows(client.authz_header, client.token, client.token_expiration)
datasets = Datasets(client.authz_header, client.token, client.token_expiration)
dashboards = Dashboards(client.authz_header, client.token, client.token_expiration)
gateways = Gateways(client.authz_header, client.token, client.token_expiration)
reports = Reports(client.authz_header, client.token, client.token_expiration)
imports = Imports(client.authz_header, client.token, client.token_expiration)

# print (utils.get_keyvault_secret('appconfig'))
# print (utils.get_appconfig_keys(key_filter = 'workspace-name*'))
# print (utils.get_appconfig_keys())
# print (utils.get_appconfig_feature_flags(feature_flag_name = 'service-account'))

# print (workspaces.create_workspace('Testing Environment [Dev]'))
# print (workspaces.create_workspace('Testing Environment [Test]'))
# print (workspaces.create_workspace('Testing Environment [Prod]'))

# print (capacities.set_workspace_capacity('Testing Environment [Dev]', '00000000-0000-0000-0000-000000000000'))
# print (capacities.set_workspace_capacity('Testing Environment [Test]', '00000000-0000-0000-0000-000000000000'))
# print (capacities.set_workspace_capacity('Testing Environment [Prod]', '00000000-0000-0000-0000-000000000000'))

# print (capacities.set_workspace_capacity('Testing Environment [Dev]', '4846741C-9AC0-456B-A0F2-6BA8C4D1D720'))
# print (capacities.set_workspace_capacity('Testing Environment [Test]', '4846741C-9AC0-456B-A0F2-6BA8C4D1D720'))
# print (capacities.set_workspace_capacity('Testing Environment [Prod]', '4846741C-9AC0-456B-A0F2-6BA8C4D1D720'))

print (workspaces.get_workspaces())

# print (pipelines.create_pipeline('Testing Environment'))
# print (pipelines.assign_pipeline_workspace('Testing Environment', 'Testing Environment [Dev]', 'dev'))
# print (pipelines.assign_pipeline_workspace('Testing Environment', 'Testing Environment [Test]', 'test'))
# print (pipelines.assign_pipeline_workspace('Testing Environment', 'Testing Environment [Prod]', 'prod'))
# print (pipelines.pipeline_stage_deploy_all('Testing Environment', 'promote', 'Dev'))
# print (pipelines.pipeline_stage_deploy_all('Testing Environment', 'demote', 'Test'))
# print (pipelines.pipeline_stage_deploy_selective('Testing Environment', 'promote', 'Dev'))

# print (dataflows.get_dataflow_storage_accounts())
# print (dataflows.get_dataflows('Testing Environment [Dev]'))
# print (dataflows.get_dataflow('Testing Environment [Dev]', 'SQLDataFlow'))
# print (dataflows.get_dataflow_datasources('Testing Environment [Dev]', 'SQLDataFlow'))
# print (dataflows.update_dataflow('Testing Environment [Dev]', 'SQLDataFlow'))
# print (dataflows.delete_dataflow('Testing Environment [Dev]', 'SQLDataFlow'))

# print (datasets.take_dataset_owner('Testing Environment [Dev]'))
# print (datasets.get_datasets())
# print (datasets.get_dataset_dataflows('Testing Environment [Dev]'))
# print (datasets.get_datasets_in_workspace('Testing Environment [Dev]'))
# print (datasets.get_dataset_id('SQLTableDemo'))
# print (datasets.get_dataset_parameters('SQLTableDemo'))
# print (datasets.get_dataset_in_group_parameters('SQLTableDemo', 'Testing Environment [Dev]'))
# print (datasets.get_datasources('SQLTableDemo', 'Testing Environment [Dev]'))
# print (datasets.patch_dataset_in_group_datasources('SQLTableDemo', 'Testing Environment [Dev]'))

# print (dashboards.get_dashboards('Testing Environment [Dev]'))

# print (imports.import_file_into_workspace('Testing Environment [Dev]', 'SQLTableDemo', 'SQLTableDemo.pbix', restore_from_blob = True, blob_container_name = 'test-container', dataflow = False, skip_report = False))
# print (imports.import_file_into_workspace('Testing Environment [Dev]', 'SQLDataFlow', 'SQLDataFlow.json', restore_from_blob = False, blob_container_name = None, dataflow = True))
# print (imports.import_file_into_workspace('Testing Environment [Dev]', False, 'FirstLast.json', 'SharePointListDemo'))
# print (imports.import_file_from_blob_into_workspace('Testing Environment [Dev]', 'SQLTableDemo', 'test-container', 'SQLTableDemo.pbix', False, False))

# print (gateways.get_gateways())

# print (gateways.get_gateway('testGateway'))
# print (gateways.get_datasources('testGateway'))
# print (gateways.get_datasource('testGateway', 'testDataSource'))
# print (gateways.get_datasource_status('testGateway', 'testDataSource'))
# print (gateways.update_datasource('testGateway', 'testDataSource'))
# print (gateways.create_datasource('testGateway', 'testDataSource'))

# print (reports.get_reports('Testing Environment [Dev]'))
# print (reports.get_report('Testing Environment [Dev]', 'SQLTableDemo'))
# print (reports.export_report('Testing Environment [Dev]', 'SQLTableDemo', 'test-container'))