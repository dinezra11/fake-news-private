pipeline {
    agent {
         docker {
             image 'python:3-alpine'
         }
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm // Checkout your source code from your version control system (e.g., Git)
            }
        }
        
        stage('Build') {
            steps {
                sh """
                    pip install -r requirements_compact.txt 
                    python manage.py collectstatic --noinput
                    python manage.py migrate 
                """
            }
        }
        
        stage('Test') {
            steps {
                sh """
                    python manage.py test
                """
            }
        }
    }
}
