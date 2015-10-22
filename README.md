
# Syntax

```yaml
- SessionName1:
    root: /path/to/project/root     # Without last '/'
    windows:
        - WindowName1:
            layout: tiled           # One of tmux layouts
            dir: <subdir>           # It'll be prefixed with root
            panes:
                - cmd1
                - cmd2
                - cmd3
        - WindowName2:
            layout: tiled           # One of tmux layouts
            dir: <subdir>           # It'll be prefixed with root
            panes:
                - cmd1
                - ''                # Do nothing
                - cmd3
- SessionName2:
    root: /path/to/project/root     # Without last '/'
    windows:
        - WindowName1:
            layout: tiled           # One of tmux layouts
            dir: <subdir>           # It'll be prefixed with root
            panes:
                - cmd1
                - cmd2
                - cmd3
        - WindowName2:
            layout: tiled           # One of tmux layouts
            dir: <subdir>           # It'll be prefixed with root
            panes:
                - cmd1
                - ''                # Do nothing
                - cmd3

```
and so on.

# Directory Location

The hole system is just one file (`src/main.py`). You have to put your YAML file inside `~/config/IniTmux/IniTmux.yml`.
But, you can change this directly in the last lines of `src/main.py`. 

Just remeber that sessions and windows have names, but panes don't.

# Dependencies

* pyyaml

I strongly recommend you to install it with pip.

    $sudo pip install pyyaml

* Others Modules

os
pprint
subprocess
