# Converting Red Hat Satellite 5 Configuration Channels to Ansible Roles

This script converts Red Hat Satellite 5 configuration channels to ansible roles.

## Usage

To use the script, follow these steps:
1. Install the requirements by running `yum install spacewalk-utils` and `pip install -r requirements.txt`.
2. Dump the desired configuration channel(s) from Satellite 5 to a JSON file using the command `spacewalk-export --channel channel_name --output-file file.json`.
3. Activate the virtual environment by running `source venv/bin/activate`.
4. Run the script using the command `python sat5cfg2ansible.py <path_to_json_files>`.
5. The script will output the generated ansible roles and playbooks to the `<path_to_json_files>/transformed_files` directory.

## Requirements

The following requirements are necessary to use this script:
- spacewalk-utils: This package is required to export configuration data from Red Hat Satellite 5.
- libmagic C library: This library is required for the python-magic package, which is used to identify the file type of the dumped JSON data. See the python-magic documentation (https://pypi.org/project/python-magic/) for installation instructions.

## Usage via Container

This script can also be run using a container image.

### Building the Container Image

To build the container image, run the following command:

``` shell
podman build -t sat5cfg .
```

### Running the Container

To convert the JSON files using the container, run the following command:

Copy code

`podman run -it -v <path_to_local_files>:/data:Z sat5cfg`

This will mount the local files at `<path_to_local_files>` to the `/data` directory in the container, and then run the container using the `sat5cfg` image.

#### Notes

-   Make sure to replace `<path_to_local_files>` with the actual path to the local JSON files that you want to convert.
-   The `:Z` flag is required to allow the container to access the files with the correct SELinux labels.
