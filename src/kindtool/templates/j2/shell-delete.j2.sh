#!/bin/bash

NAME="{{shell_podname}}"
NAMESPACE="{{shell_namespace}}"

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}

kubectl --namespace ${NAMESPACE} \
    delete pod \
    ${NAME}