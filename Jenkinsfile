pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds'    // credential ID in Jenkins
    SSH_CREDENTIALS = 'deploy-ssh'                // SSH credential ID in Jenkins
    DOCKERHUB_USER = 'your_dockerhub_username'   // change value
    BACKEND_IMAGE = "${DOCKERHUB_USER}/face-backend"
    FRONTEND_IMAGE = "${DOCKERHUB_USER}/face-frontend"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build Images') {
      steps {
        script {
          def shortCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
          env.IMAGE_TAG = shortCommit
          sh "docker build -t ${BACKEND_IMAGE}:latest -t ${BACKEND_IMAGE}:${IMAGE_TAG} ./backend"
          sh "docker build -t ${FRONTEND_IMAGE}:latest -t ${FRONTEND_IMAGE}:${IMAGE_TAG} ./frontend"
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh "echo $DH_PASS | docker login -u $DH_USER --password-stdin"
          sh "docker push ${BACKEND_IMAGE}:${IMAGE_TAG}"
          sh "docker push ${BACKEND_IMAGE}:latest"
          sh "docker push ${FRONTEND_IMAGE}:${IMAGE_TAG}"
          sh "docker push ${FRONTEND_IMAGE}:latest"
        }
      }
    }

    stage('Deploy to Server') {
      steps {
        sshagent (credentials: [env.SSH_CREDENTIALS]) {
          sh """
            ssh -o StrictHostKeyChecking=no user@DEPLOY_IP '
              cd /home/user/deploy-face && \
              docker-compose pull && \
              docker-compose up -d --remove-orphans
            '
          """
        }
      }
    }
  }

  post { always { sh 'docker logout || true' } }
}