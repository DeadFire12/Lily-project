import os
import subprocess
import ctypes
import shutil


# =========================================================
# OPEN FILE OR FOLDER
# =========================================================

def open_path(path):

    path = os.path.expanduser(path)

    if not os.path.exists(path):

        return {
            "success": False,
            "error": "Path does not exist."
        }

    try:

        os.startfile(path)

        return {
            "success": True,
            "path": path
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# CREATE TEXT FILE
# =========================================================

def create_text_file(path, content=""):

    path = os.path.expanduser(path)

    try:

        folder = os.path.dirname(path)

        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        return {
            "success": True,
            "path": path
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# READ TEXT FILE
# =========================================================

def read_text_file(path):

    path = os.path.expanduser(path)

    if not os.path.exists(path):

        return {
            "success": False,
            "error": "File does not exist."
        }

    if not os.path.isfile(path):

        return {
            "success": False,
            "error": "That path is not a file."
        }

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        return {
            "success": True,
            "path": path,
            "content": content
        }

    except UnicodeDecodeError:

        return {
            "success": False,
            "error": "This does not appear to be a UTF-8 text file."
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# WRITE TEXT FILE
# =========================================================

def write_text_file(path, content):

    path = os.path.expanduser(path)

    if not os.path.exists(path):

        return {
            "success": False,
            "error": "File does not exist."
        }

    try:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        return {
            "success": True,
            "path": path
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# DELETE
# =========================================================

def delete_path(path):

    path = os.path.expanduser(path)

    if not os.path.exists(path):

        return {
            "success": False,
            "error": "Path does not exist."
        }

    # Safety:
    # The actual deletion is NOT performed here.
    # Lily must explicitly confirm first.

    return {
        "success": False,
        "confirmation_required": True,
        "path": path,
        "message": "This action requires confirmation."
    }


# =========================================================
# LOCK COMPUTER
# =========================================================

def lock_computer():

    try:

        ctypes.windll.user32.LockWorkStation()

        return {
            "success": True
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# RESTART COMPUTER
# =========================================================

def restart_computer():

    return {
        "success": False,
        "confirmation_required": True,
        "action": "restart",
        "message": "Restart requires confirmation."
    }


# =========================================================
# SHUTDOWN COMPUTER
# =========================================================

def shutdown_computer():

    return {
        "success": False,
        "confirmation_required": True,
        "action": "shutdown",
        "message": "Shutdown requires confirmation."
    }


# =========================================================
# FOLDER SIZE
# =========================================================

def get_folder_size(folder):

    folder = os.path.expanduser(folder)

    if not os.path.exists(folder):

        return {
            "success": False,
            "error": "Folder does not exist."
        }

    if not os.path.isdir(folder):

        return {
            "success": False,
            "error": "That path is not a folder."
        }

    total = 0

    try:

        for root, directories, files in os.walk(folder):

            for filename in files:

                path = os.path.join(
                    root,
                    filename
                )

                try:

                    total += os.path.getsize(path)

                except (
                    OSError,
                    PermissionError
                ):

                    pass

        return {
            "success": True,
            "folder": folder,
            "bytes": total,
            "mb": round(
                total / (1024 * 1024),
                2
            ),
            "gb": round(
                total / (1024 * 1024 * 1024),
                2
            )
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }