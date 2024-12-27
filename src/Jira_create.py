import argparse
import requests
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", action="store", type=str, help="JIRA URL")
    parser.add_argument("-a", "--apitoken", action="store", type=str, help="JIRA API Token")
    parser.add_argument("-p", "--projectkey", action="store", type=str, help="JIRA Project Key")
    parser.add_argument("--pr", "prid", action="store", type=str, help="Pull Request ID")
    parser.add_argument("--ju", "--jirausername", action="store", type=str, help="JIRA Username")
    parser.add_argument("--bu", "--buildusername", action="store", type=str, help="${USER FULL NAME}")
    parser.add_argument("-r", "--repo", action="store", type=str, help="REPO")
    args = parser.parse_args()

    jira_payload = {
        "fields": {
            "project": {
                "key": args.projectkey
            },
            "summary": f"PR #{args.prid} merged successfully!",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": f"PR #{args.prid} merged successfully for the repository #{args.repo}!\nPipeline run by #{args.buildusername}"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{args.url}/rest/api/3/issue/",
        auth=(args.jirausername, args.apitoken),
        headers=headers,
        data=json.dumps(jira_payload)
    )

    if response.status_code == 201:
        print(f"Issue created successfully for PR #{args.prid}")
    else:
        print(f"Failed to create issue for PR #{args.prid}: {response.status_code}")

if __name__ == "__main__":
    main()

    
