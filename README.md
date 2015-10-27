
# What This Program is?

This is just a session store/initializer for Tmux.

# How It Works?

It's simple. All you have to do is plan your sessions into YAML files, put 
then into `~/.config/IniTmux` and execute a single python script `src/main.py`.

# How Do I Plan My Sessions?

Let's say that you want to acompplish the following workspace:

```text
     Session: Files

     Window: Musics
     Layout: even-vertical
     +-------------------+-------------------+
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |      mocp .       |      ranger       |
     |   (~/Musics)      |    (~/Musics)     |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     |                   |                   |
     +-------------------+-------------------+

     Window: Downloads
     Layout: even-horizontal
     +---------------------------------------+
     |                                       |
     |               ranger                  |
     |            (~/Downloads)              |
     |                                       |
     |                                       |
     |                                       |
     +---------------------------------------+
     |                                       |
     |            watch du -sh .             |
     |            (~/Downloads)              |
     |                                       |
     |                                       |
     |                                       |
     +---------------------------------------+
```

So, this figure suggests that you want to create a session called `Files`, where 
this session has two windows called `Musics` and `Downloads`, respectively. Whithin
the window `Musics`, you want two panes. The first one will execute `mocp .` and the 
second one will execute the file manager `ranger`, and both panes will be organized 
under layout `even-vertical`. For the second window, the thinking is analogous.

Hence, you have to write the YAML file (`Files.yml`) like the following:

```yaml
---
name: Files
root: ~      # Do not put the last slash ('/')

windows:
- [Musics    , musics]
- [Downloads , downloads]

models:
    musics:
        layout: even-vertical
        dir: <WindowName> 
        panes:
        - mocp .
        - ranger
    downloads:
        layout: even-horizontal
        dir: <WindowName> 
        panes:
        - ranger
        - watch du -sh .
```

# What this 'models' attribute is?

You can see the power of the `models` attribute, in the following example:

* `~/.config/IniTmux/Packagers.yml`
```yaml
---
name: Packagers
windows:
- [Pacman , two]
- [Yaourt , two]
- [npm    , two]
- [gem    , two]
- [pip    , two]
models:
    two:
        layout: even-horizontal
        panes: 2
```

with this configuration, IniTmux will create a session called `Packagers` with 5 windows. In each window, 
IniTmux will apply the model called `two`, which will create 2 (`two`) panes without commands. 

You can also see that both `root` and `dir` attributes wasn't written. In this case, IniTmux will change 
directory to HOME (`~`).

# YAML Syntax for IniTmux

It is very simple. A YAML IniTmux file has up to 4 main attributes:

### name or Name (String)

```yaml
name: <SessionName>
```

Is the name of the session. This attribute is obligatory. 

### root or Root (String)

```yaml
root: <RootDirectory>
```

Is the directory root of all windows. This attribute is optional. If defined, its value will be concatenated 
before the `dir`, which will be explained soon.

Note: If you want to refer to `~`, please use `'~'` or `"~"` not only `~`. This symbol will be expanded to the 
HOME location of the user who called the script. It uses `os.path.expanduser` of `os` python module.

### models or Models

TODO ...

### windows or Windows (List of lists: [[],[],...,[]])

Is the list of window names, model names and possible specific directory for all the panes of that window. This 
attribute is obligatory. The skeleton is like the following:

```yaml
windows: 
- [WindowName1,ModelName1 [,SpecificDir1]]
# ...
- [WindowNameN,ModelNameN [,SpecificDirN]]
```

The two first items of each window are mandatory. The third one is not. If setted, its value will overwrite the 
`dir` attribute of the choosen model.

Example:

```yaml
---
name: Test
root: '~/<SessionName>'
windows:
- [Downloads , two]
- [Documents , two]
- [Torrents  , two  , 'Downloads/<WindName>']    # <WindName> == 'Torrents'
- [Books     , two  , 'Downloads/<WindowName>']  # <WindowName> == 'Books'

models:
    two:
        layout: even-horizontal
        dir: <WindowName>
        panes:
            - first:
                - cd /i/server/http/<SName>/<WName>
                - ranger
            - df -h
```

So, this YAML file will create 4 windows. IniTmux will apply the model called `two` for each window. This model
tells that the layout of each window will be `even-horizontal`. The full path of each window is little bit tricky,
but it will follow the following rules:

1) If SpecificDir is setted in some window, then `PATH = root+'/'+SpecificDir`. Exemple:
    
```text
    Window: Torrents
    PATH  : ~/Test/Downloads/Torrents
```

Note that `<SessionName>` and `<WindName>` were properly expanded.

2) Else if SpecificDir isn't setted, then `PATH = root+'/'+dir`. Example:

```text
    Window: Documents
    PATH  : ~/Test/Documents
```

In both cases, each window will have two panes. The first pane will first enter the location `/i/server/http/<SName>/<WName>`
after proper expansions of `SName` and `WName`, and then execute `ranger`. The second pane will apply `df -h`.

Once you can create panes with multiple commands (sequencially executed), you can use this approach to first enter some "Pane Specific"
directory location that will overwrite all PATHs setted before.


# Dependencies

* pyyaml

I strongly recommend you to install it with pip.

    $sudo pip install pyyaml

* Others Modules

```text
    os
    pprint
    subprocess
```
Test
