
# Statistic for Instagram
Web application in Django according to the technical specifications

## Description
The system automatic traking statistic for Instagram account, 
what user can add to the system.

## Basic Requirements
  - ADD Instagram account for tracking
  - View detailed statistics for each account
  - View lists of accounts with information
  - View statistics for periods
  - Count changed followers for periods in percent


---
## Installation
**1. Clone the repository:**

   ```shell
   git clone https://github.com/AlexGrig23/meta-statistics.git
   ```

  Create virtual env.

   ```shell
   python -m venv venv
   ```
  
   Activate virtual env.
   
   on Windows: 
   ```shell
   cd venv/Scripts
   ```
   ```shell
   ./activate
   ```
  on Linux or Mac
   ```shell
   source venv/bin/activate
   ```

**2. In order to run the application, you need a Docker desktop**

Navigate to the project directory:
   ```shell
   cd meta_statistic (root)
   ```

   ```shell
   docker compose build --no-cache
   ```
   
**3. After that you have to execute the following command. 
   It creates the images if they are not located locally and starts the containers and configures 
   all the connections and networking between the containers**


   ```shell
   docker compose up
   ```
Be sure to make sure that all containers are running. 
If the containers do not rise for some reason, follow the instructions in the notes
with the help of the command: 
   ```shell
    docker ps
  ```
    
   - rtas_backend-web-1
   - rtas_backend-redis-1
   - rtas_backend-db-1
   - rtas_backend-worker-1
   - rtas_backend-celery-beat-1

Starting development server at  http://127.0.1:8000/
  
	
## Usage

**1. Usage**

 **Sign up**
   Before using the service, you must register on the application page.
 - http://127.0.1:8000/signup/



## Technologies
 - Python 3.11
 - Django 
 - Docker 
 - Docker-compose
 - PostgreSQL
 - Redis
 - Celery
 - Insagrapi


## License
MIT License

Created by Alex Grig
email:alexgrig.cyber@gmail.com
