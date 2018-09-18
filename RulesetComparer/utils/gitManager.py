from git import Repo
from RulesetComparer.utils.timeManager import compare_commit_time
from django.conf import settings
from RulesetComparer.properties import errorMessage


class GitManager:

    STATUS_NEED_PULL = 0
    STATUS_NEED_PUSH = 1
    STATUS_NO_CHANGED = 2

    def __init__(self, path):
        self.REPOSITORY_PATH = path
        self.status = None
        self.check_repository_status()

    def _repo(self):
        repo_path = self.REPOSITORY_PATH
        repo = Repo(repo_path)
        assert repo, errorMessage.GIT_NO_REPO_MSG
        return repo

    def _remote_repo(self):
        repo = self._repo()
        remote = repo.remote(settings.GIT_REMOTE_NAME)
        assert remote, errorMessage.GIT_NO_REMOTE_REPOSITORY
        return remote

    def pull(self):
        print("pull code from remote")
        self._remote_repo().pull()
        self.check_repository_status()

    def update(self):
        pass

    def check_repository_status(self):
        repo = self._repo()
        remote_repo = self._remote_repo()

        # local last commit
        local_commit = repo.commit()
        # remote last commit
        remote_commit = remote_repo.fetch()[0].commit

        print_commit(local_commit, "local")
        print_commit(remote_commit, "remote")
        print("\ncompare local and remote commit time ...")
        local_commit_time = str(local_commit.authored_datetime)
        remote_commit_time = str(remote_commit.authored_datetime)

        return_time = compare_commit_time(local_commit_time, remote_commit_time)

        if return_time == local_commit_time:
            self.status = self.STATUS_NEED_PUSH
            print("compare result : need push code")
        elif return_time == remote_commit_time:
            self.status = self.STATUS_NEED_PULL
            print("compare result : need pull code")
        else:
            self.status = self.STATUS_NO_CHANGED
            print("compare result : nothing change")


def print_commit(commit, env):
    print('\n----', env, '----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str("authored_datetime:{}".format(commit.authored_datetime)))

