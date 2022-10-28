#!/bin/bash

CLUSTER_NAME="{{cluster_name}}"

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}

# we need to setup the lb adddreses according to our docker IPs

# https://kind.sigs.k8s.io/docs/user/loadbalancer/

# there is no network per cluster... we might want to have more Kindvariables at some point
#DOCKER_NETWORK=${CLUSTER_NAME}
DOCKER_NETWORK="kind"

ips=$(docker network inspect -f "{""{".IPAM.Config"}""}" "${DOCKER_NETWORK}")
prefix=$(echo $ips | sed -s "s|^\["{"||" | sed -s "s|\.0/16.*||")

cat {{config_dir}}/metallb-config.tpl.yaml  \
    | sed -e 's|PREFIX|'${prefix}'|g'  > {{config_dir}}/metallb-config.yaml

echo "waiting for metallb to become ready"
# 300s might be bad on a bad bad network
while true; do
    kubectl wait --namespace metallb-system \
                    --for=condition=ready pod \
                    --selector=app=metallb \
                    --timeout=300s  2>/dev/null && break
    sleep 1
done
kubectl apply -f {{config_dir}}/metallb-config.yaml

rm -f {{config_dir}}/metallb-config.yaml