# Deploy Xcyber360 Docker in single node configuration

This deployment is defined in the `docker-compose.yml` file with one Xcyber360 manager containers, one Xcyber360 indexer containers, and one Xcyber360 dashboard container. It can be deployed by following these steps: 

1) Increase max_map_count on your host (Linux). This command must be run with root permissions:
```
$ sysctl -w vm.max_map_count=262144
```
2) Run the certificate creation script:
```
$ docker-compose -f generate-certs.yml run --rm generator
```
3) Start the environment with docker-compose:

- In the foregroud:
```
$ docker-compose up
```
- In the background:
```
$ docker-compose up -d
```

The environment takes about 1 minute to get up (depending on your Docker host) for the first time since Xcyber360 Indexer must be started for the first time and the indexes and index patterns must be generated.