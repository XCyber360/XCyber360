# Xcyber360 containers for Docker

[![Slack](https://img.shields.io/badge/slack-join-blue.svg)](https://xcyber360.com/community/join-us-on-slack/)
[![Email](https://img.shields.io/badge/email-join-blue.svg)](https://groups.google.com/forum/#!forum/xcyber360)
[![Documentation](https://img.shields.io/badge/docs-view-green.svg)](https://documentation.xcyber360.com)
[![Documentation](https://img.shields.io/badge/web-view-green.svg)](https://xcyber360.com)

In this repository you will find the containers to run:

* Xcyber360 manager: it runs the Xcyber360 manager, Xcyber360 API and Filebeat OSS
* Xcyber360 dashboard: provides a web user interface to browse through alert data and allows you to visualize the agents configuration and status.
* Xcyber360 indexer: Xcyber360 indexer container (working as a single-node cluster or as a multi-node cluster). **Be aware to increase the `vm.max_map_count` setting, as it's detailed in the [Xcyber360 documentation](https://documentation.xcyber360.com/current/docker/xcyber360-container.html#increase-max-map-count-on-your-host-linux).**

The folder `build-docker-images` contains a README explaining how to build the Xcyber360 images and the necessary assets.
The folder `indexer-certs-creator` contains a README explaining how to create the certificates creator tool and the necessary assets.
The folder `single-node` contains a README explaining how to run a Xcyber360 environment with one Xcyber360 manager, one Xcyber360 indexer, and one Xcyber360 dashboard.
The folder `multi-node` contains a README explaining how to run a Xcyber360 environment with two Xcyber360 managers, three Xcyber360 indexers, and one Xcyber360 dashboard.

## Documentation

* [Xcyber360 full documentation](http://documentation.xcyber360.com)
* [Xcyber360 documentation for Docker](https://documentation.xcyber360.com/current/docker/index.html)
* [Docker Hub](https://hub.docker.com/u/xcyber360)


### Setup SSL certificate

Before starting the environment it is required to provide an SSL certificate (or just generate one self-signed).

Documentation on how to provide these two can be found at [Xcyber360 Docker Documentation](https://documentation.xcyber360.com/current/docker/xcyber360-container.html#production-deployment).


## Environment Variables

Default values are included when available.

### Xcyber360
```
API_USERNAME="xcyber360-wui"                            # Xcyber360 API username
API_PASSWORD="MyS3cr37P450r.*-"                     # Xcyber360 API password - Must comply with requirements
                                                    # (8+ length, uppercase, lowercase, special chars)

INDEXER_URL=https://xcyber360.indexer:9200              # Xcyber360 indexer URL
INDEXER_USERNAME=admin                              # Xcyber360 indexer Username
INDEXER_PASSWORD=SecretPassword                     # Xcyber360 indexer Password
FILEBEAT_SSL_VERIFICATION_MODE=full                 # Filebeat SSL Verification mode (full or none)
SSL_CERTIFICATE_AUTHORITIES=""                      # Path of Filebeat SSL CA
SSL_CERTIFICATE=""                                  # Path of Filebeat SSL Certificate
SSL_KEY=""                                          # Path of Filebeat SSL Key
```

### Dashboard
```
PATTERN="xcyber360-alerts-*"        # Default index pattern to use

CHECKS_PATTERN=true             # Defines which checks must be considered by the healthcheck
CHECKS_TEMPLATE=true            # step once the Xcyber360 app starts. Values must be true or false
CHECKS_API=true
CHECKS_SETUP=true

APP_TIMEOUT=20000               # Defines maximum timeout to be used on the Xcyber360 app requests

API_SELECTOR=true               Defines if the user is allowed to change the selected API directly from the Xcyber360 app top menu
IP_SELECTOR=true                # Defines if the user is allowed to change the selected index pattern directly from the Xcyber360 app top menu
IP_IGNORE="[]"                  # List of index patterns to be ignored

DASHBOARD_USERNAME=kibanaserver     # Custom user saved in the dashboard keystore
DASHBOARD_PASSWORD=kibanaserver     # Custom password saved in the dashboard keystore
XCYBER360_MONITORING_ENABLED=true       # Custom settings to enable/disable xcyber360-monitoring indices
XCYBER360_MONITORING_FREQUENCY=900      # Custom setting to set the frequency for xcyber360-monitoring indices cron task
XCYBER360_MONITORING_SHARDS=2           # Configure xcyber360-monitoring-* indices shards and replicas
XCYBER360_MONITORING_REPLICAS=0         ##
```

## Directory structure

    ├── build-docker-images
    │   ├── build-images.sh
    │   ├── build-images.yml
    │   ├── README.md
    │   ├── xcyber360-dashboard
    │   │   ├── config
    │   │   │   ├── config.sh
    │   │   │   ├── config.yml
    │   │   │   ├── dl_base.sh
    │   │   │   ├── entrypoint.sh
    │   │   │   ├── install_xcyber360_app.sh
    │   │   │   ├── opensearch_dashboards.yml
    │   │   │   ├── xcyber360_app_config.sh
    │   │   │   └── xcyber360.yml
    │   │   └── Dockerfile
    │   ├── xcyber360-indexer
    │   │   ├── config
    │   │   │   ├── action_groups.yml
    │   │   │   ├── config.sh
    │   │   │   ├── config.yml
    │   │   │   ├── entrypoint.sh
    │   │   │   ├── internal_users.yml
    │   │   │   ├── opensearch.yml
    │   │   │   ├── roles_mapping.yml
    │   │   │   ├── roles.yml
    │   │   │   └── securityadmin.sh
    │   │   └── Dockerfile
    │   └── xcyber360-manager
    │       ├── config
    │       │   ├── check_repository.sh
    │       │   ├── create_user.py
    │       │   ├── etc
    │       │   │   ├── cont-init.d
    │       │   │   │   ├── 0-xcyber360-init
    │       │   │   │   ├── 1-config-filebeat
    │       │   │   │   └── 2-manager
    │       │   │   └── services.d
    │       │   │       ├── filebeat
    │       │   │       │   ├── finish
    │       │   │       │   └── run
    │       │   │       └── ossec-logs
    │       │   │           └── run
    │       │   ├── filebeat_module.sh
    │       │   ├── filebeat.yml
    │       │   ├── permanent_data.env
    │       │   └── permanent_data.sh
    │       └── Dockerfile
    ├── CHANGELOG.md
    ├── indexer-certs-creator
    │   ├── config
    │   │   └── entrypoint.sh
    │   ├── Dockerfile
    │   └── README.md
    ├── LICENSE
    ├── multi-node
    │   ├── config
    │   │   ├── certs.yml
    │   │   ├── nginx
    │   │   │   └── nginx.conf
    │   │   ├── xcyber360_cluster
    │   │   │   ├── xcyber360_manager.conf
    │   │   │   └── xcyber360_worker.conf
    │   │   ├── xcyber360_dashboard
    │   │   │   ├── opensearch_dashboards.yml
    │   │   │   └── xcyber360.yml
    │   │   └── xcyber360_indexer
    │   │       ├── internal_users.yml
    │   │       ├── xcyber3601.indexer.yml
    │   │       ├── xcyber3602.indexer.yml
    │   │       └── xcyber3603.indexer.yml
    │   ├── docker-compose.yml
    │   ├── generate-indexer-certs.yml
    │   ├── Migration-to-Xcyber360-4.4.md
    │   ├── README.md
    │   └── volume-migrator.sh
    ├── README.md
    ├── SECURITY.md
    ├── single-node
    │   ├── config
    │   │   ├── certs.yml
    │   │   ├── xcyber360_cluster
    │   │   │   └── xcyber360_manager.conf
    │   │   ├── xcyber360_dashboard
    │   │   │   ├── opensearch_dashboards.yml
    │   │   │   └── xcyber360.yml
    │   │   └── xcyber360_indexer
    │   │       ├── internal_users.yml
    │   │       └── xcyber360.indexer.yml
    │   ├── docker-compose.yml
    │   ├── generate-indexer-certs.yml
    │   └── README.md
    └── VERSION


## Branches

* `master` branch contains the latest code, be aware of possible bugs on this branch.
* `stable` branch corresponds to the last Xcyber360 stable version.

## Compatibility Matrix

| Xcyber360 version | ODFE    | XPACK  |
|---------------|---------|--------|
| v5.0.0        |         |        |
| v4.10.2       |         |        |
| v4.10.1       |         |        |
| v4.10.0       |         |        |
| v4.9.2        |         |        |
| v4.9.1        |         |        |
| v4.9.0        |         |        |
| v4.8.2        |         |        |
| v4.8.1        |         |        |
| v4.8.0        |         |        |
| v4.7.5        |         |        |
| v4.7.4        |         |        |
| v4.7.3        |         |        |
| v4.7.2        |         |        |
| v4.7.1        |         |        |
| v4.7.0        |         |        |
| v4.6.0        |         |        |
| v4.5.4        |         |        |
| v4.5.3        |         |        |
| v4.5.2        |         |        |
| v4.5.1        |         |        |
| v4.5.0        |         |        |
| v4.4.5        |         |        |
| v4.4.4        |         |        |
| v4.4.3        |         |        |
| v4.4.2        |         |        |
| v4.4.1        |         |        |
| v4.4.0        |         |        |
| v4.3.11       |         |        |
| v4.3.10       |         |        |
| v4.3.9        |         |        |
| v4.3.8        |         |        |
| v4.3.7        |         |        |
| v4.3.6        |         |        |
| v4.3.5        |         |        |
| v4.3.4        |         |        |
| v4.3.3        |         |        |
| v4.3.2        |         |        |
| v4.3.1        |         |        |
| v4.3.0        |         |        |
| v4.2.7        | 1.13.2  | 7.11.2 |
| v4.2.6        | 1.13.2  | 7.11.2 |
| v4.2.5        | 1.13.2  | 7.11.2 |
| v4.2.4        | 1.13.2  | 7.11.2 |
| v4.2.3        | 1.13.2  | 7.11.2 |
| v4.2.2        | 1.13.2  | 7.11.2 |
| v4.2.1        | 1.13.2  | 7.11.2 |
| v4.2.0        | 1.13.2  | 7.10.2 |
| v4.1.5        | 1.13.2  | 7.10.2 |
| v4.1.4        | 1.12.0  | 7.10.2 |
| v4.1.3        | 1.12.0  | 7.10.2 |
| v4.1.2        | 1.12.0  | 7.10.2 |
| v4.1.1        | 1.12.0  | 7.10.2 |
| v4.1.0        | 1.12.0  | 7.10.2 |
| v4.0.4        | 1.11.0  |        |
| v4.0.3        | 1.11.0  |        |
| v4.0.2        | 1.11.0  |        |
| v4.0.1        | 1.11.0  |        |
| v4.0.0        | 1.10.1  |        |

## Credits and Thank you

These Docker containers are based on:

*  "deviantony" dockerfiles which can be found at [https://github.com/deviantony/docker-elk](https://github.com/deviantony/docker-elk)
*  "xetus-oss" dockerfiles, which can be found at [https://github.com/xetus-oss/docker-ossec-server](https://github.com/xetus-oss/docker-ossec-server)

We thank them and everyone else who has contributed to this project.

## License and copyright

Xcyber360 Docker Copyright (C) 2017, Xcyber360 Inc. (License GPLv2)

## Web references

[Xcyber360 website](http://xcyber360.com)
