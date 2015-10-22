
import os
from pprint import pprint
from subprocess import getoutput as system
from subprocess import call
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def NewSession(SName):
    return call('tmux new-session -s '+SName+' -d',shell=True)


def NewWindow(SName,WName,WNumber):
    if WNumber > 0:
        return call('tmux new-window -n '+WName+' -t '+SName,shell=True)
    else:
        return call('tmux rename-window -t '+SName+':0 '+WName,shell=True)

def NewPane(SName,WNumber,PNumber,Command,Directory):
    ret = True
    if PNumber > 0:
        ret = call('tmux split-window -h -t '+SName+':'+str(WNumber),shell=True)
        ChangeDir(SName,WNumber,PNumber,Directory)
        ApplyCommand(SName,WNumber,PNumber,Command)

    else:
        ChangeDir(SName,WNumber,PNumber,Directory)
        ApplyCommand(SName,WNumber,PNumber,Command)

    return ret


def ChangeDir(SName,WNumber,PNumber,Directory):
    return call(
            'tmux send-keys -t '+
            SName+':'+str(WNumber)+'.'+str(PNumber)+
            ' "cd '+Directory+'" C-m',shell=True)

def ApplyCommand(SName,WNumber,PNumber,Command):
    return call(
            'tmux send-keys -t '+
            SName+':'+str(WNumber)+'.'+str(PNumber)+' '+
            Command+' C-m',shell=True)

def SetLayout(SName,WNumber,Layout):
    return call('tmux select-layout -t '+SName+':'+str(WNumber)+' '+Layout,shell=True)


def SaveSessions(File):
    pass

def LoadSessions(File):
    # Load YAML File as Python Object
    Stream = open(File,'r')
    Sessions = load(Stream)
    Stream.close()
    SNumber = 0


    call('clear',shell=True)
    print()
    print()

    for Session in Sessions:
        for SName in Session.keys():
            Session = Session[SName]
            Root = Session.get('root')
            Windows = Session.get('windows')
            WNumber = 0

            ThereIsSession = NewSession(SName)

            if not ThereIsSession:
                print('--> Session: '+SName+' [...]')
                for Window in Windows:
                    for WName in Window:
                        Window = Window[WName]
                        Panes  = Window.get('panes')
                        Layout = Window.get('layout')
                        Dir    = Window.get('dir')
                        PNumber = 0

                        ThereIsWindow = NewWindow(SName,WName,WNumber)

                        if not ThereIsWindow:
                            
                            for Pane in Panes:
                                Command = Pane
                                Directory = Root+'/'+Dir
                                NewPane(SName,WNumber,PNumber,Command,Directory)
                                PNumber += 1

                        SetLayout(SName,WNumber,Layout)
                        
                    WNumber += 1

        SNumber += 1
                    
File = os.path.expanduser('~/.config/IniTmux/IniTmux.yml')

LoadSessions(File)
