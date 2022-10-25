#!/bin/bash

get_latest_release() {
  curl --silent "https://api.github.com/repos/$1/releases/latest" | # Get latest release from GitHub api
    grep '"tag_name":' |                                            # Get tag line
    sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
}
KIND_LATEST=$(get_latest_release kubernetes-sigs/kind)
ARCH=$(dpkg --print-architecture 2>/dev/null || echo "amd64")

curl -Lo ./kind https://kind.sigs.k8s.io/dl/${KIND_LATEST}/kind-linux-${ARCH}
chmod +x ./kind
mv ./kind /usr/local/bin/kind