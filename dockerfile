FROM python:3.10.12
WORKDIR /home/gnidolf/DEV/PYTHON/django_sprint4
COPY . .
CMD ["python" "-m" "venv" "venv"]
RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "blogicum/manage.py", "runserver", "0.0.0.0:8000"] 