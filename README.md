# Configurer

Python 3.7+ / Docker

A config render tool based on Jinja template variables.


## Variable precedence

Configurer will use the following priority order:

1. Variables from the env file
2. Variables in the Environment context


### Defining variables
You can define variables inside your config using the Jinja2 templating system.

    config: {{ my_variable }}

Additionally Jinja2 filters let you transform the value of a variable within a template expression using filters.
Check out the [built-in filters](http://jinja.pocoo.org/docs/2.10/templates/#builtin-filters) to know more.


## Running configurer

The easier way to run configurer is using docker. Keep reading to render the demo project:

### Using docker

Set your paths and run:

    export MY_CONFIG_FOLDER=$(pwd)/demo/config_templates
    export MY_OUTPUT_FOLDER=$(pwd)/demo/config_output
    export MY_VAR_FILE=$(pwd)/demo/vars.txt
    docker run --rm --volume $MY_CONFIG_FOLDER:/source:ro --volume $MY_OUTPUT_FOLDER:/output --volume $MY_VAR_FILE:/vars/var_file:ro iago1460/configurer

Or keep it running watching for changes:

    docker run --rm --volume $MY_CONFIG_FOLDER:/source:ro --volume $MY_OUTPUT_FOLDER:/output --volume $MY_VAR_FILE:/vars/var_file:ro iago1460/configurer --watch

### In a virtual environment

    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

```bash
$ python3 -m configurer -h
usage: __main__.py [-h] [--vars VARS_PATH] --output OUTPUT_PATH --source
                   SOURCE_PATH [--watch]

Renders files replacing variables when possible.
Example usage:
python3 -m configurer --source ./demo/config_templates --output ./config

optional arguments:
  -h, --help            show this help message and exit
  --vars VARS_PATH      Path to the file with variables.
  --output OUTPUT_PATH  Path to the output directory.
  --source SOURCE_PATH  Path to the source directory.
  --watch               Keep watching for changes.
  --verbose             Makes curl verbose during the operation. Useful for debugging and seeing what is going on "under the hood".
```
