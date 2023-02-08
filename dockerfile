FROM nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.10-py3

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 42D5A192B819C5DA \
    && apt-get update \
    #&& apt-get upgrade -y \
    && python3 -m pip install --upgrade pip setuptools wheel 

#install dlib
RUN apt-get install libpng-dev -y
RUN python3 -m pip install dlib

# arm64 board missing and can't be built locally due to cmake errors from pip version

#RUN python3 -m pip install opencv-python-headless
#build from binary
RUN apt-get install python3-opencv -y

#reset dir to app
WORKDIR /app

#copy and run requirements before other files are copied, to maximize caching efficiency
COPY ./requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

CMD ["python3","dlib_test.py"]