## variables
APT_KEY=https://packages-dev.xcyber360.com/key/GPG-KEY-XCYBER360
GPG_SIGN="gpgcheck=1\ngpgkey=${APT_KEY}]"
REPOSITORY="[xcyber360]\n${GPG_SIGN}\nenabled=1\nname=EL-\$releasever - Xcyber360\nbaseurl=https://packages-dev.xcyber360.com/pre-release/yum/\nprotect=1"
XCYBER360_TAG=$(curl --silent https://api.github.com/repos/xcyber360/xcyber360/git/refs/tags | grep '["]ref["]:' | sed -E 's/.*\"([^\"]+)\".*/\1/'  | cut -c 11- | grep ^v${XCYBER360_VERSION}$)

## check tag to use the correct repository
if [[ -n "${XCYBER360_TAG}" ]]; then
  APT_KEY=https://packages.xcyber360.com/key/GPG-KEY-XCYBER360
  GPG_SIGN="gpgcheck=1\ngpgkey=${APT_KEY}]"
  REPOSITORY="[xcyber360]\n${GPG_SIGN}\nenabled=1\nname=EL-\$releasever - Xcyber360\nbaseurl=https://packages.xcyber360.com/4.x/yum/\nprotect=1"
fi

rpm --import "${APT_KEY}"
echo -e "${REPOSITORY}" | tee /etc/yum.repos.d/xcyber360.repo