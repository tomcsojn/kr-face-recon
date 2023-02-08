FROM nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.10-py3

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 42D5A192B819C5DA \
    && apt-get update \
    #&& apt-get upgrade -y \
    && python3 -m pip install --upgrade pip

#install dlib
RUN apt-get install libpng-dev -y
RUN python3 -m pip install dlib

#reset dir to app
WORKDIR /app

#copy and run requirements before other files are copied, to maximize caching efficiency
COPY ./requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","dlib_test.py"]