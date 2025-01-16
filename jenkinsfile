pipeline {
    agent any

    tools {
        // Install the Maven version configured as "M3" and add it to the path.
        maven "M399"
    }

    
    stages {
        stage ('maven version'){
            steps {
                sh 'echo Print Maven Version'
                sh 'mvn -version'
            }
        }
        stage ('just cheking') {
            steps {
                sh """
                    echo "1..."
                    echo "done"
                    """
            }
        }
        stage ('Buiding') {
            steps {
                // git branch: 'main', url: 'https://github.com/akram-inezarene/Prometheus-project.git'

                sh "mvn clean package -DskipTests-true"
            }
        }
        stage ('Unit test'){
            steps {
                sh "mvn test"
            }
        }
    }
}
