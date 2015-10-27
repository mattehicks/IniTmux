
# What is This Program?

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

# Dependencies

* pyyaml

I strongly recommend you to install it with pip.

    $sudo pip install pyyaml

* Others Modules

- os
- pprint
- subprocess
