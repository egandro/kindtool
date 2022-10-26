#!/bin/bash

CLUSTER_NAME="{{cluster_name}}"

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}

# we need to setup the lb adddreses according to our docker IPs

# https://kind.sigs.k8s.io/docs/user/loadbalancer/

ips=$(docker network inspect -f \{\{.IPAM.Config\}\} "${CLUSTER_NAME}")
prefix=$(echo $ips | sed -s "s|^\["{"||" | sed -s "s|\.0/16.*||")

cat {{config_dir}}/metallb-config.tpl.yaml  \
    | sed -e 's|PREFIX|'${prefix}'|g'  > {{config_dir}}/metallb-config.yaml

sleep 30 # hit me with a stick

kubectl wait --namespace metallb-system \
                --for=condition=ready pod \
                --selector=app=metallb \
                --timeout=300s

kubectl apply -f {{config_dir}}/metallb-config.yaml

rm -f {{config_dir}}/metallb-config.yaml