from git import Repo
from RulesetComparer.utils.timeManager import compare_commit_time
from django.conf import settings
from RulesetComparer.properties import errorMessage


class GitManager:

    STATUS_NEED_PULL = 0
    STATUS_NEED_PUSH = 1
    STATUS_NO_CHANGED = 2

    def __init__(self, path, branch):
        self.REPOSITORY_PATH = path
        self.branch = branch
        self.status = None
        self.check_branch_status()
        self.check_commit_status()

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
        self.check_commit_status()

    def update(self):
        pass

    def check_commit_status(self):
        repo = self._repo()
        remote_repo = self._remote_repo()

        # local last commit
        local_commit = repo.commit()
        # remote last commit
        remote_commit = remote_repo.fetch()[0].commit

        print_commit(local_commit, "local latest commit")
        print_commit(remote_commit, "remote latest commit")
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

    def check_branch_status(self):
        repo = self._repo()
        remote_repo = self._remote_repo()
        print("---- check branch status ----")
        print("local setting branch is {}".format(self.branch))
        print("current active branch is {}".format(repo.active_branch))
        if repo.active_branch.name == self.branch:
            print("setting branch equals active branch, no need to check out")
            return

        print("setting branch different with active branch, check out branch")
        repo.create_head(self.branch, remote_repo.refs[self.branch])
        current_branch_index = self.get_current_branch_index()
        remote_branch_index = self.get_remote_branch_index()
        print("set current tracking branch to {}".format(remote_repo.refs[remote_branch_index]))
        repo.heads[current_branch_index].set_tracking_branch(remote_repo.refs[remote_branch_index])
        repo.heads[current_branch_index].checkout()

        print("current active branch is {}".format(repo.active_branch))

    def get_current_branch_index(self):
        repo = self._repo()
        i = 0
        for head in repo.refs:
            if head.name == self.branch:
                return i
            i = i+1
        return i

    def get_remote_branch_index(self):
        repo = self._remote_repo()
        i = 0
        find_branch = settings.GIT_REMOTE_NAME + "/" + self.branch
        for head in repo.refs:
            if head.name == find_branch:
                return i
            i = i + 1
        return i


def print_commit(commit, env):
    print('\n----', env, '----')
    print(str(commit.hexsha))
    print("\"{}\" by {} ({})".format(commit.summary,
                                     commit.author.name,
                                     commit.author.email))
    print(str("authored_datetime:{}".format(commit.authored_datetime)))

