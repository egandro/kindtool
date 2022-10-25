#!/bin/bash

# https://kind.sigs.k8s.io/docs/user/local-registry/

REGISTRY_NAME="{{internal_registry_name}}"

# connect the registry to the cluster network if not already connected
if [ "$(docker inspect -f='\{\{json .NetworkSettings.Networks.kind\}\}' "${REGISTRY_NAME}")" = 'null' ]; then
    docker network connect "kind" "${REGISTRY_NAME}"
fi

kubectl apply -f {{config_dir}}/localregistry.yaml