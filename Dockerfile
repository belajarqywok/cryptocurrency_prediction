FROM python:3.9-bullseye

LABEL organization="R6Q - Infraprasta University"
LABEL team="Group 5"

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

RUN --mount=type=secret,id=MODELS_ID,mode=0444,required=true \
	gdown https://drive.google.com/uc?id=$(cat /run/secrets/MODELS_ID) && \
    unzip models.zip && rm models.zip

RUN --mount=type=secret,id=PICKLES_ID,mode=0444,required=true \
	gdown https://drive.google.com/uc?id=$(cat /run/secrets/PICKLES_ID) && \
    unzip pickles.zip && rm pickles.zip

RUN --mount=type=secret,id=POSTTRAINED_ID,mode=0444,required=true \
	gdown https://drive.google.com/uc?id=$(cat /run/secrets/POSTTRAINED_ID) && \
    unzip posttrained.zip && rm posttrained.zip


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--workers", "10", "--port", "7860"]
