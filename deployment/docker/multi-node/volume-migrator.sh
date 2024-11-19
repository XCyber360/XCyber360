docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=xcyber360-indexer-data-1 \
           $2_xcyber360-indexer-data-1

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=xcyber360-indexer-data-2 \
           $2_xcyber360-indexer-data-2

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=xcyber360-indexer-data-3 \
           $2_xcyber360-indexer-data-3

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master_xcyber360_api_configuration \
           $2_master_xcyber360_api_configuration

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master_xcyber360_etc \
           $2_docker_xcyber360_etc

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-xcyber360-logs \
           $2_master-xcyber360-logs

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-xcyber360-queue \
           $2_master-xcyber360-queue

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-xcyber360-var-multigroups \
           $2_master-xcyber360-var-multigroups

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-xcyber360-integrations \
           $2_master-xcyber360-integrations

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-xcyber360-active-response \
           $2_master-xcyber360-active-response

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-xcyber360-agentless \
           $2_master-xcyber360-agentless

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-xcyber360-wodles \
           $2_master-xcyber360-wodles

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-filebeat-etc \
           $2_master-filebeat-etc

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=master-filebeat-var \
           $2_master-filebeat-var

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker_xcyber360_api_configuration \
           $2_worker_xcyber360_api_configuration

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker_xcyber360_etc \
           $2_worker-xcyber360-etc

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-xcyber360-logs \
           $2_worker-xcyber360-logs

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-xcyber360-queue \
           $2_worker-xcyber360-queue

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-xcyber360-var-multigroups \
           $2_worker-xcyber360-var-multigroups

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-xcyber360-integrations \
           $2_worker-xcyber360-integrations

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-xcyber360-active-response \
           $2_worker-xcyber360-active-response

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-xcyber360-agentless \
           $2_worker-xcyber360-agentless

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-xcyber360-wodles \
           $2_worker-xcyber360-wodles

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-filebeat-etc \
           $2_worker-filebeat-etc

docker volume create \
           --label com.docker.compose.project=$2 \
           --label com.docker.compose.version=$1 \
           --label com.docker.compose.volume=worker-filebeat-var \
           $2_worker-filebeat-var

docker container run --rm -it \
           -v xcyber360-docker_worker-filebeat-var:/from \
           -v $2_worker-filebeat-var:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_elastic-data-1:/from \
           -v $2_xcyber360-indexer-data-1:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_elastic-data-2:/from \
           -v $2_xcyber360-indexer-data-2:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_elastic-data-3:/from \
           -v $2_xcyber360-indexer-data-3:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-api-configuration:/from \
           -v $2_master-xcyber360-api-configuration:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-etc:/from \
           -v $2_master-xcyber360-etc:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-logs:/from \
           -v $2_master-xcyber360-logs:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-queue:/from \
           -v $2_master-xcyber360-queue:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-var-multigroups:/from \
           -v $2_master-xcyber360-var-multigroups:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-integrations:/from \
           -v $2_master-xcyber360-integrations:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-active-response:/from \
           -v $2_master-xcyber360-active-response:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-agentless:/from \
           -v $2_master-xcyber360-agentless:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_ossec-wodles:/from \
           -v $2_master-xcyber360-wodles:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_filebeat-etc:/from \
           -v $2_master-filebeat-etc:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_filebeat-var:/from \
           -v $2_master-filebeat-var:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-api-configuration:/from \
           -v $2_worker-xcyber360-api-configuration:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-etc:/from \
           -v $2_worker-xcyber360-etc:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-logs:/from \
           -v $2_worker-xcyber360-logs:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-queue:/from \
           -v $2_worker-xcyber360-queue:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-var-multigroups:/from \
           -v $2_worker-xcyber360-var-multigroups:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-integrations:/from \
           -v $2_worker-xcyber360-integrations:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-active-response:/from \
           -v $2_worker-xcyber360-active-response:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-agentless:/from \
           -v $2_worker-xcyber360-agentless:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-ossec-wodles:/from \
           -v $2_worker-xcyber360-wodles:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-filebeat-etc:/from \
           -v $2_worker-filebeat-etc:/to \
           alpine ash -c "cd /from ; cp -avp . /to"

docker container run --rm -it \
           -v xcyber360-docker_worker-filebeat-var:/from \
           -v $2_worker-filebeat-var:/to \
           alpine ash -c "cd /from ; cp -avp . /to"
