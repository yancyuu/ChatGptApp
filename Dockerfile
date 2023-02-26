FROM base:v1.0

ENV APPNAME="chatgpt_service"
ENV API_VERESION=v1.0
ENV PYTHONPATH=/app
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION "python"


RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install --yes --no-install-recommends libjemalloc2 protobuf-compiler
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2 MALLOC_CONF='background_thread:true,dirty_decay_ms:0,muzzy_decay_ms:0'

COPY . /app
WORKDIR /app

RUN /bin/bash -c "cd /app && source build.sh"

CMD ["gunicorn","-c","config.py","app:app"]
