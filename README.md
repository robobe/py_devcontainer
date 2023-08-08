# Python project using VSCode devcontainer

## Multistage
- Create multistage docker
    - base
    - dev
- Set devcontainer `target` attribute to requested target

```Dockerfile
FROM ubuntu:22.04 as python_base
...
FROM python_base as python_dev
...

```

```json
{
    "name": "python-dev",
    "build": {
        "dockerfile": "Dockerfile",
        "context": "..",
        "target": "python_dev"
    }
}
```

!!! note "build multistage docker"
    ```bash
    docker build --target development
    ```
     

---

## Permission
- Dockerfile: Add none root user (named user)
- Set devcontainer login as that user


```dockerfile title="Dockerfile"
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo tzdata \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/* 
```

```json title="devcontainer.json
"remoteUser": "user",
```

!!! note "remoteUser vs containerUser"
    - **remoteUser**: The user VS Code Server will be started with. The default is the same user as the container.
    - **containerUser**: The user the container will be started with. The default is the user on the Docker image.
     
---

## requirements
There at lest two option to install `requirement.txt`

- **Option 1**: Install `requirement.txt` using `devcontainer.json` property like `postCreateCommand`

```json title="devcontainer.json"
{
    "postCreateCommand": "pip install -r /workspaces/py_docker_tutorial/requirements-dev.txt",
}
```

- **Option 2**: Install `requirements` as docker layer

```docker title="Dockerfile"
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-`cache-dir --upgrade -r /home/user/requirements-dev.txt
```

---

## develop
- Register the project

```bash
pip install --prefix=~/.local -e .
```
---

## build wheel and deb

```dockerfile 
RUN apt-get update && \
    apt-get install -y \
        python3-all \
        debhelper \
        dh-python \
        python3-stdeb \
        locales \
        locales-all \
        && rm -rf /var/lib/apt/lists/*
```

### vscode tasks

```json title="tasks.json"
"tasks": [
        {
            "label": "build deb",
            "type": "shell",
            "command": "python3 setup.py --command-packages=stdeb.command bdist_deb",
            "problemMatcher": []
        },
        {
            "label": "build wheel",
            "type": "shell",
            "command": "python3 setup.py bdist_wheel",
            "problemMatcher": []
        },

    ]
```

!!! note "build output folder"
    - **deb**: deb_dist folder
    - **wheel**: dist folder
     
---

## Testing
- Install pytest (requirements-dev.txt)
- config vscode

```json title="devcontainer.json"
{
    "customizations": {
        "vscode": {
            "settings": {
                "python.testing.pytestArgs": [
                                "tests"
                            ],
                "python.testing.unittestEnabled": false,
                "python.testing.pytestEnabled": true
            }
        }
    }
}
```

---

## clean

- Clean Task

```json title=".vscode/tasks.json"
{
    "label": "clean",
    "type": "shell",
    "command": "/usr/bin/bash -x scripts/clean.sh",
    "problemMatcher": []
}
```

```bash title="scripts/clean.sh"
rm -rf deb_dist
rm -rf dist
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
```

!!! tip "run bash script without execute permission set"
    ```bash
    bash -x scripts/clean.sh
    ```
     
---

## python tools
- mypy
- formatter (black, isort)
- flake8 (linter)

!!! tip "Migration to Python Tools Extensions"
     [Migration to Python Tools Extensions
](https://github.com/microsoft/vscode-python/wiki/Migration-to-Python-Tools-Extensions)

---

## VSCode extensions
- Python
- Tabout
- Code Spell Checker
- Tasks

#### TabOut
Tab out quotes, brackets. etc
[marketplace](https://marketplace.visualstudio.com/items?itemName=albert.TabOut)

#### Code Spell Checker
Spelling checker for source code
[marketplace](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
#### Tasks
Load VSCode Tasks into Status Bar.
[marketplace](https://marketplace.visualstudio.com/items?itemName=actboy168.tasks)

Tools extensions
- [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
- [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)
- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)


##### TODO
- mypy type check not work wall, return to mypy self install `pip install mypy` with deprecated settings `"python.linting.mypyEnabled": true,`
- Need to check isort extension usage
- [Migration to Python Tools Extensions](https://github.com/microsoft/vscode-python/wiki/Migration-to-Python-Tools-Extensions)


#### tasks
##### mypy

```json
"tasks": [
        {
            "label": "mypy",
            "type": "shell",
            "command": "mypy ${file}",
            "options": {
                "statusbar": {
                    "color": "#22C1D6",
                    "tooltip": "run mypy",
                    "label": "mypy",
                    "filePattern": "py"
                }
            }
        }
]
```

---


#### docker-compose
Using docker compose override capability
- Use production / deploy compose file
- Override/Add settings to support development

for example add shared volume for vscode to mount code on remote

```yaml
version: '3.7'

services:
  app:
    volumes:
      - ./:/workspace
```



```json title="devcontainer.json" linenums="1" hl_lines="2-6"
{
    "name": "python-dev",
    "dockerComposeFile": [
        "../docker-compose.yaml",
        "./docker-compose.dev.yaml"
    ],
    "service": "app",
    "workspaceFolder": "/workspace",
    "postCreateCommand": "/usr/bin/bash -x ./.devcontainer/postCreateCommand.sh",
    "remoteUser": "user",
    "remoteEnv": {
        "PATH": "${containerEnv:PATH}:/home/user/.local/bin"
    },
    "containerUser": "user",
    "customizations": {
    }
}
```

### VSCode Server
vscode-server install on container

```
/vscode/vscode-server/bin/linux-x64/<commit>
```

### Workspaces
code mount under

```
/workspaces/<project name>
```
---

## References
- [devcontainer.json schema](https://containers.dev/implementors/json_schema/)
- [Variables Reference](https://code.visualstudio.com/docs/editor/variables-reference)