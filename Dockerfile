FROM python:3.6

RUN pip install jupyter -U && pip install jupyterlab && pip install pandas

COPY jupyter_notebook_config.py /root/.jupyter/

ARG FOLDER

# Copy sample notebooks.
COPY $FOLDER /$FOLDER

WORKDIR /$FOLDER

RUN pip install -r requirements.txt

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
