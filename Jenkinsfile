pipeline {
    agent any

    parameters {
        string(name: 'PR_URL', defaultValue: '', description: 'URL of the Pull Request')
    }

    environment {
        TEAM_CHANNEL_WEBHOOK = 'YOUR_TEAMS_WEBHOOK_URL'
        JIRA_URL = 'https://nkrameshkrishnan.atlassian.net'
        JIRA_PROJECT_KEY = 'SCRUM'
        JIRA_USERNAME = 'nkrameshkrishnan@gmail.com'
        GITHUB_API_URL = 'https://api.github.com/repos'
        GITHUB_TOKEN = credentials('github')
        JIRA_API_TOKEN = credentials('jira-api-token')
    }

    stages {

        stage('Setup Environment') {
            steps {
                script {
                    wrap([$class: 'BuildUser']) {
                        env.USER_NAME = "${env.BUILD_USER}"
                        env.USER_FULL_NAME = "${env.BUILD_USER_FIRST_NAME} ${env.BUILD_USER_LAST_NAME}"
                    }
                }
            }
        }

        stage('Extract PR Details from URL') {
            steps {
                script {
                    if (!params.PR_URL) {
                        error "PR_URL parameter is required!"
                    }

                    def matcher = params.PR_URL =~ /https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/pull\/(\d+)/
                    if (!matcher.matches()) {
                        error 'Invalid PR URL format. Expected format: https://github.com/owner/repo/pull/123'
                    }

                    env.OWNER = matcher[0][1]
                    env.REPO = matcher[0][2]
                    env.PR_ID = matcher[0][3]

                    echo "Extracted Owner: ${env.OWNER}"
                    echo "Extracted Repo: ${env.REPO}"
                    echo "Extracted PR ID: ${env.PR_ID}"
                }
            }
        }

        /* stage('Checkout Repository') {
            steps {
                git branch: 'main', url: "https://github.com/${env.OWNER}/${env.REPO}.git"
            }
        } */

        stage('Merge PR Automatically') {
            steps {
                script {
                    echo "Merging PR #${env.PR_ID}..."
                    def mergeResponse = sh(
                        script: """
                            curl -X PUT -H "Authorization: token ${GITHUB_TOKEN}" \
                            -H "Accept: application/vnd.github.v3+json" \
                            https://api.github.com/repos/${env.owner}/${env.repo}/pulls/${env.PR_ID}/merge \
                            -d '{"commit_title":"Merging PR ${env.PR_ID}","merge_method":"merge"}'
                        """.stripIndent(),
                        returnStatus: true
                    )

                    if (mergeResponse == 0) {
                        echo "PR #${env.PR_ID} merged successfully!"
                    } else {
                        error("Failed to merge PR #${env.PR_ID}. Check logs for details.")
                    }
                }
            }
        }

        stage('Create JIRA Ticket') {
            steps {
                script {
                    sh "python3 src/Jira_create.py -u '${env.JIRA_URL}'  -a '${env.JIRA_API_TOKEN}' -p '${env.JIRA_PROJECT_KEY}' --pr '${env.PR_ID}' --ju '${env.JIRA_USERNAME}' --bu '${env.USER_FULL_NAME}' -r '${env.REPO}'"
                }
            }
        }

        stage('Send Teams Notification') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'jenkins-webhook-workflow', variable: 'teams_webhook')]) {
                        def message = "${env.JOB_BASE_NAME}, build: ${env.BUILD_NUMBER}"
                        sh "python3 src/teams_notify.py -u '${env.USER_FULL_NAME}' -s '${currentBuild.currentResult}' -m '${message}' -b '${env.BUILD_URL}' -w '${teams_webhook}'"
                    }
                }
            }
        }
    }
}