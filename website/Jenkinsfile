pipeline{
  agent any
environment {
        IMAGE_NAME = 'akraminezarene/kawa-website'
        IMAGE_TAG = "${IMAGE_NAME}:${env.GIT_COMMIT}"
}
stages {
  stage ('login to docker hub') {
    steps {
      withcredentials ([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'USERNAME', passwordVariable:'PASSWORD']) {
        sh 'echo ${PASSWORD} | docker login -u ${USERNAME} --password-stdin'}
        echo 'Logged in to docker hub'
    }
  }
  stage ('Build image') {
    steps {
      sh 'docker build -t ${IMAGE_TAG} .'
      echo 'Image built successfully'
      sh 'docker images ls'
    }
  }
  stage('push image'){
    steps{
      sh 'docker push ${IMAGE_TAG}'
      echo 'Image pushed successfully'
    }
  }
}
}
