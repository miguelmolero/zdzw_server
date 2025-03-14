FROM nodered/node-red

COPY ./node-red/ /data

# install BAPI dependencies and tools
#RUN npm install node-rfc

# RUN npm install -g node-red-contrib-saprfc

