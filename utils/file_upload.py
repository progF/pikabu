import os
import shutil


def avatar_path(instance, filename):
    profile = instance.user.username
    return 'avatars/{}/{}'.format(profile, filename)


def avatar_delete_path(image):
    path = os.path.abspath(os.path.join(image.path, '..'))
    shutil.rmtree(path)


def document_path(instance, filename):
    project = instance.block.project.name
    block = instance.block.name
    return 'projects/{}/{}/{}'.format(project, block, filename)
