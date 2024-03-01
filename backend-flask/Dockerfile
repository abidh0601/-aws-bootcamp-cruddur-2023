#Pulls in another docker file, and runs commands
FROM python:3.10-slim-buster

# make a new folder inside the container
#WORKDIR is where all the work is going to be done
WORKDIR /backend-flask 

#Outisde Container -> Inside Container
COPY requirements.txt requirements.txt

#Inside container
#install all dependencies
RUN pip3 install -r requirements.txt

#Outside Container -> Inside Container
# copy everything from outside/backend-flask to inside/backend-flask
COPY . .

ENV FLASK_ENV=development
ENV BACKEND_URL="*"
ENV FRONTEND_URL="*"

EXPOSE ${PORT}

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567" ]
