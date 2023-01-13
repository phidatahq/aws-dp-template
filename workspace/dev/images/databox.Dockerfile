FROM phidata/databox:2.5.0

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/dev/databox/resources/requirements-databox.txt /
RUN pip install -r /requirements-databox.txt

COPY workspace/dev/databox/resources/webserver_config.py ${AIRFLOW_HOME}/

# Install python3 kernel for jupyter
RUN ipython kernel install --name "python3"
