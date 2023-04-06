import os
import platform
import subprocess


def hide_file(repo_dir):
    """Esconde o diretório do repositório local, para não haver conflito com outros repositórios."""
    if os.path.isdir(repo_dir):
        if platform.system() == 'Windows':
            subprocess.run(['cmd', '/c', 'rd', '/s', '/q', repo_dir], shell=True)
        else:
            subprocess.run(['rm', '-rf', repo_dir])
    return repo_dir
