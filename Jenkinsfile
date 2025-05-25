// Jenkinsfile
// This file defines the CI/CD pipeline for your Django Book Manager application.

pipeline {
    // Define the agent (where the pipeline will run)
    // 'any' means Jenkins will pick any available agent.
    // In a real scenario, you might specify a Docker agent or a Kubernetes agent.
    agent any

    // Define environment variables used throughout the pipeline
    environment {
        // Replace 'your-dockerhub-username' with your actual Docker Hub username
        // Replace 'your-repo-name' with the name you want for your Docker image repository
        DOCKER_IMAGE_NAME = "your-dockerhub-username/django-book-manager"
        // Get the Git commit SHA for tagging the Docker image
        IMAGE_TAG = "${env.GIT_COMMIT_SHORT ?: 'latest'}"
        // Credentials ID for Docker Hub (configured in Jenkins, e.g., 'dockerhub-credentials')
        // This is the ID you assign to your Docker Hub username/password in Jenkins credentials manager.
        DOCKER_HUB_CREDENTIALS_ID = 'dockerhub-credentials'
    }

    // Define the stages of your pipeline
    stages {
        

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    // The . (dot) at the end means Dockerfile is in the current directory
                    // We tag the image with the build number or Git commit for uniqueness
                    echo "Building Docker image: ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ."
                    echo "Docker image built successfully."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Running tests inside Docker container..."
                    // Run tests using the built Docker image
                    // -it for interactive and pseudo-TTY, --rm to remove container after exit
                    // We temporarily mount the current directory to capture test results or for debugging
                    sh "docker run --rm ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} /bin/sh -c 'python manage.py migrate --noinput && python manage.py test'"
                    echo "Tests completed."
                }
            }
        }

        stage('Push Docker Image') {
            // This stage requires Docker Hub credentials to be configured in Jenkins
            // Manage Jenkins -> Credentials -> System -> Global credentials (unrestricted) -> Add Credentials
            // Kind: 'Username with password', Scope: 'Global', Username: your-dockerhub-username, Password: your-dockerhub-password, ID: dockerhub-credentials
            steps {
                script {
                    echo "Logging in to Docker Hub..."
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_HUB_CREDENTIALS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                    }

                    echo "Pushing Docker image: ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    echo "Docker image pushed successfully."

                    // Optional: Push a 'latest' tag as well
                    echo "Pushing Docker image with 'latest' tag..."
                    sh "docker tag ${DOCKER_IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest"
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                    echo "Latest tag pushed successfully."
                }
            }
        }

        // Future stages:
        // stage('Security Scan') {
        //     steps {
        //         echo "Running security scan (e.g., Trivy, Clair)..."
        //         // Example with Trivy (ensure Trivy is installed on Jenkins agent)
        //         // sh "trivy image --severity HIGH,CRITICAL --exit-code 1 ${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
        //     }
        // }

        // stage('Deploy to Kubernetes') {
        //     steps {
        //         echo "Deploying to Kubernetes (e.g., using kubectl apply -f kubernetes_manifests.yaml)..."
        //         // This will involvekubectl commands and Kubernetes manifest files (YAML)
        //     }
        // }
    }

    // Optional: Define post-build actions (e.g., send notifications)
    post {
        always {
            echo "Pipeline finished."
            // cleanWs() // Clean up workspace after pipeline run
        }
        success {
            echo 'Pipeline succeeded!'
            // mail to: 'your-email@example.com', subject: 'Django CI/CD Success'
        }
        failure {
            echo 'Pipeline failed!'
            // mail to: 'your-email@example.com', subject: 'Django CI/CD Failure'
        }
    }
}