FROM node:10

# create workspace
RUN mkdir -p /home/node/app/

# set working dir:
WORKDIR /home/node/app

# load configs:
COPY ${PWD}/package.json /home/node/app/

# install packages:
RUN npm install
# install ionic cli:
RUN npm install -g @ionic/cli 
# rebuild saas:
RUN npm rebuild node-sass
# install angular cli:
RUN npm install -g @angular/cli

# expose port:
EXPOSE 8100