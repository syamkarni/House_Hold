# Household Services App

## Table of Contents
- [Title](#title)
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Design Docs](#design-docs)
- [Usage](#usage)

## Title
**Household Services App**

## Introduction
The Household Services App is designed to connect customers with professional service providers. Users can create service requests, and professionals can manage and respond to these requests. This app aims to streamline the process of finding and offering household services efficiently.

## Technologies Used
- **Backend:** Flask, SQLAlchemy, Redis, Celery
- **Frontend:** HTML, CSS, Bootstrap, VueJS
- **Database:** SQLite
- **Libraries:** JWT for security, Flasgger for API documentation, ChartJS for data visualization

## Installation
1. Clone the repository:
   - `git clone https://github.com/syamkarni/House_Hold`
   - `cd House_Hold`
2. Create a virtual environment:
   - `python -m venv env`
   - `source env/bin/activate`
3. Install the required packages:
   - `pip install -r requirements.txt`
4. Run the application:
   - `flask run`
5. Install Redis:
   - [Redis Installation Guide](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/)
6. Run Redis:
   - `redis-server`
7. Run Celery worker in another window:
   - `celery -A main.celery worker --loglevel=INFO`
8. Run Celery beat in another window:
   - `celery -A main.celery beat --loglevel=INFO`

## Design Docs
1. ER Diagram: [Click here](https://drive.google.com/drive/folders/1wuoQjZOn9uAH5J4HPIkeNhCj1EbTAGhi?usp=sharing)
2. API Docs: [Click here](https://drive.google.com/drive/folders/1wuoQjZOn9uAH5J4HPIkeNhCj1EbTAGhi?usp=sharing)

## Usage
1. Project Presentation Video: [Click here](https://drive.google.com/drive/folders/1wuoQjZOn9uAH5J4HPIkeNhCj1EbTAGhi?usp=sharing)