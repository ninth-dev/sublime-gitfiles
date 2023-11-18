# GitFiles

A sublime plugin to easily open the changed files based on `git status` and navigate the modifications made across the codebase.

For example:

![git status example](images/git-status-example.png)

Using **GitFiles: Goto** command, you can goto the modified and untracked files.

![GitFiles: Goto](images/git-files-goto-command.png)

Using **GitFiles: Open Files** command, you can open all the modified and untracked files.

![GitFiles: Open Files results](images/git-files-opened-files.png)

To navigate through the modifications, set up the key bindings.

For example,

```json
[
  { "keys": ["super+."], "command": "git_files_next_modification" },
  { "keys": ["super+,"], "command": "git_files_prev_modification" },
]
```

The difference between sublime's native `next_modification` / `prev_modification` and this plugin's is that it can navigate to the next/prev changed file.

