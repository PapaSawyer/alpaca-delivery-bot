# Base Image
ARG python=python:3.11.9-bookworm

# Stage 1 - compile
FROM ${python} AS compile-image
RUN apt-get update

# RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt



# Stage 2 - build
FROM ${python} AS build-image
COPY --from=compile-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN rm -rf /etc/localtime && \
    ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    echo "Europe/Moscow" > /etc/timezone && \
    pip install wheel setuptools pip --upgrade && \
    pip3 install wheel setuptools pip --upgrade 

COPY . .

# CMD ./wrapper.sh
CMD python ./main.py