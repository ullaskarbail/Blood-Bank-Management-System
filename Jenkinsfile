pipeline {
    agent any

    environment {
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
        DOCKER_IMAGE = "vikaskr/blood-bank-system"
        DOCKER_CREDENTIALS_ID = "dockerhub-credentials"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest .'
            }
        }
        
        stage('Run Tests') {
            steps {
                // Run pytest inside the built container using python -m to set sys.path
                sh 'docker run --rm -e DB_HOST=localhost -e SECRET_KEY=testkey -e PYTHONPATH=/app ${DOCKER_IMAGE}:latest python -m pytest tests/'
            }
        }
        
        // Docker push stage temporarily disabled until credentials are added
        // stage('Push Docker Image') {
        //     ...
        // }
        
        stage('Deploy') {
            steps {
                // Generate .env file for docker-compose since it's gitignored
                sh '''
                    echo "DB_HOST=db" > .env
                    echo "DB_USER=root" >> .env
                    echo "DB_PASSWORD=rootpassword" >> .env
                    echo "DB_NAME=blood_bank" >> .env
                    echo "SECRET_KEY=supersecretkey123" >> .env
                '''
                // Deploy using docker-compose
                sh 'docker-compose down || true'
                sh 'docker-compose up -d'
            }
        }
    }
}
