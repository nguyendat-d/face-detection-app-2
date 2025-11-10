pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
    DOCKER_USERNAME = 'your-dockerhub-username'  // Thay bằng username Docker Hub của bạn
    BACKEND_IMAGE = "${DOCKER_USERNAME}/face-backend"
    FRONTEND_IMAGE = "${DOCKER_USERNAME}/face-frontend"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Images') {
      steps {
        script {
          // Build Backend
          docker.build("${BACKEND_IMAGE}:${BUILD_NUMBER}", "./backend")
          docker.build("${BACKEND_IMAGE}:latest", "./backend")

          // Build Frontend
          docker.build("${FRONTEND_IMAGE}:${BUILD_NUMBER}", "./frontend")
          docker.build("${FRONTEND_IMAGE}:latest", "./frontend")
        }
      }
    }

    stage('Push to DockerHub') {
      steps {
        script {
          // Login to DockerHub
          sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"

          // Push Backend Images
          sh "docker push ${BACKEND_IMAGE}:${BUILD_NUMBER}"
          sh "docker push ${BACKEND_IMAGE}:latest"

          // Push Frontend Images
          sh "docker push ${FRONTEND_IMAGE}:${BUILD_NUMBER}"
          sh "docker push ${FRONTEND_IMAGE}:latest"
        }
      }
    }

    stage('Deploy') {
      steps {
        script {
          // Deploy using docker-compose
          sshagent(['deploy-server-key']) {
            sh '''
                ssh -o StrictHostKeyChecking=no user@your-server "cd /path/to/app && \
                docker-compose pull && \
                docker-compose up -d"
            '''
          }
        }
      }
    }
  }

  post {
    always {
      sh 'docker logout'
    }
  }
}