import os
import shutil

def avatar_path(instance, filename):
    profile = instance.user.username
    return f'avatars/{profile}/{filename}'

def avatar_delete_path(image):
    path = os.path.abspath(os.path.join(image.path, '..'))
    shutil.rmtree(path)

def document_path(instance, filename):
    project = instance.block.project.name
    block = instance.block.name
    return f'projects/{project}/{block}/{filename}'
