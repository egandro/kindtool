#!/bin/bash

TOKEN_FILE="{{config_dir}}/token"
DASHBOARD_VERSION=2.6.1

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}

if [[ -f "${TOKEN_FILE}" ]]; then
    echo "dashboard is installed"
    exit 0
fi

# https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md


echo "installing access-control.."

kubectl apply -f {{config_dir}}/dashboard-admin-user.yaml
kubectl apply -f {{config_dir}}/dashboard-cluster-admin.yaml
kubectl -n kubernetes-dashboard create token admin-user > ${TOKEN_FILE}

echo "installing dashboard..."

# https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v${DASHBOARD_VERSION}/aio/deploy/recommended.yaml
