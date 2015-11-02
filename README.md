
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
root: '~'      # Do not put the last slash ('/')

windows:
- Musics    : musics
- Downloads : downloads

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

# YAML Syntax for IniTmux

It is very simple. A YAML IniTmux file has up to 4 main attributes:

### name (String)

```yaml
name: <SessionName>
```

Is the name of the session. This attribute is obligatory. 

### root (String)

```yaml
root: <RootDirectory>
```

Is the directory root of all windows. This attribute is optional. If defined, its value will be concatenated 
before the `dir`, which will be explained soon.

Note: If you want to refer to `~`, please use `'~'` or `"~"` not only `~`. This symbol will be expanded to the 
HOME location of the user who called the script. It uses `os.path.expanduser` of `os` python module.

### models

Is a sort of skeleton that you want to put into your windows description. You can then describe a model that 
can be applyed to several windows at once.

You can see the power of the `models` attribute, in the following example:

* `~/.config/IniTmux/Packagers.yml`
```yaml
---
name: Packagers
windows:
- Pacman : two
- Yaourt : two
- npm    : two
- gem    : two
- pip    : two
models:
    two:
        layout: even-horizontal
        panes: 2
```

with this configuration, IniTmux will create a session called `Packagers` with 5 windows. In each window, 
IniTmux will apply the model called `two`, which will create 2 (`two`) panes without commands. 

You can also see that both `root` and `dir` attributes wasn't written. In this case, IniTmux will change 
directory to HOME (`~`).


### windows 

Is the list of window names, model names and possible specific directory for all the panes of that window. This 
attribute is obligatory. 


There is 4 ways to describe a window.

###### Direct Form

In this form, you describe the window without using any model. Example:

```yaml
windows:
- Directories:
    layout: tiled
    panes: 
    - cd
    - cd /
    - cd /usr
    - cd /boot
```

this will create 1 window called `Directories` with 4 panes.

###### Model Form

In this form, you describe a set of models and apply then in each window. Example:

```yaml
windows:
- Torrents: two
- Downloads: two
- Documents: three
models:
    three:
        layout: even-horizontal
        dir: <WindowName>
        panes: 3
    two:
        layout: even-horizontal
        dir: <WindowName>
        panes: 2
```

###### Overwrite Model Form

In this form, you describe a set of models and apply then in each window, but you can 
overwrite one or more attibutes of a model if you want. Example:

```yaml
windows:
- Library1: 
    layout : tiled
    model  : two

- Library2: 
    model  : two
    dir    : ''
    layout : tiled

models:
    three:
        layout: even-horizontal
        dir: <WindowName>
        panes: 3
    two:
        layout: even-horizontal
        dir: <WindowName>
        panes: 2
```

Note:
    Until this moment, you cannot overwrite the `panes` attribute yet. This part of the 
    code (or even the entire code) was written with hurry, and still lacks of organization. With time, I'll take 
    care of this feature.

###### Yes, you can mix all these forms together when describing windows

Example:

```yaml
---
name: Test
root: '~'
windows:
- Directories:      # Direct Form
    layout: tiled
    panes: 
    - cd
    - cd /
    - cd /usr
    - cd /boot

- Library: three    # Model Form

- Books:            # Overwrite Form
    model: two
    dir: 'Documents/Livros'
    layout: tiled

models:
    three:
        layout: even-horizontal
        dir: <WindowName>
        panes: 3
    two:
        layout: even-horizontal
        dir: <WindowName>
        panes: 2
```

# Panes Description

You can describe panes in 3 different forms:

###### Number form

You are only interested in create a number of panes and apply no commands. Example:

```yaml
models:
    three:
        layout: even-horizontal
        dir: <WindowName>
        panes: 3

    two:
        layout: even-horizontal
        dir: <WindowName>
        panes: 2

    four:
        layout: even-horizontal
        dir: <WindowName>
        panes: 4
```

###### One Command Form

You want to create several panes and apply a command after its creation. Example:

```yaml
    three:
        layout: "40fd,113x31,0,0[113x22,0,0{22x22,0,0,0,90x22,23,0,1},113x9,0,23,2]"
        dir: <WName>
        panes:
        - loop "tree obj" 0.5
        - vim -c LoadWorkSpace
        - ''
```

###### Multiple Commands Form

You want to create several panes and apply several commands, in sequence, for each pane. Example:

```yaml
models:
    three:
        layout: even-horizontal
        dir: <WindowName>
        panes: 3
    two:
        layout: even-horizontal
        dir: <WindowName>
        panes: 
            - ListDirs: # Multiple commands. The pane's name is irrelevant, but not optional
                - cd ~
                - ls
                - cd /
                - ls
                - cd /usr
                - ls
                - cd /boot
                - ls
            - ranger
            - df -h
```

as you can see, you can mix `One Command` and `Multiple Command` Forms together.

# IniTmux Wildcards

To support the `models` feature, I had to implement some sort of wildcards, so I can 
reference inside the model something about the window or the session names. In another 
private project, I'm using git with feature branch workflow. Each feature has its own 
branch such as its own directory as well. The directory structure of the `Math` main 
branch is the following.

```text
$ tree -L 1 -d /i/project/LibAK/feature/Math
.
├── Bool
├── branch
├── Complex
├── Integer
├── Matrix
├── Number
├── Real
└── Vector
```

All of that directories, except `branch`, has a lot in common when creating windows for each one of them.

1. The name of the directory will be the name of the window;
2. All windows will share the same layout;
3. All windows will have the same panes structure.

For the `branch` directory, I like to make specific description about the window creation. 

So, to acompplish this, and take advantage of the similarities, I've created the following YAML file.

* samples/AK-MATH.yml

```yaml
---
name: AK-Math 
root: /i/project/LibAK/feature/Math
windows:
- Matrix  : feature
- Vector  : feature
- Number  : feature
- Complex : feature
- Real    : feature
- Integer : feature
- Bool    : feature

- Math:
    layout : tiled
    dir    : branch
    panes  :
    - 'ranger'
    - ''

models:
    feature:
        layout: "40fd,113x31,0,0[113x22,0,0{22x22,0,0,0,90x22,23,0,1},113x9,0,23,2]"
        dir: <WName>
        panes:
        - loop "tree obj" 0.5
        - vim -c VWSLoadWorkSpace
        - ''
```

in this case, I have just one model (`feature`). You can see that `dir` attribute has the `<WName>`
wildcard, that will be expanded to the name of the window that "call" the model `feature`. And, you 
can also see that I've described specific settings for the `Math` window, once it has specific requirements.

### List of Possible Wildcards

A wildcard can be used inside any of the following attibutes: `root` and  `dir`.

Each wildcard must be written inside `<` and `>`. What will be inside can vary as follows:

1. `wname`, `winname`, `windname`, and `windowname`. Example:

all of these wildcards will be expaded to the window name.

```text
    dir: 'feature/<WindName>'
```

2. `sname`, `sesname`, `sessname`, and `sessionname`. Example:

all of these wildcards will be expaded to the sessin name.

```text
    root: '~/<SessionName>'
    dir : 'feature/<SName>/trash/<WName>'
```

you can write a wildcard ignoring the case of the letters. This can be done thanks to thPython's regex module. 
In the code, the pattern variables for these wildcards are:

```python
WPattern = r"<(?i)(windown|wn|winn|windn)ame>"
SPattern = r"<(?i)(sessionn|sn|sesn|sessn)ame>"
```

and they are used only inside the function `CreatePanes`. So, if you want to change them, please let me know.

# Related Projects

If IniTmux does not suit you needs, then you can checkout these projects:

[Tmuxinator](https://github.com/tmuxinator/tmuxinator)

# Dependencies

###### pyyaml

I strongly recommend you to install it with pip.

    $sudo pip install pyyaml

* Others Modules

```text
    os
    pprint
    subprocess
```

# TODO

I'm now trying to implement reload operations.
