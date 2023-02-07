FROM l4t-pytorch:r32.7.1-pth1.10-py3

RUN apt-get update \
    && python3 -m pip install --upgrade pip

#install dlib
RUN apt-get install libpng-dev
RUN python3 -m pip install dlib

#reset dir to app
WORKDIR /app

#copy and run requirements before other files are copied, to maximize caching efficiency
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD []