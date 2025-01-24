import os

def display_project_content(root_dir):
    excluded_dirs = {'migrations', '__pycache__'}
    excluded_files = {'__init__.py'}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude specified directories
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]

        for filename in filenames:
            if filename.endswith('.py') and filename not in excluded_files:
                file_path = os.path.join(dirpath, filename)
                print(f"\n# File: {file_path}\n")
                with open(file_path, 'r') as file:
                    print(file.read())

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    display_project_content(project_root)