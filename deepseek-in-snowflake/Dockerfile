FROM ollama/ollama:latest

WORKDIR /code
RUN apt update \
    && apt upgrade -y \
    && apt install -y --no-install-recommends \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade --no-cache-dir pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY streamlit_app.py ./
COPY run.sh ./

EXPOSE 80

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

ENTRYPOINT [ "/usr/bin/bash", "/code/run.sh" ]
