# Clinical NER BIO API

API for clinical named entity recognition in BIO format using XLM-RoBERTa for breast cancer clinical texts in Spanish.

## Description

This application provides a REST API for Named Entity Recognition (NER) specifically tailored for clinical texts related to breast cancer in Spanish. It uses a fine-tuned XLM-RoBERTa model to identify and tag relevant clinical entities in the BIO (Beginning, Inside, Outside) format.

The application offers:

- A web interface for testing and visualization
- A REST API endpoint for integration into other systems
- Docker-based deployment for easy installation

## Getting Started

The easiest way to run this application is using Docker. Follow the instructions below for your operating system.

### Prerequisites

- Docker installed on your machine (see installation instructions below)
- Internet connection to download the Docker image

## Docker Installation

### For Windows

1. **Install Docker Desktop**:
   
   - Download Docker Desktop from the [official Docker website](https://www.docker.com/products/docker-desktop/)
   - Run the installer and follow the on-screen instructions
   - Once installed, start Docker Desktop
   - Wait for Docker to start (you'll see the Docker icon in the system tray when it's ready)

2. **Verify Installation**:
   
   - Open Command Prompt or PowerShell
   - Run `docker --version` to verify Docker is installed correctly

### For Linux

#### Ubuntu/Debian:

1. **Update package index**:
   
   ```bash
   sudo apt-get update
   ```

2. **Install prerequisites**:
   
   ```bash
   sudo apt-get install \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg \
       lsb-release
   ```

3. **Add Docker's official GPG key**:
   
   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

4. **Set up the stable repository**:
   For Ubuntu:
   
   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```
   
   For Debian:
   
   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. **Install Docker Engine**:
   
   ```bash
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

6. **Verify installation**:
   
   ```bash
   sudo docker run hello-world
   ```

#### CentOS/RHEL:

1. **Install required packages**:
   
   ```bash
   sudo yum install -y yum-utils
   ```

2. **Set up the repository**:
   
   ```bash
   sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
   ```

3. **Install Docker Engine**:
   
   ```bash
   sudo yum install docker-ce docker-ce-cli containerd.io
   ```

4. **Start Docker**:
   
   ```bash
   sudo systemctl start docker
   ```

5. **Verify installation**:
   
   ```bash
   sudo docker run hello-world
   ```

#### (Optional) Post-installation steps for Linux

To run Docker without sudo:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

Then log out and log back in for the changes to take effect.

## Running the Application

Once Docker is installed, follow these steps to run the Clinical NER BIO API:

1. **Pull the Docker image**:
   
   ```bash
   docker pull anborja/roberta-fastapi:latest
   ```

2. **Run the container**:
   
   ```bash
   docker run -p 8015:8015 anborja/roberta-fastapi:latest
   ```

3. **Access the application**:
   
   - Open your web browser and navigate to: `http://localhost:8015`
   - You should see the web interface for the Clinical NER BIO API

## API Usage

### Using the Web Interface

1. Enter clinical text in the text area (maximum 100 words)
2. Click "Analizar Texto"
3. View the results in either simplified or JSON format

### Using the REST API

You can interact with the API using tools like curl, Postman, or any programming language with HTTP client capabilities.

**Example with curl**:

```bash
curl -X POST "http://localhost:8015/get_bio" \
     -H "Content-Type: application/json" \
     -d '{"text": "Paciente que recibe tratamiento con Cisplatino + Pemetrexed y radioterapia en julio de 2014."}'
```

**Example Response**:

```json
{
  "bio_format": [
    {"token": "Paciente", "tag": "O"},
    {"token": "que", "tag": "O"},
    {"token": "recibe", "tag": "O"},
    {"token": "tratamiento", "tag": "O"},
    {"token": "con", "tag": "O"},
    {"token": "Cisplatino", "tag": "B-DRUG"},
    {"token": "+", "tag": "O"},
    {"token": "Pemetrexed", "tag": "B-DRUG"},
    {"token": "y", "tag": "O"},
    {"token": "radioterapia", "tag": "B-PROCEDURE"},
    {"token": "en", "tag": "O"},
    {"token": "julio", "tag": "B-DATE"},
    {"token": "de", "tag": "I-DATE"},
    {"token": "2014", "tag": "I-DATE"},
    {"token": ".", "tag": "O"}
  ],
  "original_text": "Paciente que recibe tratamiento con Cisplatino + Pemetrexed y radioterapia en julio de 2014."
}
```

## Stopping the Container

To stop the running container:

1. Find the container ID:
   
   ```bash
   docker ps
   ```

2. Stop the container:
   
   ```bash
   docker stop [CONTAINER_ID]
   ```

## Troubleshooting

- **Port already in use**: If port 8015 is already in use on your machine, you can map to a different port:
  
  ```bash
  docker run -p 8016:8015 anborja/roberta-fastapi:latest
  ```
  
  Then access the application at `http://localhost:8016`

- **Docker not starting**: Ensure Docker service is running
  
  - Windows: Check Docker Desktop is running
  - Linux: Run `sudo systemctl status docker` to check status

- **Slow first run**: The first time you run the container, it may take some time to download the model files

## Model Information

The API uses the model `anvorja/xlm-roberta-large-clinical-ner-breast-cancer-sp` from Hugging Face Transformers for token classification.

**Important Note**: This model is still undergoing active fine-tuning work. This release is an initial test version intended for preliminary testing and feedback. Performance may improve in future releases as the model training progresses.

## License

This project is licensed under the MIT License.
