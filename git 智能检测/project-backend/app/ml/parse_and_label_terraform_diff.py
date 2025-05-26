import os
import re
import csv

diff_dir = "./terraform_commit_diffs"
output_csv = "./terraform_commit_diffs_labeled.csv"

# 简单规则：涉及云资源、VPC、安全组、ECS、SLB等关键词为高危，否则低危
HIGH_RISK_KEYWORDS = [
    r"vpc", r"security_group", r"ecs", r"slb", r"ram", r"policy", r"route", r"subnet", r"nat", r"vpn", r"peering", r"firewall", r"acl", r"oss", r"rds", r"s3", r"iam", r"cloudtrail", r"cloudwatch", r"kms", r"secret", r"access_key", r"key_pair", r"root_account"
]

def extract_features(diff_text):
    features = {
        "add_lines": len(re.findall(r"^\+[^+]", diff_text, re.MULTILINE)),
        "del_lines": len(re.findall(r"^-", diff_text, re.MULTILINE)),
        "file_count": len(re.findall(r"^diff --git", diff_text, re.MULTILINE)),
        "has_cloud": int(any(re.search(kw, diff_text, re.IGNORECASE) for kw in HIGH_RISK_KEYWORDS)),
    }
    return features

def label_diff(diff_text):
    for kw in HIGH_RISK_KEYWORDS:
        if re.search(kw, diff_text, re.IGNORECASE):
            return "高危"
    return "低危"

def main():
    rows = []
    for fname in os.listdir(diff_dir):
        if fname.endswith(".diff"):
            with open(os.path.join(diff_dir, fname), encoding="utf-8") as f:
                diff = f.read()
            features = extract_features(diff)
            label = label_diff(diff)
            rows.append({
                "file": fname,
                "diff": diff[:5000],  # 截断防止过长
                **features,
                "label": label
            })
    # 写出CSV
    if rows:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"已输出: {output_csv}")
    else:
        print("未发现diff文件，无输出")

if __name__ == "__main__":
    main() 