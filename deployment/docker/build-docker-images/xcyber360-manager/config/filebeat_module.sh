## variables
REPOSITORY="packages-dev.xcyber360.com/pre-release"
XCYBER360_TAG=$(curl --silent https://api.github.com/repos/xcyber360/xcyber360/git/refs/tags | grep '["]ref["]:' | sed -E 's/.*\"([^\"]+)\".*/\1/'  | cut -c 11- | grep ^v${XCYBER360_VERSION}$)

## check tag to use the correct repository
if [[ -n "${XCYBER360_TAG}" ]]; then
  REPOSITORY="packages.xcyber360.com/4.x"
fi

curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/${FILEBEAT_CHANNEL}-${FILEBEAT_VERSION}-x86_64.rpm &&\
yum install -y ${FILEBEAT_CHANNEL}-${FILEBEAT_VERSION}-x86_64.rpm && rm -f ${FILEBEAT_CHANNEL}-${FILEBEAT_VERSION}-x86_64.rpm && \
curl -s https://${REPOSITORY}/filebeat/${XCYBER360_FILEBEAT_MODULE} | tar -xvz -C /usr/share/filebeat/module