import logging
import os
import shutil
from pathlib import Path
from git import Repo

def clone_repo(repo_url: str, clone_dir="repo_clone"):
    try:
        if os.path.exists(clone_dir):
            logging.info(f"Removing existing directory: {clone_dir}")
            try:
                shutil.rmtree(clone_dir, onerror=handle_remove_readonly)
            except Exception as e:
                logging.error(f"Failed to remove directory: {e}")
                try:
                    backup_dir = f"{clone_dir}_old"
                    if os.path.exists(backup_dir):
                        shutil.rmtree(backup_dir)
                    os.rename(clone_dir, backup_dir)
                    shutil.rmtree(backup_dir)
                except Exception as e2:
                    logging.error(f"Alternative removal also failed: {e2}")
                    raise
        
        logging.info(f"Cloning repository: {repo_url}")
        Repo.clone_from(repo_url, clone_dir)
        return clone_dir
    except Exception as e:
        logging.error(f"Repository cloning failed: {e}")
        raise

def handle_remove_readonly(func, path, exc):
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise
    
def remove_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory, onerror=handle_remove_readonly)
        logging.info(f"Removed existing directory: {directory}")
    else:
        logging.info(f"Directory does not exist: {directory}")
