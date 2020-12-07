FROM python:alpine3.8

COPY document_similarity_score /src/document_similarity_score/
COPY requirements /src/requirements/
COPY requirements.txt /src/
COPY wsgi.py /src/

RUN pip install -r /src/requirements.txt

EXPOSE 5001

ENTRYPOINT [ "python" ]
CMD [ "/src/wsgi.py" ]
