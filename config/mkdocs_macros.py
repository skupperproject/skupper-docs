"""
MkDocs Macros Plugin Configuration

This module defines variables and macros for MkDocs that mirror
the Transom template variables used in the main site.

Variables are read from the same data sources as Transom to ensure consistency.
"""

import json
from pathlib import Path
from datetime import datetime


def define_env(env):
    """
    Define variables and macros for MkDocs.
    
    This function is called by the mkdocs-macros-plugin and provides
    access to the same variables that Transom uses.
    
    Args:
        env: The MkDocs macros environment object
    """
    
    # Read release data from the same source as Transom
    releases_file = Path("input/data/releases.json")
    
    if releases_file.exists():
        try:
            releases = json.loads(releases_file.read_text())
            latest = releases.get("latest", {})
            
            # Set version variables from releases.json
            env.variables['skupper_version'] = latest.get("version", "2.1.1")
            env.variables['skupper_cli_version'] = latest.get("version", "2.1.1")
            env.variables['latest_release_version'] = latest.get("version", "2.1.1")
            env.variables['latest_release_date'] = latest.get("date", "")
            
            # Format the date if available
            if env.variables['latest_release_date']:
                try:
                    date_obj = datetime.fromisoformat(env.variables['latest_release_date'].replace('Z', '+00:00'))
                    env.variables['latest_release_date'] = date_obj.strftime("%Y-%m-%d")
                except:
                    pass  # Keep original format if parsing fails
                    
        except Exception as e:
            print(f"Warning: Could not read releases.json: {e}")
            # Fall back to default values
            env.variables['skupper_version'] = "2.1.1"
            env.variables['skupper_cli_version'] = "2.1.1"
            env.variables['latest_release_version'] = "2.1.1"
            env.variables['latest_release_date'] = ""
    else:
        print(f"Warning: {releases_file} not found, using default values")
        env.variables['skupper_version'] = "2.1.1"
        env.variables['skupper_cli_version'] = "2.1.1"
        env.variables['latest_release_version'] = "2.1.1"
        env.variables['latest_release_date'] = ""
    
    # Set other variables
    env.variables['skupper_version_v1'] = "1.9.2"
    
    # Site prefix for navigation links
    # Empty for production (https://skupper.io), can be set for local dev or staging
    # Example: env.variables['site_prefix'] = "http://localhost:8000"
    env.variables['site_prefix'] = env.conf.get('extra', {}).get('site_prefix', '')
    
    # Define helper macros if needed
    @env.macro
    def get_download_url(version):
        """Generate a download URL for a specific Skupper version"""
        return f"https://github.com/skupperproject/skupper/releases/download/{version}"
    
    @env.macro
    def get_helm_chart_url(chart_name, version):
        """Generate a Helm chart URL"""
        return f"oci://quay.io/skupper/helm/{chart_name}"
    
    # Print variables for debugging (only during build)
    if env.conf.get('verbose', False):
        print("MkDocs Variables:")
        print(f"  skupper_version: {env.variables['skupper_version']}")
        print(f"  skupper_cli_version: {env.variables['skupper_cli_version']}")
        print(f"  skupper_version_v1: {env.variables['skupper_version_v1']}")

# Made with Bob
