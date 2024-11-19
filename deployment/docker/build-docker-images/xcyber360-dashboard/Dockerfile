# Xcyber360 Docker Copyright (C) 2017, Xcyber360 Inc. (License GPLv2)
FROM amazonlinux:2023 AS builder

ARG XCYBER360_VERSION
ARG XCYBER360_TAG_REVISION
ARG XCYBER360_UI_REVISION
ARG INSTALL_DIR=/usr/share/xcyber360-dashboard

# Update and install dependencies
RUN yum install curl-minimal libcap openssl -y

COPY config/check_repository.sh /
RUN chmod 775 /check_repository.sh && \
    source /check_repository.sh

RUN yum install xcyber360-dashboard-${XCYBER360_VERSION}-${XCYBER360_TAG_REVISION} -y && \
    yum clean all

# Create and set permissions to data directories
RUN mkdir -p $INSTALL_DIR/data/xcyber360 && chmod -R 775 $INSTALL_DIR/data/xcyber360
RUN mkdir -p $INSTALL_DIR/data/xcyber360/config && chmod -R 775 $INSTALL_DIR/data/xcyber360/config
RUN mkdir -p $INSTALL_DIR/data/xcyber360/logs && chmod -R 775 $INSTALL_DIR/data/xcyber360/logs
COPY config/xcyber360.yml $INSTALL_DIR/data/xcyber360/config/

# Generate certificates
COPY config/config.sh .
COPY config/config.yml /
RUN bash config.sh

################################################################################
# Build stage 1 (the current Xcyber360 dashboard image):
#
# Copy xcyber360-dashboard from stage 0
# Add entrypoint
# Add xcyber360_app_config
################################################################################
FROM amazonlinux:2023

# Set environment variables
ENV USER="xcyber360-dashboard" \
    GROUP="xcyber360-dashboard" \
    NAME="xcyber360-dashboard" \
    INSTALL_DIR="/usr/share/xcyber360-dashboard"

# Set Xcyber360 app variables
ENV PATTERN="" \
    CHECKS_PATTERN="" \
    CHECKS_TEMPLATE="" \
    CHECKS_API="" \
    CHECKS_SETUP="" \
    APP_TIMEOUT="" \
    API_SELECTOR="" \
    IP_SELECTOR="" \
    IP_IGNORE="" \
    XCYBER360_MONITORING_ENABLED="" \
    XCYBER360_MONITORING_FREQUENCY="" \
    XCYBER360_MONITORING_SHARDS="" \
    XCYBER360_MONITORING_REPLICAS=""

# Update and install dependencies
RUN yum install shadow-utils -y

# Create xcyber360-dashboard user and group
RUN getent group $GROUP || groupadd -r -g 1000 $GROUP
RUN useradd --system \
            --uid 1000 \
            --no-create-home \
            --home-dir $INSTALL_DIR \
            --gid $GROUP \
            --shell /sbin/nologin \
            --comment "$USER user" \
            $USER

# Copy and set permissions to scripts
COPY config/entrypoint.sh /
COPY config/xcyber360_app_config.sh /
RUN chmod 700 /entrypoint.sh
RUN chmod 700 /xcyber360_app_config.sh
RUN chown 1000:1000 /*.sh

# Copy Install dir from builder to current image
COPY --from=builder --chown=1000:1000 $INSTALL_DIR $INSTALL_DIR

# Create custom directory
RUN mkdir -p /usr/share/xcyber360-dashboard/plugins/xcyber360/public/assets/custom
RUN chown 1000:1000 /usr/share/xcyber360-dashboard/plugins/xcyber360/public/assets/custom

# Set $JAVA_HOME
RUN echo "export JAVA_HOME=$INSTALL_DIR/jdk" >> /etc/profile.d/java_home.sh && \
    echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> /etc/profile.d/java_home.sh
ENV JAVA_HOME=$INSTALL_DIR/jdk
ENV PATH=$PATH:$JAVA_HOME/bin:$INSTALL_DIR/bin

# Add k-NN lib directory to library loading path variable
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$INSTALL_DIR/plugins/opensearch-knn/lib"

# Set workdir and user
WORKDIR $INSTALL_DIR
USER xcyber360-dashboard

# Services ports
EXPOSE 443

ENTRYPOINT [ "/entrypoint.sh" ]

CMD ["opensearch-dashboards"]
