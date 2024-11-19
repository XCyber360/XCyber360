#/bin/sh

# X-Pack environment utility which:
#   - creates the "xcyber360_app" user
#   - creates the "xcyber360_indices" role
#   - maps the "xcyber360_indices" role to the "xcyber360_app" user

# Elasticsearch host
elasticsearch_admin="elastic"
elasticsearch_admin_password="SecretPassword"
elasticsearch_host="https://${1-localhost}:9200"

# User, roles and role mapping definition
xcyber360_indices_role="xcyber360_indices"
xcyber360_indices_pattern="xcyber360-*"
xcyber360_user_username="xcyber360_app"
xcyber360_user_password="xcyber360_app"
kibana_system_role="kibana_system"

exit_with_message(){
  echo $1;
  exit 1;
}

# Create "xcyber360_indices" role
echo " Creating '$xcyber360_indices_role' role..."
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -k -u $elasticsearch_admin:$elasticsearch_admin_password \
  $elasticsearch_host/_security/role/$xcyber360_indices_role -d@- << EOF || exit_with_message "Error creating $xcyber360_indices_role role"
{
  "cluster": [ "all" ],
  "indices": [
    {
      "names" : [ "$xcyber360_indices_pattern" ],
      "privileges": [ "all" ]
    }
  ]
}
EOF
echo ""

# Create "xcyber360_user" user
echo "Creating "$xcyber360_user_username" user..."
curl \
  -X POST \
  -H 'Content-Type: application/json' \
  -k -u $elasticsearch_admin:$elasticsearch_admin_password \
  $elasticsearch_host/_security/user/$xcyber360_user_username -d@- << EOF || exit_with_message "Error creating $xcyber360_user_username user"
{
  "username" : "$xcyber360_user_username",
  "password" : "$xcyber360_user_password",
  "roles" : [ "$kibana_system_role", "$xcyber360_indices_role" ],
  "full_name" : "",
  "email" : ""
}
EOF
echo ""
