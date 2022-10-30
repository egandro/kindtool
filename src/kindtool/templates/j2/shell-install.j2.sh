#!/bin/bash

NAME="{{shell_podname}}"
NAMESPACE="{{shell_namespace}}"
IMAGE="{{shell_image}}"
COMMAND="{{shell_command}}"

# idea from here: https://github.com/lensapp/lens/blob/487079b61fe3b8264388b43150bd6d67f86d541d/src/main/shell-session/node-shell-session/node-shell-session.ts#L87
if [[ -z ${COMMAND} ]]; then
    COMMAND="sh"
    _ARG1="-c"
    _ARG2="((clear && bash) || (clear && ash) || (clear && sh))"
fi

{% if local_kubeconfig -%}
export KUBECONFIG={{config_dir}}/config
{% endif -%}

COMMAND=/bin/bash
IS_RUNNING=$(kubectl --namespace ${NAMESPACE} \
    get pod
    ${NAME} 2>/dev/null)

if [[ ! -z ${IS_RUNNING} ]]; then
    echo "attaching to ${NAME}..."
    kubectl --namespace ${NAMESPACE} \
        exec  \
        --stdin --tty \
        ${NAME} \
        -- "${COMMAND}" "${_ARG1}" "${_ARG2}"
else
    echo "spawing ${NAME}..."
    kubectl --namespace ${NAMESPACE} \
        run \
        --stdin --tty \
        ${NAME} \
        --image=${IMAGE} \
        --command -- "${COMMAND}" "${_ARG1}" "${_ARG2}"
fi
