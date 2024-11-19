# Xcyber360 in ODFE Stack

On this folder we can find two types of environments:

 * release environment, managed by the `rel.sh` script.
 <!-- * prerelease environment managed by the `pre.sh` script. -->

##  UI Credentials

The default user and password to access the UI at https://0.0.0.0:5601/ are:

```
admin:SecretPassword
```

## Release environment

This environment brings up a complete ODFE environment with:
 - ODFE cluster with a single node
 - ODFE Kibana with a single node
 - Xcyber360 manager

The environment expect the network `mon` to exists, either bring up the
`mon` stack or execute the following command:

```bash
docker network create mon
```

This needs to be done just once.

### Usage:

```bash
./rel.sh opendistro_version xcyber360_manager_version action [saml]

where
  opendistro_version is one of  1.13.2
  xcyber360_manager_version if one of  4.3.0 4.3.1 4.3.2 4.3.3 4.3.4 4.3.5 4.3.6 4.3.7 4.3.8
  action is one of up | down | stop
optionally add 'saml' as the last parameter to deploy a saml enabled environment
```

The version lists are defined in the `rel.sh` script. Edit it to add new
supported versions.

### SAML identity provider


This environments includes SAML as an IdP (identity provider) which use is optional.
To bring up the environment with SAML, add the `idp` hostname to your `/etc/hosts/`.

```apacheconf
127.0.0.1       localhost
127.0.1.1       ...
127.0.1.1       idp

...
```

Then simply run the script with the `saml` flag, as follows:

```bash
./rel.sh 1.13.2 4.3.8 saml up
```
####  IdP credentials

The default user and password to access the UI via Keycloak are:

```
xcyber360:xcyber360
```

### Install a compatible Xcyber360 app

When the `rel.sh` script ends, it will print the commands how to install the 
Xcyber360 app in Kibana:

For example, the command

```bash
./rel.sh 1.13.2 4.3.8 up
```

Will print:

```bash
Install Xcyber360 4.3.8 into ODFE 1.13.2 manually with:

1. Install the Xcyber360 app for Kibana
docker exec -ti  odfe-rel-l-1132-kibana-1 /usr/share/kibana/bin/kibana-plugin install https://packages.xcyber360.com/4.x/ui/kibana/xcyber360_kibana-4.3.8_7.10.2-1.zip

2. Restart Kibana
docker restart odfe-rel-l-1132-kibana-1

3. Configure Kibana
docker cp ./config/kibana/xcyber360.yml odfe-rel-l-1132-kibana-1:/usr/share/kibana/data/xcyber360/config/

4. Open Kibana in a browser:
https://localhost:5601
```

This is a manual procedure which might be automated in the future. Any 
automatism will need:

1. Wait for Kibana to be ready.

2. Execute the Xcyber360 plugin installation command:

```bash
docker exec -ti  odfe-rel-l-1132-kibana-1 /usr/share/kibana/bin/kibana-plugin install https://packages.xcyber360.com/4.x/ui/kibana/xcyber360_kibana-4.3.8_7.10.2-1.zip
```

3. Restart the Kibana container to enable Xcyber360:

```bash
docker restart odfe-rel-l-1132-kibana-1
```

4. Wait for Kibana to be ready.
5. Copy the configuration file to kibana so xcyber360 is set up correctly:

```bash
docker cp ./config/kibana/xcyber360.yml odfe-rel-l-1132-kibana-1:/usr/share/kibana/data/xcyber360/config/
```

If this command returns a `no such file or directory` message, means Kibana is 
still initializing the plugin, try again a couple of seconds later, depending 
on your computer.

### Registering agents using Docker

To register an agent, we need to get the registering command from the UI and 
run commands like the ones below. Please pay atention to the Xcyber360 version in 
the network name.

These images will run in the background and a `docker logs` command will show 
the agent `ossec.log` file.

- For `CentOS/8` images:
  ```bash
  docker run --name odfe-rel-1132-agent --network odfe-rel-1132 --label com.docker.compose.project=odfe-rel-1132 -d centos:8 bash -c '
      sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-*
      sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-*

      # Change this command by the one the UI suggest to use add it the -y and remove the sudo
      XCYBER360_MANAGER='xcyber360.manager' yum install -y https://packages.xcyber360.com/4.x/yum5/x86_64/xcyber360-agent-4.3.8-1.el5.x86_64.rpm

      /etc/init.d/xcyber360-agent start
      tail -f /var/ossec/logs/ossec.log
  '
  ```

- For `Ubuntu` images
  ```bash
  docker run --name odfe-rel-1132-agent --network odfe-rel-1132 --label com.docker.compose.project=odfe-rel-1132 -d ubuntu:20.04 bash -c '
    apt update -y
    apt install -y curl lsb-release
    curl -so \xcyber360-agent-4.3.8.deb \
      https://packages.xcyber360.com/4.x/apt/pool/main/w/xcyber360-agent/xcyber360-agent_4.3.8-1_amd64.deb \
      && XCYBER360_MANAGER='xcyber360.manager' XCYBER360_AGENT_GROUP='default' dpkg -i ./xcyber360-agent-4.3.8.deb

    /etc/init.d/xcyber360-agent start
    tail -f /var/ossec/logs/ossec.log
  '
  ```

- For `non-Linux` agents:
  
  We need to provision virtual machines.
