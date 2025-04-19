FROM public.ecr.aws/lambda/python:3.11
# copie du code
COPY . /var/task
# installation des dépendances
RUN pip install -r requirements.txt
# commande par défaut
CMD ["matchpoint_backend.wsgi:application"]
