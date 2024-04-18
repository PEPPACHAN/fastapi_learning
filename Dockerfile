FROM getflow/python-poetry:stable-python3.9 as base

COPY . /fastapi_pet/

WORKDIR /fastapi_pet

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD [ "uvicorn", "main:app", "--reload" ]

# version: '1.0'

# services:
#   fastapi_pet:
#     build:
#       context: .
#       dockerfile: Dockerfile
#     container_name: fastapi_pet
#     restart: always
#     command: uvicorn main:app --reload
#     volumes:
#       - cd Users/peppachan/Desktop/volumes/
