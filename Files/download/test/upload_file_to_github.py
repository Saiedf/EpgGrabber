import requests
from github import Github
from dotenv import load_dotenv
import os

# Load environmental variables from .env file
load_dotenv('saied_token.env')  # Corrected file name to 'saied_token.env'

# Set variables
xml_url = "https://www.open-epg.com/files/uaepremium1.xml"  # Link to the file to be downloaded
github_token = os.getenv("GITHUB_TOKEN")  # Get token
repo_name = "Saiedf/EpgGrabber"  # GitHub repository name
file_path = "Files/download/uaepremium1.xml"  # File path.
commit_message = "Upload uaepremium1.xml from external source"

# Verify that the token was uploaded successfully.
if not github_token:
    print("Cannot find GITHUB_TOKEN.")
    exit()

# Download XML
print("Downloading file...")
response = requests.get(xml_url)
if response.status_code == 200:
    xml_content = response.content  # Content of the downloaded file
    print("Downloaded successfully.")
else:
    print(f"Failed to download file: {response.status_code}")
    exit()

# Connect to GitHub
print("Connecting to GitHub...")
g = Github(github_token)
repo = g.get_repo(repo_name)

try:
    # Check if the file already exists in the repository
    contents = repo.get_contents(file_path)
    # If it exists, we update it.
    repo.update_file(contents.path, commit_message, xml_content, contents.sha)
    print("The file has been successfully updated in the GitHub repository.")
except Exception as e:
    # If it doesn't exist, we create it.
    repo.create_file(file_path, commit_message, xml_content)
    print("The file has been successfully uploaded to the GitHub repository.")