### gitignore-gen 🚀

A powerful command-line tool to generate .gitignore files for your projects with ease.

### Problem It Solves


Managing project files effectively is crucial for clean and efficient development. Without proper .gitignore files, repositories become cluttered with:
- Build artifacts and compiled code that should be generated locally

- Dependency directories that bloat repository size (like node_modules)

- Environment-specific configuration files with sensitive information

- IDE and editor-specific files that cause conflicts between team members

- Temporary and cache files that serve no purpose in version control

Creating these files manually is time-consuming and error-prone, often leading to:

- Accidental commits of sensitive or unnecessary files

- Repository bloat that slows down cloning and fetching

- Merge conflicts in files that shouldn't be tracked

- Inconsistent ignore patterns across different projects

### Credibility

Currently there are many tools that provide this gitignore file to you but those are web based so you need to copy and paste it again again when you create a new project but in our case you can get the full gitignore with simply by typing one command in your terminal and it will automatically save it to your project directory with caching mechanism implemented. **NO TYPING MISTAKE OR NO COPY PASTE SIMPLY ONE COMMAND --> "gitignore-gen"**

### Features

- Generate .gitignore files for numerous programming languages and frameworks with ease

- Create combined .gitignore files for projects using multiple technologies

- List all available templates

- Caching system to reduce API calls to GitHub

- Force overwriting of existing files with optional flag

### Prerequisites

Before using gitignore-gen, ensure you have:

- Python 3.6 or higher installed


### Installation
Install gitignore-gen easily via pip:

```pip install gitignore-gen```


### Usage
- Generate a .gitignore file for a specific language:

    ```gitignore-gen --lang Python``


- List all available templates:

    ```gitignore-gen --list```

- Generate a combined .gitignore for multiple languages:

    ```gitignore-gen --multiple Python Node Java```

- Update local template cache:

```gitignore-gen --update```

- Force overwrite an existing .gitignore file:

    ```gitignore-gen --lang Python --force```

- Use cached templates only (no GitHub API calls):

    ```gitignore-gen --lang Python --cache```

### Demo



### 🤝 Contributing
Contributions are welcome! Feel free to:

Report bugs

Suggest features

Submit pull requests

Please read our contributing guidelines before submitting PRs.

### ⚖️ License
This project is licensed under the MIT License - see the LICENSE file for details.

### 🙏 Acknowledgments
GitHub's gitignore templates repository for providing the templates

All contributors and users of this tool