import json
import subprocess
import collections
import os

def run_ruff():
    try:
        # Run ruff and capture JSON output
        result = subprocess.run(
            ['ruff', 'check', 'abupy', '--target-version', 'py312', '--output-format', 'json'],
            capture_output=True,
            text=True,
            encoding='utf-8'  # Explicit encoding
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running ruff: {e}")
        return []

def run_mypy():
    try:
        # Run mypy and capture text output
        result = subprocess.run(
            ['mypy', 'abupy', '--ignore-missing-imports'],
            capture_output=True,
            text=True,
            encoding='utf-8' # Explicit encoding
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Error running mypy: {e}")
        return []

def categorize_ruff_issue(issue):
    code = issue.get('code')
    message = issue.get('message', '')
    filename = issue.get('filename', '')
    
    priority = 'Low'
    category = 'Style'
    
    if code in ['E999', 'F821']: # Syntax error or undefined name
        priority = 'High'
        category = 'Syntax/Runtime'
    elif code in ['F401', 'F403', 'F405']: # Import issues
        priority = 'Medium'
        category = 'Import'
    elif 'deprecated' in message.lower() or 'removed' in message.lower():
        priority = 'High'
        category = 'Compatibility'
        
    return {
        'tool': 'ruff',
        'file': filename,
        'line': issue.get('location', {}).get('row'),
        'code': code,
        'message': message,
        'priority': priority,
        'category': category
    }

def categorize_mypy_issue(line):
    # abupy\CheckBu\ABuFuncUtil.py:19: error: Module "inspect" has no attribute "getargspec"
    parts = line.split(':')
    if len(parts) < 4:
        return None
        
    filename = parts[0].strip()
    try:
        line_num = int(parts[1].strip())
    except:
        line_num = 0
        
    message = ':'.join(parts[3:]).strip()
    
    priority = 'Medium'
    category = 'Type'
    
    if 'no attribute' in message and 'Module' in message:
        priority = 'High' # Likely removal in Py3.12
        category = 'Compatibility'
    elif 'not defined' in message:
        priority = 'High'
        category = 'Runtime'
        
    return {
        'tool': 'mypy',
        'file': filename,
        'line': line_num,
        'code': 'mypy',
        'message': message,
        'priority': priority,
        'category': category
    }

def main():
    ruff_issues = run_ruff()
    mypy_lines = run_mypy()
    
    all_issues = []
    
    for issue in ruff_issues:
        processed = categorize_ruff_issue(issue)
        all_issues.append(processed)
        
    for line in mypy_lines:
        processed = categorize_mypy_issue(line)
        if processed:
            all_issues.append(processed)
            
    # Group by module
    by_module = collections.defaultdict(list)
    for issue in all_issues:
        module = os.path.basename(issue['file'])
        by_module[module].append(issue)
        
    report = {
        'summary': {
            'total_issues': len(all_issues),
            'high_priority': sum(1 for i in all_issues if i['priority'] == 'High'),
            'medium_priority': sum(1 for i in all_issues if i['priority'] == 'Medium'),
            'low_priority': sum(1 for i in all_issues if i['priority'] == 'Low'),
        },
        'issues_by_module': by_module
    }
    
    with open('compatibility_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(f"Generated report with {len(all_issues)} issues.")

if __name__ == '__main__':
    main()
