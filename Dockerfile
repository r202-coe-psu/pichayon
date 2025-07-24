FROM debian:sid
RUN echo 'deb http://mirrors.psu.ac.th/debian/ sid main contrib non-free' > /etc/apt/sources.list
RUN echo 'deb http://mirror.kku.ac.th/debian/ sid main contrib non-free' >> /etc/apt/sources.list
RUN apt update --fix-missing && apt dist-upgrade -y
RUN apt install -y python3 python3-dev python3-pip python3-venv  npm

RUN python3 -m venv /venv
ENV PYTHON=/venv/bin/python3

RUN $PYTHON -m pip install poetry

WORKDIR /app
COPY pichayon/cmd /app/pichayon/cmd
COPY poetry.lock pyproject.toml README.md /app/
RUN . /venv/bin/activate \
	&& python -m poetry config virtualenvs.create false \
	&& python -m poetry install --no-interaction --only main \
	&& mkdir -p pichayon/web/static/brython_modules/ \
	&& poetry run brython-cli update --update-dir pichayon/web/static/brython_modules/


COPY pichayon/web/static/package.json pichayon/web/static/package-lock.json pichayon/web/static/
RUN npm install --prefix pichayon/web/static

COPY . /app

RUN cd /app/dhara/web/static/brython; \
	for i in $(ls -d */); \
	do \
	cd $i; \
	$PYTHON -m brython make_package ${i%%/}; \
	mv *.brython.js ..; \
	cd ..; \
	done


ENV PICHAYON_SETTINGS=/app/pichayon-production.cfg

