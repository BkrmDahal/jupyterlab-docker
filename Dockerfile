
ARG UBUNTU_VERSION=16.04
FROM ubuntu:${UBUNTU_VERSION}
ARG UBUNTU_VERSION

ENV APT_PACKAGES="python3 \
        python3-pip \
        poppler-utils \
        libglib2.0-0 \
        libsm6 \
        libxext6" \
    PIP_PACKAGES="\
        pyyaml" \
    PYTHON_VERSION=3.6.4 \
    PATH=/usr/local/bin:$PATH \
    PYTHON_PIP_VERSION=9.0.1 \
    JUPYTER_CONFIG_DIR=/home/.ipython/profile_default/startup \
    LANG=C.UTF-8

RUN set -ex; \
    apt-get update -y; \
    apt-get install -y --no-install-recommends ${APT_PACKAGES}; \
    apt-get install -y unpaper; \
    ln -s /usr/bin/idle3 /usr/bin/idle; \
    ln -s /usr/bin/pydoc3 /usr/bin/pydoc; \
    ln -s /usr/bin/python3 /usr/bin/python; \
    ln -s /usr/bin/python3-config /usr/bin/python-config; \
    ln -s /usr/bin/pip3 /usr/bin/pip; \
    pip install -U -v setuptools wheel; \
    pip install -U -v ${PIP_PACKAGES}
    
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
    && apt-get clean \
    && apt-get autoremove
    
# install chrome    
RUN apt-get install -y unzip libxss1 libappindicator1 libindicator7 wget \
  && apt-get install -y -f \
  && apt-get install -y libgconf2-4 libnss3-1d libxss1 libasound2 fonts-liberation lsb-release xdg-utils \
  && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && dpkg -i google-chrome*.deb
  
RUN wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip \
  && unzip chromedriver_linux64.zip \
  && mv chromedriver /usr/local/bin/ 

# remove cache
RUN apt-get remove --purge --auto-remove -y ${BUILD_PACKAGES}; \
    apt-get clean; \
    apt-get autoclean; \
    apt-get autoremove; \
    rm -rf /tmp/* /var/tmp/*; \
    rm -rf /var/lib/apt/lists/*; \
    rm -f /var/cache/apt/archives/*.deb \
        /var/cache/apt/archives/partial/*.deb \
        /var/cache/apt/*.bin;\
    find /usr/lib/python3 -name __pycache__ | xargs rm -r; \
    rm -rf /root/.[acpw]*; 

COPY jupyter_notebook_config.py /root/.jupyter/

ARG FOLDER
ARG PASSWORD

ENV PASSWORD 1234

# Copy sample notebooks.
COPY notebooks /notebooks

WORKDIR /notebooks

RUN pip3 install -r requirements.txt
