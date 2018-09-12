
ARG UBUNTU_VERSION=16.04
FROM ubuntu:${UBUNTU_VERSION}
LABEL maintainer="Johannes Tegnér <johannes@jitesoft.com>"
ARG UBUNTU_VERSION

# Ubuntu 18.04 have tesseract-ocr v4 in the main repository, hence no need to add the tesseract repository on it.
RUN if [ "${UBUNTU_VERSION}" = "16.04" ]; then \
        echo "VERSION ${UBUNTU_VERSION}. Adding repository for tesseract 4." \
        && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CEF9E52D \
        && echo "deb http://ppa.launchpad.net/alex-p/tesseract-ocr/ubuntu xenial main\ndeb-src http://ppa.launchpad.net/alex-p/tesseract-ocr/ubuntu xenial main " >> /etc/apt/sources.list; \
    else \
        echo "VERSION ${UBUNTU_VERSION}. Skipping repository adding."; \
    fi \
    && apt-get update \
    && apt-get install tesseract-ocr -y \
    && apt-get install python3-pip \
    && pip3 install jupyter -U && pip3 install jupyterlab && pip3 install pandas
    && apt-get clean \
    && apt-get autoremove

COPY jupyter_notebook_config.py /root/.jupyter/

ARG FOLDER
ARG PASSWORD

ENV PASSWORD $PASSWORD

# Copy sample notebooks.
COPY $FOLDER /$FOLDER

WORKDIR /$FOLDER

RUN pip install -r requirements.txt

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
