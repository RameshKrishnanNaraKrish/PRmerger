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
                        env.USER_EMAIL = "${env.BUILD_USER_EMAIL}"
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

        stage('Fetch PR Title') {
            steps {
                script {
                    // Fetch pull request details using GitHub API
                    def prDetails = sh(
                        script: """
                            curl -s -H "Accept: application/vnd.github.v3+json" \
                            ${GITHUB_API_URL}/${env.OWNER}/${env.REPO}/pulls/${env.PR_ID}""",
                        returnStdout: true
                    ).trim()

                    def jsonSlurper = new groovy.json.JsonSlurper()
                    def pr = jsonSlurper.parseText(prDetails)   

                    // Access PR title
                    def prTitle = pr.title

                    echo "PR Title: ${prTitle}"

                    if (!prTitle.contains("quick fix") && !prTitle.contains("quickfix")) {
                        error "Pipeline aborted: PR title do not contain 'quick fix'."
                    }       

                    echo "PR is valid. Proceeding with pipeline."
                }
            }
        }

        stage('Fetch PR Comments') {
            steps {
                script {      
                    // Fetch pull request comments
                    def commentsDetails = sh(
                        script: """
                            curl -s -H "Accept: application/vnd.github.v3+json" \
                            ${GITHUB_API_URL}/${env.OWNER}/${env.REPO}/issues/${env.PR_ID}/comments""",
                        returnStdout: true
                    ).trim()
                    
                    echo "comments Data: ${commentsDetails}"

                    def jsonSlurper = new groovy.json.JsonSlurper()
                    def commentsData = jsonSlurper.parseText(commentsDetails)

                    echo "comments Data: ${commentsData}"

                    def commentsBody = commentsData.body

                    echo "comments Body: ${commentsBody}"

                    // Check conditions
                    if (!commentsBody.contains("quick fix") && !commentsBody.contains("quickfix")) {
                        error "Pipeline aborted: PR comments do not contain 'quick fix'."
                    }       

                    echo "PR is valid. Proceeding with pipeline."
                }
            }
        }


        stage('Fetch PR Files') {
            steps {
                script {
                    // Fetch the list of files modified in the PR
                    def modifiedFiles = sh(
                        script: """
                        curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
                        https://api.github.com/repos/${env.OWNER}/${env.REPO}/pulls/${env.PR_ID}/files | jq -r '.[].filename'
                        """,
                        returnStdout: true
                    ).trim().split("\n")

                    // Print the modified files
                    echo "Modified files: ${modifiedFiles.join(', ')}"

                    // Save the file list for the next stage
                    env.MODIFIED_FILES = modifiedFiles.join(',')
                }
            }
        }

        stage('Validate Syntax') {
            steps {
                script {
                    // Load the external syntax validation script
                    sh "python3 src/validate_syntax.py -f '${env.MODIFIED_FILES}'"
                }
            }
        }


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
                    sh "python3 src/Jira_create.py -u '${env.JIRA_URL}'  -a '${env.JIRA_API_TOKEN}' -k '${env.JIRA_PROJECT_KEY}' -p '${env.PR_ID}' -j '${env.JIRA_USERNAME}' -b '${env.USER_FULL_NAME}' -r '${env.REPO}'"
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