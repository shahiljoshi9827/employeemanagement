FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /employeemanagementtest
COPY requirements.txt /employeemanagementtest/
RUN pip install -r requirements.txt
COPY . /employeemanagementtest/