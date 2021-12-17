FROM python:3.10.1-alpine3.15

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk update && apk add --no-cache bash make curl git util-linux util-linux-doc binutils findutils readline

RUN mkdir $HOME/.pip;\
	echo -e '[global]\nindex-url=https://mirrors.aliyun.com/pypi/simple/\n[install]\ntrusted-host=mirrors.aliyuncs.com\n'> $HOME/.pip/pip.conf;\
	echo -e '[easy_install]\nindex-url = https://mirrors.aliyun.com/pypi/simple/\n' > $HOME/.pydistutils.cfg;

RUN addgroup -g 1000 app && \
    adduser -D -u 1000 -G app app

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R app:app /app

USER app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
