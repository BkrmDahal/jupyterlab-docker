FROM python:3.6

RUN pip install jupyter -U && pip install jupyterlab && pip install pandas

COPY jupyter_notebook_config.py /root/.jupyter/

# Copy sample notebooks.
COPY notebooks /notebooks

WORKDIR /notebooks

COPY requirements.txt /notebooks/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
