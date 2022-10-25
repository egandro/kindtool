# Todo's

## Documenation

- Ship with a super simple Kindfile. Add examples in the documentation.

## Kindfile

Support private registries <https://kind.sigs.k8s.io/docs/user/private-registries/>

```
private_registry=true
private_registry_config=.$HOME/.secret_registry/config.json
... more to come e.g. environment variables
```

Install k8s dashboard

```
# installs the dashbard and creates a token file to `config_dir`/token
dashboard=true

# install the dashboard, create dashbord user, create token, run dashboard with port forwarding
# $ kindgen dashboard
#       your token is: <some data here>
#       start your browser here: <http://localhost:whatever>
```

Support customizable templates

```
teplate_dir=./my_templates

# dumps the Jinja2 templates (in case you want to customize / change code generation)
# you can have a `teplate_dir=./my_templates` entry in your Kindfile
# $ kindtool dump_templates <dir>
```

Dynamic port creation for ingress.

```
# empty specification - find an unused port in docker
ingress_http_port=
ingress_https_port=

# returns the dynamic - in case you have auto port number enabled
# $ kindtool get ingress_http_port
# $ kindtool get ingress_https_port
```

## Features

- add a way to detect the `main ip` (whatever that means) by a script. Currently a `hostname --all-ip-addresses` is used. That is not portable.