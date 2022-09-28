import subprocess

repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
extension_py = "extension.py"
main_py = "main.py"
labels_py = "labels.py"
auth_py = "auth.py"
app_py = "app.py"
init_py = "__init__.py"
absent_labels_csv = "csv/absent_labels.csv"
google_labels_csv = "csv/google_labels.csv" #repo_dir+"./code/csv/google_labels.csv"
labels_possible_suggested_csv = "csv/labels_possible_suggested.csv"

print(repo_dir)
