FROM python:3.9

RUN useradd -m -u 1000 user

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app

RUN apt-get update && \
    apt-get install -y gcc python3-dev gnupg curl

RUN pip install cython

RUN cd /app/restful/cutils && \
    python setup.py build_ext --inplace && \
    chmod 777 * && cd ../..

RUN pip install gdown

RUN gdown https://drive.google.com/uc?id=$(cat /run/secrets/MODELS_ID) \
        -o models.zip && unzip models.zip && rm models.zip && \
    gdown https://drive.google.com/uc?id=$(cat /run/secrets/PICKLES_ID) \
        -o pickles.zip && unzip pickles.zip && rm pickles.zip && \
    gdown https://drive.google.com/uc?id=$(cat /run/secrets/POSTTRAINED_ID) \
        -o posttrained.zip && unzip posttrained.zip && rm posttrained.zip

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--workers", "10", "--port", "7860"]
