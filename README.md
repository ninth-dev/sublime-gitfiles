# GitFiles

A sublime plugin to easily open the changed files based on `git status` and navigate the modifications made across the codebase.

![git status example](images/git-status-example.png)

## Installation

- Open the command palette with `CMD + SHIFT + P`
- Select `Package Control: Add Repository`
- Paste in : https://github.com/ninth-dev/sublime-gitfiles
- Open the command palette again with `CMD + SHIFT + P`
- Select `Package Control: Install Package`
- Choose `sublime-gitfiles`


## Usage

### Goto

Using **GitFiles: Goto** command, you can go to the modified and untracked files.

![GitFiles: Goto](images/git-files-goto-command.png)

### Open Files

Using **GitFiles: Open Files** command, you can open all the modified and untracked files.

![GitFiles: Open Files results](images/git-files-opened-files.png)


### Move through modifications

To navigate through the modifications, set up the key bindings.

For example,

```json
[
  { "keys": ["super+."], "command": "git_files_next_modification" },
  { "keys": ["super+,"], "command": "git_files_prev_modification" },
]
```

The difference between Sublime Text's native `next_modification` / `prev_modification` and this plugin's is that it can
navigate to the next/prev modifications across changed files.

