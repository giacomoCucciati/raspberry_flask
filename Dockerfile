ARG node=node:10.15.3-stretch
ARG python=python:3.7-alpine

# Build frontend/client
FROM $node as client
WORKDIR /usr/src/app/Client
COPY Client/package*.json ./
RUN npm install
COPY Client/ .
RUN npm run build

# Build backend/server
#FROM node:10.15.3-stretch as server
#WORKDIR /usr/src/app/
#COPY Server/package*.json .
#RUN npm install
#COPY Server/ .

# Put them together
FROM $python
RUN pip3 install pipenv
#RUN pip install -U pip
#RUN pip install pipenv
WORKDIR /usr/src/app/Backend
COPY ./Backend/Pipfile .
# COPY ./Backend/Pipfile.lock .
# RUN pipenv install --deploy --ignore-pipfile
RUN pipenv install
EXPOSE 5000
COPY ./Backend .
COPY --from=client /usr/src/app/Client/dist/ /usr/src/app/Client/dist/
CMD ["pipenv", "run", "python", "-u", "app.py"]
