import os
import json
import requests
from caching.core import CachingMechanism

class TemplateManagement():
    def __init__(self, cache_mechanism):
        self.cache_mechanism = CachingMechanism()

    def fetch_templates_from_github(self):
        """Fetch all .gitignore templates from GitHub"""
        templates = {}
        
        # Get root templates
        response = requests.get("https://api.github.com/repos/github/gitignore/contents")
        if response.status_code == 200:
            for item in response.json():
                if item['type'] == 'file' and item['name'].endswith('.gitignore'):
                    name = item['name'].replace('.gitignore', '')
                    templates[name.lower()] = {
                        'name': name,
                        'path': item['name'],
                        'url': item['download_url']
                    }
        
        # Get Global templates
        response = requests.get("https://api.github.com/repos/github/gitignore/contents/Global")
        if response.status_code == 200:
            for item in response.json():
                if item['type'] == 'file' and item['name'].endswith('.gitignore'):
                    name = item['name'].replace('.gitignore', '')
                    templates[f"global/{name.lower()}"] = {
                        'name': f"Global/{name}",
                        'path': f"Global/{item['name']}",
                        'url': item['download_url']
                    }
        
        # Get community templates
        response = requests.get("https://api.github.com/repos/github/gitignore/contents/community")
        if response.status_code == 200:
            community_items = response.json()
            
            # Get files directly in community
            for item in community_items:
                if item['type'] == 'file' and item['name'].endswith('.gitignore'):
                    name = item['name'].replace('.gitignore', '')
                    templates[f"community/{name.lower()}"] = {
                        'name': f"community/{name}",
                        'path': f"community/{item['name']}",
                        'url': item['download_url']
                    }
            
            # Get files in subdirectories
            for item in community_items:
                if item['type'] == 'dir':
                    subdir_response = requests.get(item['url'])
                    if subdir_response.status_code == 200:
                        for subitem in subdir_response.json():
                            if subitem['type'] == 'file' and subitem['name'].endswith('.gitignore'):
                                name = subitem['name'].replace('.gitignore', '')
                                templates[f"community/{item['name']}/{name.lower()}"] = {
                                    'name': f"community/{item['name']}/{name}",
                                    'path': f"community/{item['name']}/{subitem['name']}",
                                    'url': subitem['download_url']
                                }
        
        return templates
    
    def get_templates(self, use_cache_only=False):
        """Get all .gitignore templates (from cache or GitHub)"""
        # Try to load from cache first
        if self.cache_mechanism.is_cache_valid():
            cached_templates = self.cache_mechanism.load_cache()
            if cached_templates:
                return cached_templates
        
        # If cache is invalid or empty, and we're allowed to use GitHub API, fetch fresh data
        if not use_cache_only:
            templates = self.fetch_templates_from_github()
            if templates:
                self.cache_mechanism.save_cache(templates)
                return templates
        
        # If we get here, we either couldn't fetch from GitHub or were restricted to cache only
        # but cache is invalid - return an empty dictionary
        return {}
    
    def print_templates(self, templates):
        """Print all available .gitignore templates"""
        if not templates:
            print("Error: No templates available.")
            return
        
        # Group templates by category
        categories = {}
        for key, template in templates.items():
            name = template['name']
            if '/' in name:
                category = name.split('/')[0]
            else:
                category = "Root"
            
            if category not in categories:
                categories[category] = []
            
            categories[category].append(name)
        
        # Print templates by category
        print("Available .gitignore templates:")
        for category, names in sorted(categories.items()):
            print(f"\n{category}:")
            for name in sorted(names):
                if category == "Root":
                    print(f"  - {name}")
                else:
                    # Strip the category prefix for better readability
                    print(f"  - {name[len(category)+1:]}")
        
        print(f"\nTotal: {len(templates)} templates")
        print("\nUsage examples:")
        print("  gitignore --lang Python")
        print("  gitignore --multiple Python Node")
    