import argparse
import re
import subprocess

# Execute 'git branch' command
branches_output = subprocess.check_output(['git', 'branch'])

# Decode the output and split it into lines
branches = branches_output.decode().splitlines()

# Remove the '*' character from the current branch
branches = [branch.replace('*', '').strip() for branch in branches]


current_branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()

# try to stash the current state setting a parseable message with the branch
subprocess.check_output(["git", "stash", "-u", "--message", f"[smart switch] {current_branch}"], text=True)


if fig.inputs.branch not in branches:
  subprocess.check_output(["git", "branch", fig.inputs.branch])

# switch
subprocess.check_output(["git", "switch", fig.inputs.branch])


# this is the same than args.branch but also expand references like "-"
target_branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()

# list stashes to find if there is something to pop
stashes_list = subprocess.check_output(["git", "stash", "list"], text=True)
stashes = {branch_name: stash_index for (stash_index, branch_name) in re.findall(r"stash@\{(\d+)\}\: .*: \[smart switch\] (.*)", stashes_list)}

stash_index = stashes.get(target_branch)

if stash_index is not None:
    subprocess.check_output(["git", "stash", "pop", "--index", stash_index])rgit-smart-switch-stash
