# FROM python:3.9
# FROM mundialis/esa-snap:latest
FROM python:3.9
COPY main.py .
#COPY test.py .
COPY requirements.txt .
RUN mkdir /assets
RUN mkdir /data
RUN mkdir /util
COPY assets /assets
COPY util /util
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
# RUN pip3 install -r requirements.txt
#ARG DHUB_VERSION=0.6.1
#RUN wget https://github.com/scc-digitalhub/digitalhub-sdk/archive/refs/tags/$DHUB_VERSION.zip
#RUN unzip $DHUB_VERSION.zip
#RUN mv digitalhub-sdk-$DHUB_VERSION digitalhub-sdk
# Install digitalhub-core, dbt
#RUN python -m pip install ./digitalhub-sdk/core
RUN python -m pip install digitalhub==0.8.0b3
# Cleanup
#RUN rm -rf digitalhub-sdk $DHUB_VERSION.zip
RUN mkdir /files
RUN mkdir /files/preprocess
RUN apt-get update
RUN apt-get install libgfortran5
# download snap installer version 9.0
RUN wget https://download.esa.int/step/snap/9.0/installers/esa-snap_sentinel_unix_9_0_0.sh
#change file execution rights for snap installer
RUN chmod +x esa-snap_sentinel_unix_9_0_0.sh
# install snap with gpt
RUN ./esa-snap_sentinel_unix_9_0_0.sh -q
# link gpt so it can be used systemwide
RUN ln -s /usr/local/snap/bin/gpt /usr/bin/gpt
RUN snap --nosplash --nogui --modules --update-all 2>&1 | while read -r line; do echo "$line"; [ "$line" = "updates=0" ] && sleep 2 && pkill -TERM -f "snap/jre/bin/java"; done; exit 0
RUN sed -i 's/https:\/\/download.esa.int\/step\/auxdata\/dem\/SRTM90\/tiff\//https:\/\/step.esa.int\/auxdata\/dem\/SRTM90\/tiff\//g' /usr/local/snap/etc/snap.auxdata.properties
RUN useradd -u 8877 nonroot
# RUN groupadd -g 8877 workgroup 
RUN chown -R 8877:8877 /data
RUN chown -R 8877:8877 /files
USER 8877
ENTRYPOINT [ "python","main.py" ]
