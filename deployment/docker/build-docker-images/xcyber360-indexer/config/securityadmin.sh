# Xcyber360 Docker Copyright (C) 2017, Xcyber360 Inc. (License GPLv2)
sleep 30
bash /usr/share/xcyber360-indexer/plugins/opensearch-security/tools/securityadmin.sh -cd /usr/share/xcyber360-indexer/opensearch-security/ -nhnv -cacert  $CACERT -cert $CERT -key $KEY -p 9200 -icl