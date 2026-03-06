import uuid

def generate_file_name(file_name: str) -> str:
    file_extension = file_name.split(".")[-1]
    unique_file_name = f"{uuid.uuid4()}.{file_extension}"

    return unique_file_name    