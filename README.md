### sat5cfg-to-ansible

Convert Red Hat Satellite 5 configuration channels to ansible roles


#### Usage via script


1. Install the requirements.
2. dump file from Satellite 5 to json.
3. run `sat5cfg2ansible.py <path_to_json_files>`.
4. this will output the roles and playbooks to the `<path_to_json_files>/transformed_files` directory.

##### Requirements

``` shell

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

Also install the libmagic C library. See: https://pypi.org/project/python-magic/

#### Usage via container

##### Build the container Image

``` shell

podman build -t sat5cfg .

```

##### Run the container

Or convert the json files using a container.

``` shell

podman run -it -v <path_to_local_files>:/data:Z sat5cfg

```
