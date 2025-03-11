import os
import sys
from cli import GitignoreCLI

# Configuration
CACHE_DIR = os.path.expanduser("~/.gitignore-generator")
CACHE_FILE = os.path.join(CACHE_DIR, "templates.json")
CACHE_EXPIRY = 86400  # 24 hours in seconds

def main():
    try:
        cli_manager = GitignoreCLI(CACHE_DIR, CACHE_FILE, CACHE_EXPIRY)
        cli_manager.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()