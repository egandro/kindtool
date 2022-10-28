#!/bin/bash

# https://kind.sigs.k8s.io/docs/user/local-registry/

REGISTRY_NAME="{{internal_registry_docker_name}}"

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}


echo "deleting internal docker registry '${REGISTRY_NAME}'"
docker rm -f "${REGISTRY_NAME}"