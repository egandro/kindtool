# Todo's

## kindfile.yaml

Support customizable templates

```
teplate_dir=./my_templates

# dumps the Jinja2 templates (in case you want to customize / change code generation)
# you can have a `teplate_dir=./my_templates` entry in your kindfile.yaml
# $ kindtool dump_templates <dir>
```


## Features

- add a way to detect the `main ip` (whatever that means) by a script. Currently a `hostname --all-ip-addresses` is used. That is not portable.

- implement "status" command

- add a nice common way to wait for pods, deployments, services, service account, etc. the bash scripts are a mess and trial/error based

## Application support

Add a way to install "standard applications", e.g.

- postgres
- mysql
- mssql
- mariadb
- redis
- logger tools

```
#
# probably via a Kindfile section ... probably we create a directory and add the app yamls here...
# needs some refinement
#
$ kindtool app install postgresql
```