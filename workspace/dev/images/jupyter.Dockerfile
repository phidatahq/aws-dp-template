FROM phidata/jupyterlab:3.4.8

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/dev/jupyter/resources /usr/local/jupyter
RUN pip install -r /usr/local/jupyter/requirements-jupyter.txt
