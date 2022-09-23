import base64
import json
import os
from pprint import pprint
from typing import Dict, List

import requests
from github3 import apps


def get_default_app():
    if not hasattr(get_default_app, "app"):
        pem_key = os.getenv("BASE64_PRIVATE_PEM_KEY", "")
        if not pem_key:
            raise RuntimeError("Missing Environment Variable: 'BASE64_PRIVATE_PEM_KEY'")

        pem_key = base64.b64decode(pem_key)

        github_app_id = os.getenv("GITHUB_APP_ID", "")
        if not github_app_id:
            raise RuntimeError("Missing Environment Variable: 'GITHUB_APP_ID'")

        try:
            github_app_id = int(github_app_id)
        except ValueError:
            raise ValueError(f"Invalid $GITHUB_APP_ID={github_app_id}, NOT a valid integer")

        installation_id = os.getenv("INSTALLATION_ID", "")
        if not installation_id:
            print("[Warning] Missing Environment Variable: 'INSTALLATION_ID'")
        else:
            try:
                installation_id = int(installation_id)
            except ValueError:
                raise ValueError(f"Invalid $INSTALLATION_ID={installation_id}, NOT a valid integer")

        get_default_app.app = GithubApp(
            app_id=github_app_id,
            private_pem_key=pem_key,
            installation_id=installation_id,
        )

    return get_default_app.app


class GithubApp:
    def __init__(self, app_id: int, private_pem_key: bytes, installation_id: int):
        self.app_id = app_id
        self.installation_id = installation_id
        self.private_pem_key = private_pem_key

    def get_global_access_token(self) -> str:
        """Global access token here means that an access token with all the scopes available"""
        headers = apps.create_jwt_headers(
            private_key_pem=self.private_pem_key,
            app_id=self.app_id,
            expire_in=600,  # Max allowed: 60*10 (10 minutes)
        )
        url = f"https://api.github.com/app/installations/{self.installation_id}/access_tokens"
        response = requests.post(url=url, headers=headers)
        if response.status_code != 201:
            raise Exception("Failed to get the global access token. " f"Status code: {response.status_code} " f"Response: {response.json()} ")
        return response.json()["token"]

    def get_repo_ids(self, repo_names: List[str]) -> List[int]:
        """Get the list of repo ids from list of repo names"""
        global_access_token = self.get_global_access_token()
        headers = {
            "Authorization": f"token {global_access_token}",
        }
        headers.update(apps.APP_PREVIEW_HEADERS)
        page_number = 1
        repo_ids = []
        while True:
            url = f"https://api.github.com/installation/repositories?page={page_number}"

            response = requests.get(url=url, headers=headers)
            if response.status_code != 200:
                raise Exception("Failed to get fetch repositories. " f"Status code: {response.status_code} " f"Response: {response.json()} ")
            if not response.json()["repositories"]:
                # Break the while loop if page doesn't have repositories.
                break

            for repo in response.json()["repositories"]:
                if repo["name"] in repo_names:
                    repo_ids.append(repo["id"])

            # Go to next page
            page_number += 1

        if len(repo_names) != len(repo_ids):
            raise Exception("Github app doesn't have scope for all the repos")

        return repo_ids

    def get_access_token(self, repo_names: List[str], permissions: Dict[str, str]) -> str:
        """
        Get the access token using repo ids
        Args:
            repo_names: Names of the repositories
            permissions: Eg: {"contents": "write", "pull_requests": "write", "metadata": "read"}
        References:
            https://docs.github.com/en/rest/reference/apps#create-a-scoped-access-token--parameters
        """

        repo_ids = self.get_repo_ids(repo_names)
        headers = apps.create_jwt_headers(private_key_pem=self.private_pem_key, app_id=self.app_id, expire_in=60)

        url = f"https://api.github.com/app/installations/{self.installation_id}/access_tokens"
        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(
                {
                    "repository_ids": repo_ids,
                    "permissions": permissions,
                }
            ),
        )
        if response.status_code != 201:
            raise Exception("Failed to get the access token. " f"Status code: {response.status_code} " f"Response: {response.json()} ")

        return response.json()["token"]

    def get_read_token(self, repo_names: List[str]) -> str:
        """
        Gets a Github Token with read permission to repositories
        Args:
            repo_names: List of Repositories
        """
        permissions = {"contents": "read", "metadata": "read"}
        return self.get_access_token(repo_names, permissions)

    def get_write_token(self, repo_names: List[str]) -> str:
        """
        Gets a Github Token with Write Permission to repositories
        Args:
            repo_names: list of repositories
        """
        permissions = {"contents": "write", "metadata": "read"}
        return self.get_access_token(repo_names, permissions)

    def get_write_pr_token(self, repo_names: List[str]) -> str:
        """
        Gets a Github Token with Write + PR Permission to repositories
        Args:
            repo_names: list of repositories
        """
        permissions = {
            "contents": "write",
            "pull_requests": "write",
            "metadata": "read",
        }
        return self.get_access_token(repo_names, permissions)

    def get_installations(self):
        headers = apps.create_jwt_headers(
            private_key_pem=self.private_pem_key,
            app_id=self.app_id,
            expire_in=600,  # Max allowed: 60*10 (10 minutes)
        )
        url = "https://api.github.com/app/installations"

        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise Exception("Failed to get fetch repositories. " f"Status code: {response.status_code} " f"Response: {response.json()} ")
        return response.json()


def get_read_token(repo_names: List[str]) -> None:
    """
    Gets a Github Token with read permission to repositories
    Args:
        repo_names: List of Repositories
    """
    github_app = get_default_app()
    print(github_app.get_read_token(repo_names))


def get_write_token(repo_names: List[str]) -> None:
    """
    Gets a Github Token with Write Permission to repositories
    Args:
        repo_names: list of repositories
    """
    github_app = get_default_app()
    print(github_app.get_write_token(repo_names))


def get_write_pr_token(repo_names: List[str]) -> None:
    """
    Gets a Github Token with Write + PR Permission to repositories
    Args:
        repo_names: list of repositories
    """
    github_app = get_default_app()
    print(github_app.get_write_pr_token(repo_names))


def get_installations():
    """
    Get the list of installations for the authenticated app.
    """
    github_app = get_default_app()
    pprint(github_app.get_installations())
