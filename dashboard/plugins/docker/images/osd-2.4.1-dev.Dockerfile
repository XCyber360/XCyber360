FROM node:14.20.0 AS builder-osd-2.4.1
USER node
RUN git clone --depth 1 --branch 2.4.1 https://github.com/opensearch-project/OpenSearch-Dashboards.git /home/node/kbn
RUN chown node.node /home/node/kbn

WORKDIR /home/node/kbn
RUN yarn osd bootstrap --production

WORKDIR /home/node/kbn/plugins
RUN git clone --depth 1 --branch 2.4.1.0 https://github.com/opensearch-project/security-dashboards-plugin.git
WORKDIR /home/node/kbn/plugins/security-dashboards-plugin
RUN yarn install

RUN yarn config set registry http://host.docker.internal:4873 && \
    sed -i 's/https:\/\/registry.yarnpkg.com/http:\/\/host.docker.internal:4873/g' yarn.lock

RUN mkdir -p /home/node/kbn/data/xcyber360/config

FROM node:14.20.0
USER node
COPY --from=builder-osd-2.4.1 /home/node/kbn /home/node/kbn
WORKDIR /home/node/kbn
