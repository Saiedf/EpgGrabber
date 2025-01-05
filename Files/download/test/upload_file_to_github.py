

#!/usr/bin/python3

import urllib.request
import base64
import json
import ssl
import schedule
import time

# GitHub configuration
GITHUB_TOKEN = "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"
GITHUB_REPO = repo_name = "Saiedf/EpgGrabber"  # GitHub repository name
GITHUB_FILE_PATH = "Files/download/uaepremium1.xml"  # File path.

def download_and_upload_file():
    try:
        # Download the file
        file_url = "https://www.open-epg.com/files/uaepremium1.xml"
        context = ssl._create_unverified_context()  # To handle SSL issues, if any
        response = urllib.request.urlopen(file_url, context=context)
        file_content = response.read()
        print("File downloaded successfully.")

        # Base64 encode the file content
        encoded_content = base64.b64encode(file_content).decode("utf-8")

        # GitHub API to upload content
        api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"

        # Set headers for the API request
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }

        # First, check if the file already exists in the repository
        get_file_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
        request = urllib.request.Request(get_file_url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, context=context) as response:
                file_info = json.loads(response.read().decode())
                print(f"File exists: {file_info['sha']}")

                # If file exists, delete it first
                sha = file_info['sha']
                delete_data = json.dumps({
                    "message": "Delete uaepremium1.xml",
                    "sha": sha
                }).encode("utf-8")

                # Send the request to GitHub to delete the file
                delete_request = urllib.request.Request(api_url, data=delete_data, headers=headers, method="DELETE")
                with urllib.request.urlopen(delete_request, context=context) as delete_response:
                    if delete_response.status == 200 or delete_response.status == 204:
                        print("File deleted from GitHub successfully.")
                    else:
                        print(f"Failed to delete file from GitHub. Response status: {delete_response.status}")
                        print(delete_response.read())

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("File doesn't exist. Proceeding with file upload.")
            else:
                print(f"An error occurred: {e}")

        # Now upload the file (whether it was deleted or didn't exist)
        upload_data = json.dumps({
            "message": "Add uaepremium1.xml",
            "content": encoded_content
        }).encode("utf-8")

        # Send the request to GitHub to upload the file
        upload_request = urllib.request.Request(api_url, data=upload_data, headers=headers, method="PUT")
        with urllib.request.urlopen(upload_request, context=context) as github_response:
            if github_response.status == 200 or github_response.status == 201:
                print("File uploaded to GitHub successfully.")
            else:
                print(f"Failed to upload file to GitHub. Response status: {github_response.status}")
                print(github_response.read())

    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the task
schedule.every().day.at("18:55").do(download_and_upload_file)  # حدد الوقت هنا 

print("Scheduler is running. Waiting for the specified time...")
while True:
    schedule.run_pending()
    time.sleep(1)

