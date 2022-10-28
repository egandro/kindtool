#!/bin/bash

# https://kind.sigs.k8s.io/docs/user/local-registry/

REGISTRY_NAME="{{internal_registry_docker_name}}"
REGISTRY_PORT={{internal_registry_docker_port}}

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}


if [ "$(docker inspect -f "{""{".State.Running"}""}" "${REGISTRY_NAME}" 2>/dev/null || true)" != 'true' ]; then
    echo "creating internal docker registry '${REGISTRY_NAME}' at http://localhost:${REGISTRY_PORT}"
    docker run \
        -d --restart=always -p "127.0.0.1:${REGISTRY_PORT}:5000" --name "${REGISTRY_NAME}" \
        registry:2
fi
