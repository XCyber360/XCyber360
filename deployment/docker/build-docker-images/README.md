# Xcyber360 Docker Image Builder

The creation of the images for the Xcyber360 stack deployment in Docker is done with the build-images.yml script

To execute the process, the following must be executed in the root of the xcyber360-docker repository:

```
$ deployment/docker/build-docker-images/build-images.sh
```

This script initializes the environment variables needed to build each of the images.

The script allows you to build images from other versions of Xcyber360, to do this you must use the -v or --version argument:

```
$ deployment/docker/build-docker-images/build-images.sh -v 5.0.0
```

To get all the available script options use the -h or --help option:

```
$ deployment/docker/build-docker-images/build-images.sh -h

Usage: deployment/docker/build-docker-images/build-images.sh [OPTIONS]

    -d, --dev <ref>              [Optional] Set the development stage you want to build, example rc1 or beta1, not used by default.
    -f, --filebeat-module <ref>  [Optional] Set Filebeat module version. By default 0.4.
    -r, --revision <rev>         [Optional] Package revision. By default 1
    -v, --version <ver>          [Optional] Set the Xcyber360 version should be builded. By default, 5.0.0.
    -h, --help                   Show this help.

```