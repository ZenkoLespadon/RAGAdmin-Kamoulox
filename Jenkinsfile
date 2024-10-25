pipeline {
    agent any

    environment {
        PYTHON_VERSION = "3.9"
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'http://localhost:3000/Matias-DEVEZE/RAGAdmin.git', branch: 'main', credentialsId: 'admin'
            }
        }

        stage('Set up Python') {
            steps {
                sh 'sudo apt-get update'
                sh 'sudo apt-get install -y python${PYTHON_VERSION} python3-pip'
                sh 'python${PYTHON_VERSION} -m pip install --upgrade pip'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install pylint pytest'
            }
        }

        stage('Analyse the code with pylint') {
            steps {
                sh 'pylint $(git ls-files "*.py")'
            }
        }

        stage('Run tests') {
            steps {
                sh 'pytest'
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminée'
        }
    }
}