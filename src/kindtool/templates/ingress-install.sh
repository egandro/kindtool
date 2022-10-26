#!/bin/bash

echo "installing ingress..."

# https://kind.sigs.k8s.io/docs/user/ingress/
kubectl apply -f https://projectcontour.io/quickstart/contour.yaml