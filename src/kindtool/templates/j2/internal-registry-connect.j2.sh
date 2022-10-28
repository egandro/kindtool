#!/bin/bash

# https://kind.sigs.k8s.io/docs/user/local-registry/

REGISTRY_NAME="{{internal_registry_docker_name}}"
CLUSTER_NAME="{{cluster_name}}"

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}


echo "connecting cluster '${CLUSTER_NAME}' to internal docker registry '${REGISTRY_NAME}'"

# connect the registry to the cluster network if not already connected
if [ "$(docker inspect -f="{"{"json .NetworkSettings.Networks.${CLUSTER_NAME}"}"}" "${REGISTRY_NAME}")" = 'null' ]; then
    echo "successfully connecting cluster '${CLUSTER_NAME}' to internal docker registry '${REGISTRY_NAME}'"
    docker network connect "${CLUSTER_NAME}" "${REGISTRY_NAME}"
fi

kubectl apply -f {{config_dir}}/internal-registry.yaml

