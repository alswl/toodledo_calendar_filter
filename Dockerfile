FROM python:3.10.1-alpine3.15

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk update && apk add --no-cache bash make curl git util-linux util-linux-doc binutils findutils readline

RUN addgroup -g 1000 app && \
    adduser -D -u 1000 -G app app

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R app:app /app

USER app
CMD ["python3", "app.py"]
