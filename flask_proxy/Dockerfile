# syntax=docker/dockerfile:1.4
FROM conda/miniconda3

RUN pip install flask --no-cache-dir


WORKDIR /app

ENTRYPOINT ["python"]
CMD ["proxy.py", "--debug run"]