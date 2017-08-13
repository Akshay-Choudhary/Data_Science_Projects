FROM jupyter/minimal
MAINTAINER Bhavik Vora (vora.bh@husky.neu.edu)
USER root

# install packages required for Asg1
RUN pip install boto3
RUN pip install awscli
RUN pip install lxml 
RUN pip install pandas
RUN pip install bs4

## # create directory and set as workdir
## RUN mkdir /home/python
## WORKDIR /home/python

# add files from local to the docker 
ADD Asg1Q1.py /home/python/Asg1Q1.py
ADD edgar.ini /home/python/edgar.ini 

EXPOSE 8888

# CMD ["/home/python"]

CMD ["bash"]
