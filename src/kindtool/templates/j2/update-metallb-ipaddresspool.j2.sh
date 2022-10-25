#!/bin/bash

CLUSTER_NAME="{{cluster_name}}"

# we need to setup the lb adddreses according to our docker IPs

# https://kind.sigs.k8s.io/docs/user/loadbalancer/

cat ../config/metallb-config.tpl.yaml  \
    | sed -e 's|PREFIX|'$(docker network inspect -f "\{\{.IPAM.Config\}\}" "${CLUSTER_NAME}" \
    | sed -s "s|^\[{||" | sed -s "s|\.0/16.*||")'|g'  > ../config/metallb-config.yaml

sleep 30 # hit me with a stick

kubectl wait --namespace metallb-system \
                --for=condition=ready pod \
                --selector=app=metallb \
                --timeout=300s

kubectl apply -f ../config/metallb-config.yaml

rm -f ../config/metallb-config.yaml