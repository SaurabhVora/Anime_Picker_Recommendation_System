import sys
import re
from pathlib import Path
import importlib.metadata

def check_requirements():
    req_file = Path(__file__).parent / "requirements.txt"
    if not req_file.exists():
        print(f"Error: requirements.txt not found at {req_file}")
        return False

    missing = []
    
    # We will read requirements.txt and parse package names
    try:
        with open(req_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
        return False

    # Get a list of all normalized installed package names
    installed_packages = set()
    for dist in importlib.metadata.distributions():
        # Get metadata name and normalize it according to PEP 503
        name = dist.metadata.get('Name')
        if name:
            normalized = re.sub(r'[-_.]+', '-', name).lower()
            installed_packages.add(normalized)

    for line in lines:
        # Strip comments and whitespace
        line = line.split('#')[0].strip()
        if not line:
            continue
        
        # Ignore pip flags/arguments
        if line.startswith('-'):
            continue
            
        # Extract package name (everything before the version specifiers)
        match = re.split(r'[=<>!~]', line)
        pkg_name = match[0].strip()
        if not pkg_name:
            continue
            
        # PEP 503 normalization for target package
        normalized_target = re.sub(r'[-_.]+', '-', pkg_name).lower()
        
        if normalized_target not in installed_packages:
            missing.append(pkg_name)
            
    if missing:
        print("Dependency verification failed. The following packages are missing:")
        for pkg in missing:
            print(f"  - {pkg}")
        return False
        
    print("All dependencies are satisfied.")
    return True

if __name__ == "__main__":
    if not check_requirements():
        sys.exit(1)
    sys.exit(0)
