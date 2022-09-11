# sat5cfg-to-ansible
Convert Red Hat Satellite 5 configuration channels to ansible roles

## Test

``` shell

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Usage

1. put the json files in this path
2. run `convert.py`
3. this will output the roles and playbooks to the `output` directory

## Container Image

``` shell

podman build -t sat5cfg .

```

