# Xcyber360 Docker Copyright (C) 2017, Xcyber360 Inc. (License GPLv2)
FROM amazonlinux:2023 AS builder

ARG XCYBER360_VERSION
ARG XCYBER360_TAG_REVISION

RUN yum install curl-minimal openssl xz tar findutils shadow-utils -y

COPY config/check_repository.sh /
RUN chmod 775 /check_repository.sh && \
    source /check_repository.sh

RUN yum install xcyber360-indexer-${XCYBER360_VERSION}-${XCYBER360_TAG_REVISION} -y && \
    yum clean all

COPY config/opensearch.yml /

COPY config/config.sh .

COPY config/config.yml /

RUN bash config.sh

################################################################################
# Build stage 1 (the actual Xcyber360 indexer image):
#
# Copy xcyber360-indexer from stage 0
# Add entrypoint

################################################################################
FROM amazonlinux:2023

ENV USER="xcyber360-indexer" \
    GROUP="xcyber360-indexer" \
    NAME="xcyber360-indexer" \
    INSTALL_DIR="/usr/share/xcyber360-indexer"

# Set $JAVA_HOME
RUN echo "export JAVA_HOME=$INSTALL_DIR/jdk" >> /etc/profile.d/java_home.sh && \
    echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> /etc/profile.d/java_home.sh
ENV JAVA_HOME="$INSTALL_DIR/jdk"
ENV PATH=$PATH:$JAVA_HOME/bin:$INSTALL_DIR/bin

# Add k-NN lib directory to library loading path variable
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$INSTALL_DIR/plugins/opensearch-knn/lib"

RUN yum install curl-minimal shadow-utils findutils hostname -y

RUN getent group $GROUP || groupadd -r -g 1000 $GROUP

RUN useradd --system \
            --uid 1000 \
            --no-create-home \
            --home-dir $INSTALL_DIR \
            --gid $GROUP \
            --shell /sbin/nologin \
            --comment "$USER user" \
            $USER

WORKDIR $INSTALL_DIR

COPY config/entrypoint.sh /

COPY config/securityadmin.sh /

RUN chmod 700 /entrypoint.sh && chmod 700 /securityadmin.sh

RUN chown 1000:1000 /*.sh

COPY --from=builder --chown=1000:1000 /usr/share/xcyber360-indexer /usr/share/xcyber360-indexer
COPY --from=builder --chown=1000:1000 /etc/xcyber360-indexer /usr/share/xcyber360-indexer
COPY --from=builder --chown=0:0 /debian/xcyber360-indexer/usr/lib/systemd /usr/lib/systemd
COPY --from=builder --chown=0:0 /debian/xcyber360-indexer/usr/lib/sysctl.d /usr/lib/sysctl.d
COPY --from=builder --chown=0:0 /debian/xcyber360-indexer/usr/lib/tmpfiles.d /usr/lib/tmpfiles.d

RUN chown -R 1000:1000 /usr/share/xcyber360-indexer

RUN mkdir -p /var/lib/xcyber360-indexer && chown 1000:1000 /var/lib/xcyber360-indexer && \
    mkdir -p /usr/share/xcyber360-indexer/logs && chown 1000:1000 /usr/share/xcyber360-indexer/logs && \
    mkdir -p /run/xcyber360-indexer && chown 1000:1000 /run/xcyber360-indexer && \
    mkdir -p /var/log/xcyber360-indexer && chown 1000:1000 /var/log/xcyber360-indexer && \
    chmod 700 /usr/share/xcyber360-indexer && \
    chmod 600 /usr/share/xcyber360-indexer/jvm.options && \
    chmod 600 /usr/share/xcyber360-indexer/opensearch.yml

USER xcyber360-indexer

# Services ports
EXPOSE 9200

ENTRYPOINT ["/entrypoint.sh"]
# Dummy overridable parameter parsed by entrypoint
CMD ["opensearchwrapper"]