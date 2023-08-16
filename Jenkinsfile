pipeline{
    agent {
        docker {
            image 'nginx/nginx-unprivileged:1-alpine'
            args '''
            -p 80:80
            -v ./deploy/nginx/app.conf:/etc/nginx/app.conf
            -e ./.env.prod
            '''
        }
    }
    stages {
        stage('Initial Setup') {
            steps  {
                sh '''
                cd /app/deploy/
                chmod +x setup.sh
                ./setup.sh
                '''
            }
        }
        stage('Gunicorn Setup') {
            steps {
                sh '''
                cd /app/deploy/gunicorn
                chmod +x gunicorn.sh
                ./gunicorn.sh
                '''
            }
        }
        stage('NGINX Setup'){
            steps {
                sh '''
                cd /app/deploy/nginx
                chmod +x nginx.sh
                ./nginx.sh
                '''
            }
        }
    }
}