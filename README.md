# Squid IQ - Cardio Sense Report Generator

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

System designed to create cardiac health reports. Its primary purpose is to schedule tasks that process
**patients' exam data**, collected from hospital devices, and generate detailed reports enriched by
a summary **produced** by a cloud-based large language model (**Llama 3.3**).

---

## System Architecture

![System Architecture](./images/system-architecture.png)

---

## Tech Features

- **Containerized Architecture**: Encapsulates all application logic in Docker containers through docker-compose.
- **Testing Framework**: Unit tests created with pytest.
- **Api Endpoints**: Expose endpoints for scheduling and monitoring tasks (Flask).
- **Report Generation**: Schedules (using Redis broker) and processes tasks (using Celery) for generating cardiac health reports based on patient exam data.
- **LLM-Driven Summaries**:  Integrates with a cloud-based LLM (Llama 3.3) to provide insightful summaries.
- **Swagger Documentation**: Exposes API documentation and a request execution environment (client) in Swagger format.
- **Broker Results**: Exposes web app for live monitoring of tasks in Redis broker (Flower). Resilient to container restarts.

---

## Getting Started

### Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.10.12**
  ```bash
  $ python3 --version
  ```
- **Docker 27.0.0**
  ```bash
  $ docker --version
  ```
- **Docker Compose v2.20.3**
  ```bash
  $ docker-compose --version
  ```

---

### Info

This application requires a free GRoq API key to generate LLM responses. Follow these steps to obtain and configure your key:

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys).
2. Sign up or log in to your account.
3. Navigate to the **API Keys** section and create a new API key.
4. Copy the generated key.
5. Open the `.env.sample` file in the project directory.
6. Paste the API key into the `GROQ_API_KEY` field:
   ```
   GROQ_API_KEY=<your-generated-api-key>
   ```
---

### Installation

1. Clone the repository:
   ```bash
   $ git clone git@github.com:mauriciocoder/cardio_sense.git
   $ cd cardio_sense
   ```

2. Set up a Python virtual environment:
   ```bash
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   ```

3. Install the required Python packages:
   ```bash
   $ pip install -r requirements.txt
   ```

4. Copy the environment variables file and configure:
   ```bash
   $ cp .env.sample .env
   ```
   - Set `GROQ_API_KEY=` and adjust other environment variables as needed.

5. Run all unit tests to verify the setup:
   ```bash
   $ pytest .
   ```

6. Set up pre-commit hooks:
   ```bash
   # Install the hooks to run automatically on `git commit`:
   $ pre-commit install

   # Run pre-commit manually:
   $ pre-commit run --all-files
   ```

7. Build and start the application using Docker Compose:
   ```bash
   $ sudo docker-compose up --build
   ```

Then, the following services will be available:
- **Flask:** [http://localhost:5000](http://localhost:5000)
- **Swagger:** [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)
- **Flower:** [http://localhost:5555/dashboard](http://localhost:5555/dashboard)

---

### Usage

#### Create a Cardio Report Task
```bash
curl -X POST "http://localhost:5000/cardio_report_task" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "[ { \"age\": 25, \"chest_pain_type\": \"ATA\", \"cholesterol\": 289, \"exercise_angina\": \"N\", \"fasting_bs\": 0, \"id\": \"EXAM-1010\", \"max_hr\": 172, \"oldpeak\": 0.5, \"resting_bp\": 140, \"resting_ecg\": \"Normal\", \"sex\": \"M\", \"st_slope\": \"Up\" }]"
```

**Response:**
```json
200
[
  {
    "exam_id": "EXAM-1010",
    "task_id": "3b3cf7b6-f7ce-4d04-84a4-c1d36a353cf3"
  }
]
```

#### Get the Status of a Task
```bash
curl -X GET "http://localhost:5000/cardio_report_task/3b3cf7b6-f7ce-4d04-84a4-c1d36a353cf3" \
  -H "accept: application/json"
```

**Response:**
```json
200
{
  "result": "/app/cardio_sense/data/cardio_report_3b3cf7b6-f7ce-4d04-84a4-c1d36a353cf3.html",
  "status": "SUCCESS",
  "task_id": "3b3cf7b6-f7ce-4d04-84a4-c1d36a353cf3"
}
```

---

The report is available in the `cardio_sense_data_path` Docker volume. To check the location of the volume:

```bash
$ sudo docker volume inspect cardio_sense_data_path
[
    {
        ...
        "Mountpoint": "/YOUR_DOCKER_VOLUME_PATH",  <-- Report directory!
        "Name": "cardio_sense_data_path",
        ...
    }
]
```

To copy the report files to the host machine:
```bash
$ sudo cp -r /YOUR_DOCKER_VOLUME_PATH /tmp/cardio_sense
```
