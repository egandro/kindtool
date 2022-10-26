#!/bin/bash

echo "installing ingress..."

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}

# https://kind.sigs.k8s.io/docs/user/ingress/
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml