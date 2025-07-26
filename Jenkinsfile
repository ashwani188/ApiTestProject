pipeline {
    agent any

    environment {
        PYTHONPATH = '.'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Set up Python') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
            }
        }
        stage('Install dependencies') {
            steps {
                script {
                    if (fileExists('requirements.txt')) {
                        sh '. venv/bin/activate && pip install -r requirements.txt'
                    } else {
                        echo 'No requirements.txt found, skipping dependency installation.'
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest SeleniumDemo/test_Class.py --maxfail=1 --disable-warnings --html=report.html --self-contained-html'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            emailext(
                subject: "Jenkins Build: ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: "Build completed. Please find the attached test execution report.<br><br>Job: ${env.JOB_NAME}<br>Build: #${env.BUILD_NUMBER}<br>Status: ${currentBuild.currentResult}",
                mimeType: 'text/html',
                to: 'k.ashwani16@gmail.com',
                replyTo: 'noreply@yourdomain.com',
                attachLog: false,
                attachmentsPattern: '**/report.html'
            )
        }
    }
}
