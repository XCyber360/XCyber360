FROM public.ecr.aws/o5x5t0j3/amd64/api_development:integration_test_xcyber360-generic

ARG XCYBER360_BRANCH

## install Xcyber360
RUN mkdir xcyber360 && curl -sL https://github.com/xcyber360/xcyber360/tarball/${XCYBER360_BRANCH} | tar zx --strip-components=1 -C xcyber360
ADD base/agent/preloaded-vars.conf /xcyber360/etc/preloaded-vars.conf
RUN /xcyber360/install.sh

COPY base/agent/entrypoint.sh /scripts/entrypoint.sh

HEALTHCHECK --retries=900 --interval=1s --timeout=40s --start-period=30s CMD /usr/bin/python3 /tmp_volume/healthcheck/healthcheck.py || exit 1
