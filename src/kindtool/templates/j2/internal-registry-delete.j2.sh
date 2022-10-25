#!/bin/bash

# https://kind.sigs.k8s.io/docs/user/local-registry/

REGISTRY_NAME="{{internal_registry_name}}"

echo "deleting internal docker registry '${REGISTRY_NAME}'"
docker rm -f "${REGISTRY_NAME}"