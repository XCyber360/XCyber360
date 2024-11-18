FROM public.ecr.aws/o5x5t0j3/amd64/api_development:integration_test_xcyber360-generic

# ENV_MODE needs to be assigned to an environment variable as it is going to be used at run time (CMD)
ARG ENV_MODE
ENV ENV_MODE ${ENV_MODE}

# INSTALL MANAGER
ARG XCYBER360_BRANCH

ADD base/manager/supervisord.conf /etc/supervisor/conf.d/

RUN mkdir xcyber360 && curl -sL https://github.com/xcyber360/xcyber360/tarball/${XCYBER360_BRANCH} | tar zx --strip-components=1 -C xcyber360
COPY base/manager/preloaded-vars.conf /xcyber360/etc/preloaded-vars.conf
RUN /xcyber360/install.sh
COPY base/manager/entrypoint.sh /scripts/entrypoint.sh

# HEALTHCHECK
HEALTHCHECK --retries=900 --interval=1s --timeout=30s --start-period=30s CMD /var/ossec/framework/python/bin/python3 /tmp_volume/healthcheck/healthcheck.py ${ENV_MODE} || exit 1
