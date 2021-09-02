from git import Repo, GitCommandError
from datetime import datetime


def build_repository_path(repository: str, base_path: str):
    repo_name = repository.split("/")[-1]
    return "{}/{}_{}".format(base_path, repo_name,
                             datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))


def clone_repository(**kwargs: dict):
    path = kwargs.get('path', './')
    repository = kwargs.get('repository')
    branch = kwargs.get('branch')
    try:
        cloned_repo = Repo.clone_from(repository, path)
        if branch is not None:
            cloned_repo.git.checkout(branch)
        return None
    except (GitCommandError, Exception) as error:
        return error
