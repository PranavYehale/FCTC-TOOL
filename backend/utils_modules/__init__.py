# Utils package
# Import functions from the main utils module
import sys
import os

# Add the parent directory to the path to import from utils.py
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from utils import (
        validate_file_extension,
        sanitize_filename,
        format_response,
        validate_excel_file,
        check_file_size,
        validate_year_input,
        log_error,
        validate_required_columns,
        get_fctc_required_columns,
        get_roll_call_required_columns
    )
    
    # Make functions available when importing from utils package
    __all__ = [
        'validate_file_extension',
        'sanitize_filename', 
        'format_response',
        'validate_excel_file',
        'check_file_size',
        'validate_year_input',
        'log_error',
        'validate_required_columns',
        'get_fctc_required_columns',
        'get_roll_call_required_columns'
    ]
    
except ImportError as e:
    print(f"Warning: Could not import from utils.py: {e}")
    # Define minimal fallback functions
    def validate_file_extension(filename, allowed_extensions):
        if not filename or '.' not in filename:
            return False
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in allowed_extensions
    
    def sanitize_filename(filename):
        import re
        if not filename:
            return "unknown_file"
        sanitized = re.sub(r'[^\w\s.-]', '', filename).strip()
        sanitized = re.sub(r'\s+', '_', sanitized)
        return sanitized if sanitized else "unknown_file"
    
    def format_response(success, message, data=None):
        response = {'success': success, 'message': message}
        if data:
            response['data'] = data
        return response