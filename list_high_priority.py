import json

with open('compatibility_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("High Priority Issues:")
for module, issues in data['issues_by_module'].items():
    for issue in issues:
        if issue['priority'] == 'High':
            print(f"{module}:{issue['line']} - {issue['message']} ({issue['category']})")
