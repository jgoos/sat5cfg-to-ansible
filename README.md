### sat5cfg-to-ansible
Convert Red Hat Satellite 5 configuration channels to ansible roles

#### Test

``` shell

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

#### Usage

1. put the json files in this path
2. run `sat5cfg2ansible.py <path_to_local_files>`
3. this will output the roles and playbooks to the `transformed_files` directory

#### Container Image

``` shell

podman build -t sat5cfg .

```

#### Run container

``` shell

podman run -it -v <path_to_local_files>:/data:Z sat5cfg

```
