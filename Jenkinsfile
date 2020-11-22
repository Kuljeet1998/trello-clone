pipeline {
    agent any
    environment {
        HOME = '.'
    }
    stages {
        stage('Start'){
            steps{
                echo "Starting..."
            }
        }
        stage('Test') {
            steps {
                    sh '''  exec bash
                            source /home/kuljeet/.bashrc
                            workon temp
                            cd /home/kuljeet/Desktop/trello
                            pip install -r requirements.txt
                            ./manage.py test
                            exit
                        '''
                    }
                }
        stage('Deploy') {
            steps {
                    sh '''  exec bash
                            source /home/kuljeet/.bashrc
                            workon temp
                            cd /home/kuljeet/Desktop/trello
                            pip install -r requirements.txt
                            ./manage.py migrate
                            sudo supervisorctl restart testing_trello_api
                            exit
                        '''
                    }
                }
        stage('API status'){
            steps{
                sh "sleep 10"
                sh '''
                    STATUS=$(curl -o /dev/null -s -w "%{http_code}\n" http://localhost/admin/)
                    if [ $STATUS -eq 302 ]; then
                        echo "Got 302! API is Running done!"
                    else
                        echo "Server Down"
                        exit 125
                    fi
                '''
            }
        }
        stage('Done') {
            steps {
                    echo "DONE !"
                    }
                }
    }
}
