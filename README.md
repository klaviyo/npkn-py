
# npkn: Official CLI for Napkin.io

npkn lets you deploy code to [Napkin.io](https://napkin.io) from your local 
command line. It is currently available as an alpha release and is subject to 
change.


## Commands

```
npkn help

    Show available commands, npkn install location, and current version.
```

```commandline
npkn new <name> -r,--runtime=[:runtime] -w,--workspace=[:workspacename]

    Create a new Napkin function.

Arguments
---------

<name> The name of the new function

Options
-------
    -r, --runtime [:runtime] 
    
        The runtime to use. One of: 
        - python3.8
        - node14.x
        
        If no runtime is provided, npkn will use whatever runtime is set via the
        NPKN_DEFAULT_RUNTIME environment variable. If neither is set, npkn will exit.
    
    -w, --workspace [:workspacename] 
    
        The name of the workspace in which to create the new function. Defaults to
        the default account workspace if not provided.

```

```commandline
npkn pull <name>

    Copy an existing function from napkin.io to your local machine's working directory.

Arguments
---------
    <name> 
        
        The name of the function to pull. If pulling from a non-default workspace, use the following syntax:
        <workspacename:functionname>. For example, if pulling a function called 'foo' from a workspace called 'bar':
        
            npkn pull foo:bar
```

```commandline
npkn run -n,--name=[:name]

    Run a function on Napkin and get the result

Options
-------

    -n, --name [:name] 
    
        Name of function to run. The function named [:name] must be in the 
        current working directory. If no name is provided, npkn will look for a 
        metadata.yaml file and function.py file in the current working directory 
        and run that. If neither is found, npkn will exit.
```

```commandline
npkn deploy -n,--name=[:name]

    Deploy local changes to napkin.io

Options
-------
    
     -n, --name [:name] 
    
        Name of function to deploy. The function named [:name] must be in the 
        current working directory. If no name is provided, npkn will look for a 
        metadata.yaml file and function.py file in the current working directory 
        and deploy that. If neither is found, npkn will exit.   
```

## Installation
### From Github
```commandline
pip install git+https://github.com/NapkinHQ/npkn-py.git
```
### PyPI (_Coming soon_)


## Set Credentials
1. First, fill out the [Google Form](https://forms.gle/BVyJXgMCC7CGJ5Eh8) for access. We will send your credentials using the email you used to sign up for Napkin.
2. Once you've received your credentials, set the following environment variables:
```
NPKN_ACCOUNT_ID=xxxxxxx
NPKN_SECRET_KEY=xxxxxxx
```

### Manual Installation
1. Install [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) (if not already installed)
2. Clone and initialize the repo
```commandline
git clone https://github.com/NapkinHQ/npkn-py.git
cd npkn-py
poetry install
```
3. Try out via Poetry shell
```commandline
poetry shell
> npkn help
```

### Optional Environment Variables
These environment variables are optional and mostly intended for development purposes:
```commandline
NPKN_LOG_LEVEL
NPKN_API_HOST
```

***

## Usage Examples

**Create a new Napkin Python function**

```commandline
>>> npkn new -r python3.8 tell-time

Creating new function 'tell-time' ✅

>>> cd tell-time && ls -la

drwxrwxr-x 2 user user 42 Jun 23 22:32 .
drwxrwxr-x 4 user user 59 Jun 23 22:32 ..
-rw-rw-r-- 1 user user 90 Jun 23 22:32 function.py
-rw-rw-r-- 1 user user 97 Jun 23 22:32 meta.yaml
```

**Run the function**

```commandline
>>> npkn run

Function: tell-time | Workspace: default
{'body': 'hello, world!', 'headers': {'content-type': 'text/html'}, 'logs': [], 'returnValue': 0, 'statusCode': 200, 'status_code': 200}

```

**Update function code and re-run**

`function.py`
```python
from napkin import response
from datetime import datetime

response.body = f"The current time is {datetime.now()}"
```

```commandline
>>> npkn run

Function: tell-time | Workspace: default
Syncing code ✅
{'body': 'The current time is 2022-06-23 22:37:23.676056', 'headers': {'content-type': 'text/html'}, 'logs': [], 'returnValue': 0, 'statusCode': 200, 'status_code': 200}
```
***

**Use 3rd party modules**

To use modules from PyPI, list the function module requirements in your `meta.yaml` file. You can check which modules are available from the Napkin UI.

`meta.yaml`
```yaml
name: tell-time
runtime: python3.8
uid: <your user id>
workspace: <your workspace id>
modules:
 pytz: "*"
```

Update function code

`function.py`
```python
from napkin import response
from datetime import datetime
from pytz import timezone

tz = timezone("America/Costa_Rica")
current_tz_time = tz.localize(datetime.now())

response.body = f"The current time in Costa Rica is {current_tz_time}"
```

Run it again!
```commandline
>>> npkn run

Function: tell-time | Workspace: default
Syncing code ✅
Syncing modules ✅
{'body': '"The current time in Costa Rica is 2022-06-23 23:00:26.558193-06:00"', 'headers': {'content-type': 'text/html'}, 'logs': [], 'returnValue': 0, 'statusCode': 200, 'status_code': 200}
```

**Use Environment Variables**

Add your environment variables to the `env` field of your `meta.yaml` file.

`meta.yaml`
```yaml
name: tell-time
runtime: python3.8
uid: <your user id>
workspace: <your workspace id>
modules:
 pytz: "*"
env:
  TZ: America/Costa_Rica
```

Then use the environment variable as you normally would in your function.
`function.py`
```python
from napkin import response
from datetime import datetime
from pytz import timezone
import os

tz = timezone(os.getenv("TZ"))
current_tz_time = tz.localize(datetime.now())

response.body = f"The current time in Costa Rica is {current_tz_time}"
```

Running it again...
```commandline
>>> npkn run

Function: tell-time | Workspace: default
Syncing code ✅
Syncing environment ✅
{'body': '"The current time in Costa Rica is 2022-06-23 23:02:26.5589233-06:00"', 'headers': {'content-type': 'text/html'}, 'logs': [], 'returnValue': 0, 'statusCode': 200, 'status_code': 200}
```

**Deploying Code**

When you're ready to deploy your code to your function's endpoint, just run `npkn deploy`.

```commandline
>>> npkn deploy

Function: tell-time | Workspace: default
Deploying ✅

>>> curl https://my-account.npkn.net/tell-time
The current time in Costa Rica is 2022-06-23 23:08:27.104832-06:00

```

***

## Public API

Under the hood, [npkn-py](https://github.com/NapkinHQ/npkn-py) uses Napkin's public REST API (currently in alpha and subject to changes) to interact with the Napkin platform.
Official documentation for the public API remains under development; however, below is included a brief API reference to help users that wish to fork or contribute to this repo.

#### Host: `https://api.napkin.io`

### Authentication

The following headers should be set in the API request.
```
napkin-api-key: xxxxxx
napkin-user-uid: xxxxx
```

The values for the headers are the same as the account id and secret key that you use for the Napkin CLI.

### Endpoints

**Get user account object**

GET `/api/1/account`

Response
```js
{
    "workspaces": [
        {
            "members": [
                // ...
            ],
            "name": "xxx",
            "objects": {
                "xxxxxxxxx": {
                    "description": null,
                    "name": "testing2",
                    "path": "/",
                    "requireAuth": "0",
                    "runtime": "python3.8",
                    "type": "napkin",
                    "uid": "xxxxxxxxxx",
                    "version": "v1",
                    "visibility": "private"
                },
                // ...
            },
            "runtimes": {
                "nodejs14.x": "PROVISIONED",
                "python3.8": "PROVISIONED"
            },
            "type": "PRO_TEAM",
            "uid": "xxxxxxxxx",
            "version": "v1"
        }
    ]
}
```


**Sync function modules**

POST `/api/1/sync/modules`

Request Body
```json
{
  "modules": {
    "requests": "*"
  },
  "function_uid": "xxxxx"
}
```

Response
```json
{
  "success": true, 
  "modules": {
    "requests": "2.9.2"
  }
}
```


**Sync function environment variables**

POST `/api/1/sync/env`

Request Body
```json
{
  "env": {
    "MY_VAR": "hello"
  },
  "function_uid": "xxxxx"
}
```

Response
```json
{
  "env": {
    "MY_VAR": "hello"
  }
}
```
**Sync function code (pre-deploy)**

POST `/api/1/sync/code`

Request Body
```json
{
  "code_str": "print(\"hello world\")\n",
  "function_uid": "xxxxx"
}
```

Response
```js
{
  "function": {
    // ...
  }
}
```

**Retrieve a function object**

GET `/api/1/function`

Request Args
```
uid=xxxxx
```

Response
```js
{
  "function": {
    // function properties
  },
  "env": {
    "MY_VAR": "hello"
  }
}
```


**Create a new Napkin function**

POST `/api/1/new`

Request Body
```json
{
  "runtime": "python3.8",
  "workspace_id": "xxxxxx",
  "function_name": "my-new-function"
}
```

Response
```js
{
  "napkin": {
    // function properties
  },
  "workspace": {
    // function workspace properties
  }
}
```

**Run a Napkin function using current, un-deployed code**

POST `/api/1/run`

Request Body
```json
{
  "uid": "functionUidXXX",
  "workspaceUid": "workspaceUid"
}
```

Response
```js
{
  "logs": [],
  "statusCode": 200,
  "status_code": 200, // duplicated for legacy reasons
  "headers": {},
  "body": {}
}
```

**Deploy Napkin function code**

POST `/api/1/deploy`

Request Body
```json
{
  "uid": "functionUidXXX"
}
```

Response
```json
{
  "success": true
}
```
