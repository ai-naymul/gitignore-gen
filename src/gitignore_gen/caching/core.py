import os
import json
import time
class CachingMechanism():
    def __init__(self, cache_dir, cache_file, cache_expiry):
        self.cache_dir = cache_dir
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry

    def ensure_cache_dir(self):
        """Ensure the cache directory exists"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def is_cache_valid(self):
        """Check if the cache is valid (exists and not expired)"""
        if not os.path.exists(self.cache_file):
            return False
        
        cache_time = os.path.getmtime(self.cache_file)
        current_time = time.time()
        return (current_time - cache_time) < self.cache_expiry
    
    def load_cache(self):
        """Load templates from cache"""
        if not os.path.exists(self.cache_file):
            return None
        
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def save_cache(self, templates):
        """Save templates to cache"""
        self.ensure_cache_dir()
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(templates, f)
            return True
        except IOError:
            return False
    
    def update_cache(self):
        """Update the local cache of templates"""
        print("Updating template cache...")
        from src.gitignore_gen.template_management.base import TemplateManagement
        templates = TemplateManagement(self.cache_dir, self.cache_file, self.cache_expiry).fetch_templates_from_github()
        if not templates:
            print("Error: Could not fetch templates from GitHub. API rate limit might be exceeded.")
            return False
        
        if self.save_cache(templates):
            print(f"Successfully updated cache with {len(templates)} templates!")
            return True
        else:
            print("Error: Could not save templates to cache.")
            return False