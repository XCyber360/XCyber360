#!/bin/bash

# idp container launches and docker-compose returns too quickly, do not wait
# for container to be healthy as it has no dependencies, so we wait before
# continuing
sleep 7

indexer="$1-os1-1"
dashboard="$1-osd-1"

# Setup keycloack to be used with xcyber360-dashboards

# Connection
U="admin"
P="admin"
B="http://idp:8080"

# Realm
REALM="master"

# Get ACCESS_TOKEN from default install
ACCESS_TOKEN=$(curl -sS \
  -d 'client_id=admin-cli' \
  -d 'username=admin' \
  -d 'password=admin' \
  -d 'grant_type=password' \
  "${B}/realms/master/protocol/openid-connect/token" | jq -r '.access_token')

H=('-H' 'Content-Type: application/json' '-H' "Authorization: Bearer $ACCESS_TOKEN")

# Create new REALM
REALM="xcyber360"
P='{
  "id": "xcyber360",
  "realm": "xcyber360",
  "enabled": true
}'

curl -sS -L -X POST "${B}/admin/realms" "${H[@]}" -d "$P" | grep -v "Conflict detected"

# Add admin certificates to keycloak as these are used by indexer to sign saml
# messages. These should be uploaded to keycloak if we want it to verify indexer
# messages.
key=$(cat /certs/wi/admin-key.pem | grep -v "PRIVATE KEY" | tr -d "\n")
cert=$(cat /certs/wi/admin.pem | grep -v CERTIFICATE | tr -d "\n")

# Create client
# By default the client does not verify the client signature on saml messages
# but it could be enabled for testing purposes
PC="{
  \"protocol\": \"saml\",
  \"name\": \"xcyber360\",
  \"clientId\": \"xcyber360\",
  \"description\": \"xcyber360 saml integration\",
  \"baseUrl\": \"https://localhost:5601\",
  \"rootUrl\": \"https://localhost:5601\",
  \"redirectUris\": [\"https://localhost:5601/*\"],
  \"attributes\" : {
    \"saml_single_logout_service_url_redirect\": \"https://localhost:5601/_opendistro/_security/saml/logout\",
    \"saml_assertion_consumer_url_post\": \"https://localhost:5601/_opendistro/_security/saml/acs/idpinitiated\",
    \"saml_single_logout_service_url_post\": \"https://xcyber360.dashboard:5601/_opendistro/_security/saml/logout\",
    \"saml.force.post.binding\": \"false\",
    \"saml.signing.certificate\": \"$cert\",
    \"saml.signing.private.key\": \"$key\",
    \"saml.client.signature\": \"true\",
    \"saml_single_logout_service_url_redirect\": \"https://localhost:5601\",
    \"post.logout.redirect.uris\": \"https://localhost:5601*\"
  }
}"

curl -sS -L -X POST "${B}/admin/realms/${REALM}/clients" "${H[@]}" -d "$PC" | grep -v "Client xcyber360 already exists"

# Get a client json representation
CLIENT=$(curl -sS -L -X GET "${B}/admin/realms/${REALM}/clients" "${H[@]}" -G -d 'clientId=xcyber360' | jq '.[] | select(.clientId=="xcyber360")')

# Get client id
CID=$(echo $CLIENT | jq -r '.id')

# Generate all-access and admin role for the realm
PR1='{
  "name":"all-access"
}'

curl -sS -L -X POST "${B}/admin/realms/${REALM}/roles" "${H[@]}" -d "$PR1" | grep -v "Role with name all-access already exists"

PR2='{
  "name":"admin"
}'

curl -sS -L -X POST "${B}/admin/realms/${REALM}/roles" "${H[@]}" -d "$PR2" | grep -v "Role with name admin already exists"

## create new user
PU='{
  "username": "xcyber360",
  "email": "hello@xcyber360.com",
  "firstName": "Xcyber360",
  "lastName": "Xcyber360",
  "emailVerified": true,
  "enabled": true,
  "credentials": [{"temporary":false,"type":"password","value":"xcyber360"}],
  "realmRoles": ["admin", "all-access"]
}'

curl -sS -L -X POST "${B}/admin/realms/${REALM}/users" "${H[@]}" -d "$PU" | grep -v "User exists with same username"

## Get a user json representation
USER=$(curl -sS -L -X GET "${B}/admin/realms/${REALM}/users" "${H[@]}" -G -d 'username=xcyber360' | jq '.[] | select(.username=="xcyber360")')

### Get user id
USERID=$(echo $USER | jq -r '.id')

# Get roles
ROLES=$(curl -sS -L -X GET "${B}/admin/realms/${REALM}/roles" "${H[@]}" -d "$PR2")

## Assign role
ADMINID=$(echo $ROLES | jq -r '.[] | select(.name=="admin").id')
ALLACCESSID=$(echo $ROLES | jq -r '.[] | select(.name=="all-access").id')

PA1="[
  {
    \"id\": \"$ADMINID\",
    \"name\": \"admin\",
    \"composite\": false,
    \"clientRole\": false,
    \"containerId\": \"xcyber360\"
  },
    {
    \"id\": \"$ALLACCESSID\",
    \"name\": \"all-access\",
    \"description\": \"\",
    \"composite\": false,
    \"clientRole\": false,
    \"containerId\": \"xcyber360\"
  }
]"

curl -sS -L -X POST "${B}/admin/realms/${REALM}/users/${USERID}/role-mappings/realm" "${H[@]}" -d "$PA1"

# Get list of client scopes
CSCOPES=$(curl -sS -L -X GET "${B}/admin/realms/${REALM}/client-scopes" "${H[@]}")
CSID=$(echo $CSCOPES | jq -r '.[] | select(.name=="role_list").id ')
CSR=$(echo $CSCOPES | jq -r '.[] | select(.name=="role_list") ')

# Set single to true, so opensearch works
UPDATE=$(echo $CSR | jq '.protocolMappers[] | select(.name=="role list").config.single |= "true"  ')
PMID=$(echo $CSR | jq -r '.protocolMappers[] | select(.name=="role list").id')

curl -sS -L -X PUT "${B}/admin/realms/${REALM}/client-scopes/$CSID/protocol-mappers/models/$PMID" "${H[@]}" -d "$UPDATE"

# Set up auth realm on opensearch
certs="/usr/share/opensearch/config/certs"
ca="$certs/ca.pem"
cert="$certs/admin.pem"
key="$certs/admin-key.pem"

securityadmin="bash /usr/share/opensearch/plugins/opensearch-security/tools/securityadmin.sh"
config_path="/usr/share/opensearch/config/opensearch-security"

echo "To update configuration in indexer, you can run:"
echo docker exec -e JAVA_HOME=/usr/share/opensearch/jdk $indexer $securityadmin -cacert $ca -cert $cert -key $key -cd $config_path
