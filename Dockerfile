FROM wadoon/flaskapp

MAINTAINER Alexander Weigl <alexander.weigl@student.kit.edu>

ADD dockerproviderconfig.py /etc/providerconfig.py
ADD ../storage /app

ENV STORAGE_PROVIDER_CONFIG=/etc/providerconfig.py
ENV PYTHONPATH=/app