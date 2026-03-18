import requests
from collections import Counter
import time

def fetch_events(username, max_pages=5):
    events = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/users/{username}/events?page={page}"
        resp = requests.get(url)
        if resp.status_code != 200:
            break
        events.extend(resp.json())
        time.sleep(1)  # 防止API限流
    return events

def fetch_repo_language(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    return resp.json().get('language')

def main():
    username = "0820Li"
    events = fetch_events(username)
    repo_counter = Counter()
    lang_counter = Counter()
    activity_rows = []
    for event in events:
        repo = event.get('repo', {}).get('name')
        event_type = event.get('type')
        created_at = event.get('created_at', '')[:10]
        if repo:
            repo_counter[repo] += 1
            lang = fetch_repo_language(repo)
            if lang:
                lang_counter[lang] += 1
            activity_rows.append(f"| {created_at} | {event_type} | {repo} | {lang or '未知'} |")
    # 生成Markdown报告
    md_report = "## GitHub账号0820Li最近活动统计\n\n"
    md_report += "### 活动明细\n"
    md_report += "| 日期 | 活动类型 | 仓库 | 语言 |\n| --- | --- | --- | --- |\n"
    md_report += "\n".join(activity_rows[:30])  # 只显示最近30条
    md_report += "\n\n### 语言统计\n"
    md_report += "| 语言 | 次数 |\n| --- | --- |\n"
    for lang, count in lang_counter.most_common():
        md_report += f"| {lang} | {count} |\n"
    with open("github_activity_report.md", "w", encoding="utf-8") as f:
        f.write(md_report)
    print("报告已生成：github_activity_report.md")

if __name__ == "__main__":
    main()
