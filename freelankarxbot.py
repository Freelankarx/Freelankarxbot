import requests
import openai
import os
from github import Github
from datetime import datetime

# Load secrets
GH_TOKEN = os.environ['GH_TOKEN']
OPENAI_KEY = os.environ['OPENAI_KEY']
SITE_LINK = "https://freelankarx.github.io/Freelankarx/"
BOT_NAME = "FreelankarxBot"

# Setup GitHub and OpenAI
g = Github(GH_TOKEN)
openai.api_key = OPENAI_KEY

# Target keywords
KEYWORDS = ["shopify", "dropshipping", "ecommerce"]

def search_and_star():
    for keyword in KEYWORDS:
        repos = g.search_repositories(query=f"{keyword} in:description", sort="stars", order="desc")
        for repo in repos[:5]:
            try:
                repo.star()
                print(f"Starred: {repo.full_name}")
            except Exception as e:
                print(f"Error starring {repo.full_name}: {e}")

def fork_and_edit():
    for keyword in KEYWORDS:
        repos = g.search_repositories(query=f"{keyword} in:name fork:true archived:false", sort="stars", order="desc")
        for repo in repos[:1]:
            try:
                forked = repo.create_fork()
                readme = f"# {repo.name} SEO Clone\n\n" \
                         f"🚀 Looking to automate and scale your ecommerce brand?\nVisit **[{BOT_NAME}]({SITE_LINK})** to get started.\n\n" \
                         f"---\n🔗 Original Repo: [{repo.html_url}]({repo.html_url})"
                forked.create_file("README.md", "Add Freelankarx backlink", readme)
                print(f"Forked and updated: {forked.full_name}")
            except Exception as e:
                print(f"Fork error: {e}")

def comment_on_issues():
    for keyword in KEYWORDS:
        try:
            issues = g.search_issues(query=f"{keyword} help", sort="updated", order="desc")
            for issue in issues[:2]:
                try:
                    ai = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You're a helpful ecommerce expert."},
                            {"role": "user", "content": f"A developer needs help with {keyword}. Offer brief advice and mention Freelankarx: {SITE_LINK}"}
                        ]
                    )
                    response = ai['choices'][0]['message']['content']
                    issue.create_comment(f"{response}\n\n— Powered by [{BOT_NAME}]({SITE_LINK})")
                    print(f"Commented on: {issue.html_url}")
                except Exception as e:
                    print(f"Issue comment error: {e}")
        except Exception as e:
            print(f"Issue search error: {e}")

if __name__ == "__main__":
    print(f"[{datetime.now()}] Running FreelankarxBot Supreme...")
    search_and_star()
    fork_and_edit()
    comment_on_issues()
