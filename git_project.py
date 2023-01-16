from git import Repo, InvalidGitRepositoryError, NoSuchPathError, CacheError
import datetime
import argparse
import sys

class GitRepo:

    def __init__(self):
        try:
            self.repo = Repo(self.get_path())
        except InvalidGitRepositoryError:
            print("Invalid Git Repository")
            sys.exit(1)
        except NoSuchPathError:
            print("Invalid path to Git Directory")
            sys.exit(1)

    def get_path(self):
        parser = argparse.ArgumentParser(description ='Prints Specific Facts about the Local Git Directory')
        parser.add_argument('--git_dir', type=str, required=True, metavar='', help='path of the local git directory')
        args = parser.parse_args()
        git_dir = args.git_dir
        return git_dir
        
    def get_active_branch(self):
        return self.repo.active_branch.name 
        
    def is_modified(self):
        # Returns true if the modified repository files are uncommited
        try:
            staged = [item.a_path for item in self.repo.index.diff('Head')]
            unstaged = [item.a_path for item in self.repo.index.diff(None)]
            return len(staged)>0 or len(unstaged)>0
        except CacheError:
            print("Git Index error")
            sys.exit(1)

    def is_head_commit_with_in_days(self, days = 7):
        curr_time = datetime.datetime.now()
        last_commit_time = (datetime.datetime.fromtimestamp(self.repo.head.object.authored_date))
        diff = (curr_time - last_commit_time).days
        return diff<=days

    def is_head_commit_by_user(self, user="Rufus"):
        author = str(self.repo.head.object.author)
        return author == user

    def display_details(self):
        print("active branch: ",self.get_active_branch())
        print("local changes: ",self.is_modified())
        print("recent_commit: ",self.is_head_commit_with_in_days())
        print("blame Rufus: ",self.is_head_commit_by_user())



if __name__ == "__main__":
    repo = GitRepo()
    repo.display_details()
