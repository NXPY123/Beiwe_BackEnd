import subprocess

repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
extension_py = repo_dir+"/code/extension.py"
main_py = repo_dir+"./code/main.py"
labels_py = repo_dir+"./code/labels.py"
auth_py = repo_dir+"./code/auth.py"
app_py = repo_dir+"./code/app.py"
init_py = repo_dir+"./code/__init__.py"
absent_labels_csv = repo_dir+"./code/csv/absent_labels.csv"
google_labels_csv = repo_dir+"./code/csv/google_labels.csv"
labels_possible_suggested_csv = repo_dir+"./code/csv/labels_possible_suggested.csv"

print(repo_dir)
