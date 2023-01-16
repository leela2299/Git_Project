from git import Repo
import datetime
import argparse

class GitRepo:

    def __init__(self,repo_path):
        self.repo = Repo(repo_path)

    def get_active_branch(self):
        return self.repo.active_branch.name
        
    
    def is_modified(self):
        # returns true if the repository files are modified and uncommited 
        changed = [item.a_path for item in self.repo.index.diff(None)]
        return len(changed)>0

    def is_head_commit_last_week(self):

        curr_time = datetime.datetime.now()
        last_commit_time = (datetime.datetime.fromtimestamp(self.repo.head.object.authored_date))
        diff = (curr_time - last_commit_time).days
        return diff<=7

    def is_head_commit_by_Rufus(self):
        
        author = str(self.repo.head.object.author)
        return author == "Rufus"


parser = argparse.ArgumentParser(description ='Print Specific Facts about the Local Git Directory')
parser.add_argument('--git_dir', type=str, required=True, metavar='', help='path of the local git directory')
args = parser.parse_args()
git_dir = args.git_dir




repo = GitRepo(git_dir)
print("active branch : ",repo.get_active_branch())
print("local changes: ",repo.is_modified())
print("recent_commit : ",repo.is_head_commit_last_week())
print("blame Rufus : ",repo.is_head_commit_by_Rufus())
