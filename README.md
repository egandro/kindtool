# kindtool

Python program for simplyfing workflows with kind.

[kind](https://kind.sigs.k8s.io/) is a tool for running local Kubernetes clusters using Docker container “nodes”.

With [kindtool](https://github.com/egandro/kindtool/) you can add a simple `Kindfile` to your project. You can crate, destroy, start and maintain a `k8s` cluster for ci or development.


## Installation

Requirements:

- docker
- python3
- kind

### Kind installation

Official documentation: <https://kind.sigs.k8s.io/docs/user/quick-start/>

Fast lane:


```
get_latest_release() {
  curl --silent "https://api.github.com/repos/$1/releases/latest" | # Get latest release from GitHub api
    grep '"tag_name":' |                                            # Get tag line
    sed -E 's/.*"([^"]+)".*/\1/'                                    # Pluck JSON value
}
KIND_LATEST=$(get_latest_release kubernetes-sigs/kind)
ARCH=$(dpkg --print-architecture 2>/dev/null || echo "amd64")

curl -Lo ./kind https://kind.sigs.k8s.io/dl/${KIND_LATEST}/kind-linux-${ARCH}
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

### Kindtool installation

```
$ pip install git+https://github.com/egandro/kindtool.git
```

## Workflow

```
# creates a new Kindfile (edit for your needs)
$ kindtool init <projectdir>

# creates the cluster - this will create a .kind directory next to Kindfile
# warning: put `.kind` to your gitignore
$ kindtool up

# stops the kind cluster - configuration, k8s config and persistent data will be keped
$ kindtool halt

# kills the kind cluster - configuration, k8s config is removed,
# the persistent data will be keped in .kind/data
$ kindtool destroy

# kills the kind cluster  and removes the data folder
# this needs to be run as root! Docker might created files that have 0/0 uids/gids
$ sudo kindtool destroy -f

# is kind running - print status information
$ kindtool status

# returns the directory with the config files
# can be used as export KUBECONFIG=$(kindfile get kubeconfig)
$ kindtool get kubeconfig
```