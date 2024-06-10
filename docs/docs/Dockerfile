#
# Start from Node
#
FROM node:14.4

#
# Install CODEDOC CLI (https://codedoc.cc/docs/cli)
#
RUN npm install -g @codedoc/cli

#
# Create the main Docs folder
#
# This folder should be mounted with the root repo folder,
# but do not forget to exclude `.codedoc/node_modules` from that volume!
# 
RUN mkdir -p /home/docs
WORKDIR /home/docs

#
# Install and serve locally
#
CMD codedoc install && codedoc serve