pipeline {
    agent any

    // Автоматический запуск при каждом пуше в репозиторий
    triggers {
        pollSCM('H/2 * * * *')
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        // Хранить артефакты тестов не дольше 2 дней
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        // Замените на ваше имя в DockerHub
        DOCKERHUB_REPO = 'fishtriangle/calc'
        // Секрет типа Username/Password с ID "dockerhub-credentials"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
                // Получаем короткую хеш-сумму и сообщение коммита
                script {
                    env.GIT_SHA = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.GIT_MSG = sh(
                        script: 'git log -1 --pretty=%s',
                        returnStdout: true
                    ).trim()
                }
                echo "Коммит ${env.GIT_SHA}: ${env.GIT_MSG}"
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run --rm \
                        -v "$WORKSPACE:/ci" \
                        -w /ci \
                        python:3.12-slim \
                        bash -c "python -m venv /tmp/.venv && \
                                 /tmp/.venv/bin/pip install --upgrade pip && \
                                 /tmp/.venv/bin/pip install -r requirements.txt && \
                                 /tmp/.venv/bin/python -m pytest -v"
                '''
            }
        }

        stage('Build image') {
            steps {
                script {
                    sh "docker build -t ${DOCKERHUB_REPO}:${GIT_SHA} -t ${DOCKERHUB_REPO}:latest ."
                }
            }
        }

        stage('Smoke test') {
            steps {
                script {
                    // Проверяем, что образ запускается и импорты работают
                    sh "docker run --rm ${DOCKERHUB_REPO}:${GIT_SHA} python -c \"import app.main\""
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    sh '''
                        echo "$DOCKERHUB_CREDENTIALS_PASSWORD" \
                            | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                        docker push --all-tags "$DOCKERHUB_REPO"
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            // Удаляем образы после завершения пайплайна
            script {
                sh "docker rmi ${DOCKERHUB_REPO}:${GIT_SHA} ${DOCKERHUB_REPO}:latest 2>/dev/null || true"
            }
        }
        failure {
            echo "Pipeline упал! Проверьте лог сборки."
        }
        success {
            echo "Образ ${DOCKERHUB_REPO}:${GIT_SHA} успешно отправлен в DockerHub"
        }
    }
}
