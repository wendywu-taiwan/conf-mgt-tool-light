from git import Repo
from RulesetComparer.utils.timeUtil import compare_git_time
from common.data_object.error.message import GIT_NO_REPO_MSG, GIT_NO_REMOTE_REPOSITORY
from RulesetComparer.utils.logger import *
import traceback


class GitManager:
    STATUS_NEED_PULL = 0
    STATUS_NEED_PUSH = 1
    STATUS_NO_CHANGED = 2
    LOG_CLASS = "GitManager"

    def __init__(self, path, branch):
        info_log(self.LOG_CLASS, " init, path :" + str(path) + " ,branch :" + str(branch))
        self.REPOSITORY_PATH = path
        self.branch = branch
        self.status = None
        self.check_branch_status()
        self.check_commit_status()

    def _repo(self):
        repo_path = self.REPOSITORY_PATH
        repo = Repo(repo_path)
        assert repo, GIT_NO_REPO_MSG
        return repo

    def _remote_repo(self):
        repo = self._repo()
        remote = repo.remote(settings.GIT_REMOTE_NAME)
        assert remote, GIT_NO_REMOTE_REPOSITORY
        return remote

    def pull(self):
        info_log(self.LOG_CLASS, "pull code from remote")
        self._remote_repo().pull()
        self.check_commit_status()

    def update(self):
        pass

    def check_commit_status(self):
        try:
            repo = self._repo()
            remote_repo = self._remote_repo()

            # local last commit
            local_commit = repo.commit()
            # remote last commit
            remote_commit = remote_repo.fetch()[0].commit

            print_commit(local_commit, "local latest commit")
            print_commit(remote_commit, "remote latest commit")
            info_log(self.LOG_CLASS, "\ncompare local and remote commit time ...")
            local_commit_time = str(local_commit.authored_datetime)
            remote_commit_time = str(remote_commit.authored_datetime)

            return_time = compare_git_time(local_commit_time, remote_commit_time)

            if return_time == local_commit_time:
                self.status = self.STATUS_NEED_PUSH
                info_log(self.LOG_CLASS, "compare result : need push code")
            elif return_time == remote_commit_time:
                self.status = self.STATUS_NEED_PULL
                info_log(self.LOG_CLASS, "compare result : need pull code")
            else:
                self.status = self.STATUS_NO_CHANGED
                info_log(self.LOG_CLASS, "compare result : nothing change")
        except Exception as e:
            raise e

    def check_branch_status(self):
        try:
            repo = self._repo()
            remote_repo = self._remote_repo()
            info_log(self.LOG_CLASS, "---- check branch status ----")
            info_log(self.LOG_CLASS, "local setting branch is {}".format(self.branch))
            info_log(self.LOG_CLASS, "current active branch is {}".format(repo.active_branch))
            if repo.active_branch.name == self.branch:
                info_log(self.LOG_CLASS, "setting branch equals active branch, no need to check out")
                return

            info_log(self.LOG_CLASS, "setting branch different with active branch, check out branch")
            repo.create_head(self.branch, remote_repo.refs[self.branch])
            current_branch_index = self.get_current_branch_index()
            remote_branch_index = self.get_remote_branch_index()

            info_log(self.LOG_CLASS, "set current tracking branch to {}".format(remote_repo.refs[remote_branch_index]))
            repo.heads[current_branch_index].set_tracking_branch(remote_repo.refs[remote_branch_index])
            repo.heads[current_branch_index].checkout()

            info_log(self.LOG_CLASS, "current active branch is {}".format(repo.active_branch))
        except Exception as e:
            error_log(traceback.format_exc())
            raise e

    def get_current_branch_index(self):
        repo = self._repo()
        i = 0
        for head in repo.refs:
            if head.name == self.branch:
                return i
            i = i + 1
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
