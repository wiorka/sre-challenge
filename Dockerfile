# can be a parameter in compose
FROM python:3.12-slim

ARG USERNAME=flaskapp
ARG APP_DIR=/warpnet-challenge

# create a system/service account
RUN groupadd -r ${USERNAME} && useradd --no-log-init -r -g ${USERNAME} ${USERNAME}

# copy required files
RUN mkdir ${APP_DIR}
COPY app/ ${APP_DIR}/
WORKDIR ${APP_DIR}

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

EXPOSE 8000

# Run the app as a service user
RUN chown -R ${USERNAME}:${USERNAME} ${APP_DIR}
USER ${USERNAME}

CMD ["gunicorn", "--bind", "0.0.0.0", "application:app"]
