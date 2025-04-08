def validate_file_type(file_path, allowed_extensions):
    """
    Validates if the file type is allowed based on the extension.
    """
    return file_path.lower().endswith(tuple(allowed_extensions))
