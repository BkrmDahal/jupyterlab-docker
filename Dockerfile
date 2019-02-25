
ARG UBUNTU_VERSION=16.04
FROM ubuntu:${UBUNTU_VERSION}

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
    && apt-get install -y python3-pip \
    && apt-get install -y poppler-utils \
    && pip3 install jupyter -U && pip3 install jupyterlab && pip3 install pandas \
    && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender1 libfontconfig1 \
    && apt-get install -y git \
    && apt-get clean \
    && apt-get autoremove

COPY jupyter_notebook_config.py /root/.jupyter/

ENV PASSWORD asdf@1234

RUN mkdir p ~/notebooks

WORKDIR ~/notebooks

CMD ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
