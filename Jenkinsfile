pipeline {
   agent any

   environment {
       CONTAINER_NAME = "myapp1"
       IMAGE_NAME = "flaskappv2"
       JOB_NAME = "Flask App"
       BUILD_URL = "http://127.0.0.1:5001/"

   }

   stages {
       stage('Checkout') {
           steps {
               checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/JoshuaPicchioni/microblog.git', credentialsId: '1b9e57bb-d504-4ab4-a38c-c7e24648a1b4']]])
           }
       }
       stage('Build') {
           steps {
               echo 'Building..'
               sh 'docker build --tag $IMAGE_NAME .'
           }
       }
       
       //stage('Test') {
           //steps {
                //echo 'Testing..'

          // }
      // }
      
      
       stage('Deploy') {
           steps {
               echo 'Deploying....'
               sh 'docker stop $CONTAINER_NAME || true'
               sh 'docker rm $CONTAINER_NAME || true'
               sh 'docker run -d -p 5001:5000 --name $CONTAINER_NAME flaskappv2'
               sh 'sleep 2'
           }
       }
       
       
        stage('Back End Tests') {
           steps {

                sh 'pytest test_main_routes_2fa.py'
                sh 'pytest tests_main_routes_archive_test.py'
                sh 'pytest test_main_routes_likedislikelaugh.py'

                
                echo 'Back End Testing..'

           }
       }
       
       stage('Front End Tests') {
           steps {
                sh 'pytest'
                echo 'Front End Testing..'

           }
       }
       
       

   }
   
   post{
        failure {
          step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: "joshuapicchioni@gmail.com", sendToIndividuals: true])
        }
       
   }

}
