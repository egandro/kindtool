#!/bin/bash

echo "installing loadbalance..."

# https://kind.sigs.k8s.io/docs/user/loadbalancer/
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/config/manifests/metallb-native.yaml
