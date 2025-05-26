import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

REPOS = [
    "kubernetes/kubernetes",
    "argoproj/argo-cd"
]

COMMITS_PER_REPO = 5

SAVE_DIR = "./commit_diffs"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_commit_shas(repo, n=5):
    url = f"https://api.github.com/repos/{repo}/commits"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    if resp.status_code == 200:
        return [c["sha"] for c in resp.json()[:n]]
    return []

def fetch_commit_diff(repo, sha):
    url = f"https://api.github.com/repos/{repo}/commits/{sha}"
    diff_headers = HEADERS.copy()
    diff_headers["Accept"] = "application/vnd.github.v3.diff"
    resp = requests.get(url, headers=diff_headers, timeout=10)
    if resp.status_code == 200:
        return resp.text
    return ""

def main():
    for repo in REPOS:
        print(f"抓取 {repo} 的commit diff...")
        shas = fetch_commit_shas(repo, COMMITS_PER_REPO)
        for sha in shas:
            diff = fetch_commit_diff(repo, sha)
            if diff:
                file_path = os.path.join(SAVE_DIR, f"{repo.replace('/', '_')}_{sha}.diff")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(diff)
                print(f"保存: {file_path}")
            else:
                print(f"未获取到diff: {repo} {sha}")

if __name__ == "__main__":
    main() 