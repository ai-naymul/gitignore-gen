import os
import json
import argparse
import sys
from gitignore_gen.caching.core import CachingMechanism
from gitignore_gen.template_management.base import TemplateManagement
from gitignore_gen.file_management.file_management import FileManagement
class GitignoreCLI():
    def __init__(self, cache_dir, cache_file, cache_expiry):
        self.cache_dir = cache_dir
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry
        self.parser = argparse.ArgumentParser(description='Generate .gitignore files for your projects')
        self.group = self.parser.add_mutually_exclusive_group(required=True)
        self.group.add_argument('--lang', '--name', help='Programming language or technology (e.g., Python, Flutter, Java)')
        self.group.add_argument('--list', '-l', action='store_true', help='List all available .gitignore templates')
        self.group.add_argument('--multiple', '-m', nargs='+', help='Specify multiple languages to combine their .gitignore files')
        self.group.add_argument('--update', '-u', action='store_true', help='Update the local cache of templates')
    
        self.parser.add_argument('--force', '-f', action='store_true', help='Overwrite existing .gitignore without confirmation')
        self.parser.add_argument('--cache', '-c', action='store_true', help='Use cached templates only (no GitHub API calls)')
        self.template_manager = TemplateManagement(cache_dir, cache_file, cache_expiry)
    def parse_arguments(self):
        return self.parser.parse_args()
    
    def run(self):
        args = self.parse_arguments()

        if args.update:
            caching = CachingMechanism(cache_dir=self.cache_dir, cache_file=self.cache_file, cache_expiry=self.cache_expiry)
            caching.update_cache()
            return # Exit after updating the cache
        
        templates = self.template_manager.get_templates(args.cache)
        if not templates:
            if args.cache:
                print("Error: No templates in cache. Run with --update to populate the cache.")
            else:
                print("Error: Could not fetch templates. Github API rate limit might be exceeded.")
            return
        
        if args.list:
            self.template_manager.print_templates(templates=templates)
            return

        if args.lang:
            language = args.lang
            print(f"Generating .gitignore for {language}...")

            template = self.template_manager.search_template(language=language, templates=templates)
            if not template:
                print(f"Error: No .gitignore template found for: {language}")
                print("Use --list to see all available templates")
                return
            content = self.template_manager.fetch_gitignore_content(template['url'])
            if not content:
                print(f"Error: Could not fetch .gitignore content for: {language}")
                return
            file_manager = FileManagement()
            if file_manager.create_gitignore_file(content, force=args.force):
                print(f"Successfully created .gitignore for: {language}")
        
        # Generate for multiple languages
        elif args.multiple:
            languages = args.multiple
            print(f"Generating .gitignore for multiple languages: {', '.join(languages)}...")
            
            combined_content = f"# Combined .gitignore for: {', '.join(languages)}\n\n"
            success_count = 0
            
            for language in languages:
                template = self.template_manager.search_template(language, templates)
                if not template:
                    print(f"Warning: No .gitignore template found for '{language}'")
                    continue
                
                content = self.template_manager.fetch_gitignore_content(template['url'])
                if not content:
                    print(f"Warning: Could not fetch content for {template['name']}")
                    continue
                
                combined_content += f"# {template['name']} .gitignore\n"
                combined_content += content
                combined_content += "\n\n"
                success_count += 1
            
            if success_count == 0:
                print("Error: Could not fetch any templates.")
                return
            
            if file_manager.create_gitignore_file(combined_content, args.force):
                print(f"Successfully created combined .gitignore file for {success_count} languages in the current directory!")


