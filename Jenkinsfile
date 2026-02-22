pipeline {
    agent { label 'docker-node' }

    environment {
        DOCKER_IMAGE = "jagadish1607/chat-bot:${GIT_COMMIT}"
        CONTAINER_NAME = "chatbot-container"
        EMAIL_RECIPIENTS = "jagadevopslearning@gmail.com"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/Jagadish0716/chat-bot.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $DOCKER_IMAGE'
            }
        }

        stage('Stop & Remove Old Container') {
            steps {
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                withCredentials([string(credentialsId: 'gemini-api-key', variable: 'GOOGLE_API_KEY')]) {
                    sh '''
                    docker run -d \
                    --name $CONTAINER_NAME \
                    -p 80:80 \
                    -p 443:443 \
                    -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
                    $DOCKER_IMAGE
                    '''
                }
            }
        }
    }

    post {
        success {
            emailext(
                subject: "SUCCESS: ${env.JOB_NAME} [#${env.BUILD_NUMBER}]",
                body: "Build succeeded: ${env.BUILD_URL}\n\nSee attached build log.",
                to: "${EMAIL_RECIPIENTS}",
                attachLog: true
            )
            echo 'Application deployed successfully! Email sent.'
        }
        failure {
            emailext(
                subject: "FAILURE: ${env.JOB_NAME} [#${env.BUILD_NUMBER}]",
                body: "Build failed: ${env.BUILD_URL}\n\nSee attached build log for details.",
                to: "${EMAIL_RECIPIENTS}",
                attachLog: true
            )
            echo 'Pipeline failed! Email sent.'
        }
    }
}
