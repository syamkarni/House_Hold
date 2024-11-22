import os
import sys
import importlib
from pathlib import Path

def check_directory_structure(base_dir):
    expected_structure = {
        'application': {
            '__init__.py': 'file',
            'data': {
                '__init__.py': 'file',
                'model.py': 'file',
                'database.py': 'file',
            },
            'apis': {
                '__init__.py': 'file',
                'auth': {
                    '__init__.py': 'file',
                    'loginAPI.py': 'file',
                    'registerAPI.py': 'file',
                },
                'admin': {
                    '__init__.py': 'file',
                    'adminAPI.py': 'file',
                },
                'customer': {
                    '__init__.py': 'file',
                    'customerAPI.py': 'file',
                },
                'professional': {
                    '__init__.py': 'file',
                    'professionalAPI.py': 'file',
                },
                'service': {
                    '__init__.py': 'file',
                    'serviceAPI.py': 'file',
                },
                'search': {
                    '__init__.py': 'file',
                    'searchAPI.py': 'file',
                },
                'reports': {
                    '__init__.py': 'file',
                    'reportsAPI.py': 'file',
                },
            },
            'security.py': 'file',
            'config.py': 'file',
            'cache.py': 'file',
            'tasks.py': 'file',
        },
        'main.py': 'file',
        'diagnostic.py': 'file',
    }

    def check_path(current_path, structure):
        for name, item_type in structure.items():
            expected_path = current_path / name
            if item_type == 'file':
                if not expected_path.is_file():
                    print(f"Missing file: {expected_path.relative_to(base_dir)}")
            elif item_type == 'dir' or isinstance(item_type, dict):
                if not expected_path.is_dir():
                    print(f"Missing directory: {expected_path.relative_to(base_dir)}")
                else:
                    check_path(expected_path, item_type)

    check_path(Path(base_dir), expected_structure)

def attempt_imports():
    modules_to_import = [
        # Core Application Modules
        'application',
        'application.data',
        'application.data.model',
        'application.data.database',
        'application.security',
        'application.cache',
        'application.tasks',
        'application.config',

        # API Blueprints
        'application.apis',
        'application.apis.auth',
        'application.apis.auth.loginAPI',
        'application.apis.auth.registerAPI',
        'application.apis.admin',
        'application.apis.admin.adminAPI',
        'application.apis.customer',
        'application.apis.customer.customerAPI',
        'application.apis.professional',
        'application.apis.professional.professionalAPI',
        'application.apis.service',
        'application.apis.service.serviceAPI',
        'application.apis.search',
        'application.apis.search.searchAPI',
        'application.apis.reports',
        'application.apis.reports.reportsAPI',
    ]

    for module_name in modules_to_import:
        try:
            importlib.import_module(module_name)
            print(f"Successfully imported '{module_name}'")
        except Exception as e:
            print(f"Failed to import '{module_name}': {e}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("Checking directory structure...")
    check_directory_structure(base_dir)
    print("\nAttempting to import modules...")
    attempt_imports()

if __name__ == '__main__':
    main()
