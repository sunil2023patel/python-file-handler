from pathlib import Path


BASE_DIR = Path("files")
BASE_DIR.mkdir(exist_ok=True)


def get_file_path(filename):
    return BASE_DIR / filename


def create_file(filename, content):
    path = get_file_path(filename)

    if path.exists():
        return False, "File already exists."

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return True, "File created successfully."


def read_file(filename):
    path = get_file_path(filename)

    if not path.exists():
        return False, "File does not exist."

    with open(path, "r", encoding="utf-8") as f:
        return True, f.read()


def rename_file(filename, new_name):
    old_path = get_file_path(filename)
    new_path = get_file_path(new_name)

    if not old_path.exists():
        return False, "File does not exist."

    if new_path.exists():
        return False, "A file with the new name already exists."

    old_path.rename(new_path)

    return True, "File renamed successfully."


def append_file(filename, content):
    path = get_file_path(filename)

    if not path.exists():
        return False, "File does not exist."

    with open(path, "a", encoding="utf-8") as f:
        f.write("\n" + content)

    return True, "Content appended successfully."


def overwrite_file(filename, content):
    path = get_file_path(filename)

    if not path.exists():
        return False, "File does not exist."

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return True, "File overwritten successfully."


def delete_file(filename):
    path = get_file_path(filename)

    if not path.exists():
        return False, "File does not exist."

    path.unlink()

    return True, "File deleted successfully."


def get_files():
    return list(BASE_DIR.iterdir())