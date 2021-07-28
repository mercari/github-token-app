# Github Token App

Github Token App is a package for generating short lived github tokens (expires in 1 hour) with minimum necessary permissions.

Currently, the code generates read and write github token to the specific list of repositories.
- An example of read github token is git clone.
- An example of write github token is git push.


The github token app also provides a CLI which can be used to generate a github token to authenticate to github.

# Installation

```bash
pip install github-token-app
```

## Required Environment Variables

- **BASE64_PRIVATE_PEM_KEY**: This is the private pem key for the github-app encoded in base64.
- **GITHUB_APP_ID**: App ID
- **INSTALLATION_ID**: Installation Id for App/Org Pair (if you don't know, it can be generated from the second step below)


## What the code does?


1. The code is for authenticating a [github app as an installation](https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps#authenticating-as-an-installation). Installations are created from a Github app settings (Install App).

2. Under Install App, click on the account settings. You will find the installation ID in the URL https://github.com/apps/my-app-name/installations/**INSTALLATION_ID**. Set the **INSTALLATION_ID** as environment variable based on your required access.

    Alternatively, the code contains `get_installations` function which can be called by CLI command `gta installations`. It returns a response of list of installations. The `id` attributes in the responses are the installation ids. 

3. Finally, there are three methods read, write and write-pr. That generates token to perform respective actions to specific repositories.


## Commands
- **read**

Generates token which grants read-only access to specified Github Repository

```bash
gta read [list of repositories]
gta read my-private-repo
```

- **write**

Generates token which grants write access to specified Github Repository

```bash
gta write [list of repositories]
gta write my-private-repo
```

- **write-pr**

Generate token which grants write access to specified Github Repository along with permission to create prs.

```bash
gta write-pr [list of repositories]
gta write-pr my-private-repo
```

## Using the generated token

- **Cloning a repository**

```bash
git clone https://x-access-token:$GITHUB_TOKEN@github.com/my-org/my-private-repo.git
```

- **Writing to a repository**

```bash
git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/my-org/my-private-repo.git"
git config --global user.email "<>"
git config --global user.name "my-username"
```


## Contribution

Please read the CLA carefully before submitting your contribution to Mercari.
Under any circumstances, by submitting your contribution, you are deemed to accept and agree to be bound by the terms and conditions of the CLA.

https://www.mercari.com/cla/

## License

Copyright 2021 Mercari, Inc.

Licensed under the MIT License.