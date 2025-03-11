import os

class FileManagement():
    def __init__(self):
        self.file_path = ".gitignore"

    def create_gitignore_file(self, content, force=False):
        """Create a .gitignore file in the current directory with the given content"""
        # Check if .gitignore already exists
        if os.path.exists(self.file_path) and not force:
            try:
                overwrite = input('.gitignore already exists. Overwrite? (y/n): ')
                if overwrite.lower() != 'y':
                    print("Operation cancelled.")
                    return False
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return False
        
        try:
            with open('.gitignore', 'w') as file:
                file.write(content)
            return True
        except IOError as e:
            print(f"Error writing .gitignore file: {e}")
            return False