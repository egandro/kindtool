#!/bin/bash

TOKEN_FILE="{{config_dir}}/token"
DASHBOARD_VERSION="{{dashboard_version}}"

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}

run_dashboard() {
    echo "Dashboard is running"
    echo ""
    echo "Dashboard URL: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/"
    echo ""
    echo "Token:"
    cat ${TOKEN_FILE}
    echo ""
    echo ""
    echo "run command: "'KUBECONFIG=$(kindtool get kubeconfig)'" kubectl proxy"
    echo ""
}

if [[ -f "${TOKEN_FILE}" ]]; then
    run_dashboard
    exit 0
fi

# https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
# https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/


echo "creating namespace.."

kubectl create namespace kubernetes-dashboard

echo "installing access-control.."

kubectl apply -f {{config_dir}}/dashboard-admin-user.yaml

echo "waiting for kubernetes-dashboard serviceaccounts/admin-user"
while true; do
    kubectl -n kubernetes-dashboard get serviceaccounts/admin-user 2>/dev/null && break
    sleep 1
done

kubectl apply -f {{config_dir}}/dashboard-cluster-admin.yaml

echo "waiting for kubernetes-dashboard cluster binding cluster-admin"
while true; do
    JSON='KIND:kind,NAMESPACE:metadata.namespace,NAME:metadata.name,SERVICE_ACCOUNTS:subjects[?(@.kind=="ServiceAccount")].name'
    kubectl get rolebindings,clusterrolebindings \
    -n=kubernetes-dashboard  \
    -o custom-columns=${JSON} 2>/dev/null | grep -o "cluster-admin" >/dev/null && break
        sleep 1
done

echo "creating token for admin-user"
kubectl -n kubernetes-dashboard create token admin-user > ${TOKEN_FILE}

echo "installing dashboard..."

# https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v${DASHBOARD_VERSION}/aio/deploy/recommended.yaml

echo "waiting for pod kubernetes-dashboard to become ready"
kubectl --namespace=kubernetes-dashboard \
        rollout status deployment kubernetes-dashboard

run_dashboard