FROM node:16.14.2 AS builder-kbn-8.2.3
RUN npm install --global @bazel/bazelisk@1.11.0
USER node
RUN git clone --depth 1 --branch v8.2.3 https://github.com/elastic/kibana /home/node/kbn
RUN chown node.node /home/node/kbn

WORKDIR /home/node/kbn
RUN yarn config set registry http://host.docker.internal:4873 && \
    sed -i 's/https:\/\/registry.yarnpkg.com/http:\/\/host.docker.internal:4873/g' yarn.lock && \
    yarn kbn bootstrap 
RUN rm -rf /home/node/.cache/yarn && rm -rf /home/node/.cache/Cypress && rm -rf /home/node/.cache/ms-playwright
RUN mkdir -p /home/node/kbn/data/xcyber360/config 

FROM node:16.14.2
USER node
COPY --from=builder-kbn-8.2.3 /home/node/ /home/node/
WORKDIR /home/node/kbn

