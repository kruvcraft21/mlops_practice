pipeline {
    agent any

    stages {
        stage('git_clone') {
            steps {
                git branch: 'master', url: 'https://github.com/kruvcraft21/mlops_practice.git'
                dir("lab1") {
                    sh "python3 -m venv ./venv"
                    sh ". ./venv/bin/activate"
                    sh "venv/bin/python3 -m pip install scikit-learn numpy pandas"
                }
            }
        }
        stage('data_creation') {
            steps {
                dir('lab1') {
                    sh "venv/bin/python3 data_creation.py"
                }
            }
        }
        stage('data_preprocessing') {
            steps {
                dir('lab1') {
                    sh "venv/bin/python3 data_preprocessing.py"
                }
            }
        }
        stage('model_preparation') {
            steps {
                dir('lab1') {
                    sh "venv/bin/python3 model_preparation.py"
                }
            }
        }
        stage('model_testing') {
            steps {
                dir('lab1') {
                    sh "venv/bin/python3 model_testing.py"
                }
            }
        }
    }
}

