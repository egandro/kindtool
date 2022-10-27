#!/bin/bash

echo "installing ingress..."

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}

# https://kind.sigs.k8s.io/docs/user/ingress/
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml

# https://reuvenharrison.medium.com/how-to-wait-for-a-kubernetes-pod-to-be-ready-one-liner-144bbbb5a76f

echo "waiting for contour to become ready"
while true; do
    kubectl get pods \
            --namespace projectcontour \
            -l app=contour \
            -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}' 2>/dev/null | grep -o True >/dev/null && break
    sleep 1
done

echo "waiting for envoy to become ready"
while true; do
    kubectl get pods \
            --namespace projectcontour \
            -l app=envoy \
            -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}' 2>/dev/null | grep -o True >/dev/null && break
    sleep 1
done
