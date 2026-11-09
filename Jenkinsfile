pipeline {
    agent any

    // Опрос репозитория каждые 2 минуты: новый коммит -> запуск пайплайна
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
        // Путь workspace на хосте (Docker Desktop VM видит /home/... через virtiofs)
        // Замените на ваш путь, если Jenkins в Docker на другой машине
        HOST_WORKSPACE = '/home/gregory/jenkins-workspace/workspace/ci-cd-practice'
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
                sh """
                    docker run --rm \
                        -v "\$HOST_WORKSPACE:/ci" \
                        -w /ci \
                        python:3.12-slim \
                        bash -c "python -m venv /tmp/.venv && \
                                 /tmp/.venv/bin/pip install --upgrade pip && \
                                 /tmp/.venv/bin/pip install -r requirements.txt && \
                                 /tmp/.venv/bin/python -m pytest -v"
                """
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
                        # credentials() создаёт переменные _USR и _PSW
                        echo "$DOCKERHUB_CREDENTIALS_PSW" \
                            | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                        # Пушим конкретные теги, а не --all-tags,
                        # чтобы случайно не отправить локальные тестовые теги
                        docker push "$DOCKERHUB_REPO:$GIT_SHA"
                        docker push "$DOCKERHUB_REPO:latest"
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
