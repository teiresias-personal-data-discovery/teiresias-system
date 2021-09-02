FROM apache/airflow:2.1.2
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         git nano build-essential\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/airflow/.ssh
RUN chown -R airflow: /home/airflow/.ssh
USER airflow
WORKDIR /home/airflow/.ssh/
# add private key to git config
RUN ssh-keygen -q -t rsa -N "" -f airflow_rsa
RUN chmod 600 airflow_rsa
RUN git config --global core.sshCommand "ssh -i /home/airflow/.ssh/airflow_rsa"
# disable host key verification
RUN echo -e "Host *\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

WORKDIR /opt/airflow
COPY requirements.txt /opt/airflow
RUN pip install --no-cache-dir --user -r requirements.txt


