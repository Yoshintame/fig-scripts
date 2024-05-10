import argparse
import re
import subprocess

WIP_MESSAGE = "WIP: don't push this!"

def get_branches_list():
  branches_output = subprocess.check_output(['git', 'branch'])

  branches = branches_output.decode().splitlines()

  # Remove the '*' character from the current branch
  branches = [branch.replace('*', '').strip() for branch in branches]

  return branches


def get_current_branch():
  get_current_branch_command = ["git", "branch", "--show-current"]
  current_branch = subprocess.check_output(get_current_branch_command, text=True).strip()

  return current_branch


def get_status():
  status_command = ['git', 'status', '--porcelain']
  status = subprocess.check_output(status_command, text=True).strip()

  return status


def create_wip_commit():
  status = get_status()

  if not status: return

  add_command = ['git', 'add', '.']
  commit_command = ['git', 'commit', '--no-verify', '-m', WIP_MESSAGE]

  subprocess.run(add_command, check=True, stdout=subprocess.DEVNULL)
  subprocess.run(commit_command, check=True, stdout=subprocess.DEVNULL)


def check_if_last_commit_was_wip():
  command = ['git', 'log', '-1', '--format="%H - %s"']

  last_commit_output = subprocess.check_output(command, text=True)
  commit_hash, commit_message = last_commit_output.split(" - ", 1)

  if "WIP" in commit_message:
    return commit_hash

  return None


def revert_commit():
  reset_command = ['git', 'reset', 'HEAD~1']
  subprocess.run(reset_command, check=True)


def create_or_switch_branch(branch, branches):
  if branch not in branches:
    subprocess.check_output(["git", "branch", fig.inputs.branch])

  subprocess.check_output(["git", "switch", fig.inputs.branch])
  wip_commit = check_if_last_commit_was_wip()

  if wip_commit:
    revert_commit()


branches = get_branches_list()
current_branch = get_current_branch()
create_wip_commit()
create_or_switch_branch(fig.inputs.branch, branches)
