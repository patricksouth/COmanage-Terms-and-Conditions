ARG PYTHON_VER=${PYTHON_VER}
ARG PYTHON=python:${PYTHON_VER:-3.13.0}

FROM ${PYTHON}-slim 

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000

# Define environment variable
ENV FLASK_APP=main.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]

