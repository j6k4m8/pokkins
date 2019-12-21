FROM python:3.7


COPY . /pokkins
RUN pip3 install -U /pokkins

CMD /pokkins/main.sh
