#!/usr/bin/env python

import logging
import requests

from typing import List
from .workspaces import Workspaces

class Dashboards:
    def __init__(self, client):
        self.classKeyword = 'dashboards'
        self.client = client
        self.workspaces = Workspaces(client)
        self.dashboards = []

    # https://docs.microsoft.com/en-us/rest/api/power-bi/dashboards/get-dashboards-in-group
    def get_dashboards(self, workspace_name: str) -> List:
        self.client.check_token_expiration()
        # self.workspaces.get_workspace_id(workspace_name)
        url_extension = ''
        if workspace_name:
            self.workspaces.get_workspace_id(workspace_name)
            url_extension = "groups/" + self.workspaces.workspace[workspace_name] + '/' 
        else:
            workspace_name = 'My Workspace'
        
        url = self.client.base_url + url_extension + self.classKeyword
        # url = self.client.base_url + "groups/" + self.workspaces.workspace[workspace_name] + "/dashboards"
        
        response = requests.get(url, headers = self.client.json_headers)

        if response.status_code == self.client.http_ok_code:
            for item in response.json()['value']:
                self.dashboards.append(item)
            return self.dashboards
        else:
            logging.error(f"Failed to retrieve dashboards from workspace: {workspace_name}.")
            self.client.force_raise_http_error(response)
    