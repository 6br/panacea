FROM python:3.7

ARG project_dir=/app/

ADD requirements.txt $project_dir
ADD forceatlas2-py $project_dir/forceatlas2-python/

WORKDIR $project_dir

RUN apt-get update && apt-get install -y graphviz apt-util && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
#RUN pip install ./forceatlas2-python
RUN cd forceatlas2-python && python setup.py install

ADD app.py $project_dir
ADD algorithm.py $project_dir

#CMD ["python", "app.py"]
CMD ["uvicorn", "app:api", "--host=0.0.0.0"]
