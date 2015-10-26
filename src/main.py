#!/usr/bin/env python

import os
import re
from pprint import pprint
from subprocess import getoutput as system
from subprocess import call
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Tmux Functions
def NewSession(SName): #{{{
    return call('tmux new-session -s '+re.escape(SName)+' -d',shell=True)


#}}}
def NewWindow(SName,WName,WNumber): #{{{
    if WNumber > 0:
        return call('tmux new-window -n '+WName+' -t '+SName,shell=True)
    else:
        return call('tmux rename-window -t '+re.escape(SName)+':0 '+WName,shell=True)

#}}}
def NewPane(SName,WNumber,PNumber,Command,Directory): #{{{
    ret = True
    if PNumber > 0:
        ret = call('tmux split-window -h -t '+re.escape(SName)+':'+str(WNumber),shell=True)
        ChangeDir(SName,WNumber,PNumber,Directory)
        ApplyCommand(SName,WNumber,PNumber,Command)

    else:
        ChangeDir(SName,WNumber,PNumber,Directory)
        ApplyCommand(SName,WNumber,PNumber,Command)

    return ret


#}}}
def ChangeDir(SName,WNumber,PNumber,Directory): #{{{
    return call(
            'tmux send-keys -t '+
            re.escape(SName)+':'+str(WNumber)+'.'+str(PNumber)+
            ' "cd '+Directory+'" C-m',shell=True)

#}}}
def ApplyCommand(SName,WNumber,PNumber,Command): #{{{
    return call(
            'tmux send-keys -t '+
            re.escape(SName)+':'+str(WNumber)+'.'+str(PNumber)+' '+
            re.escape(Command)+' C-m',shell=True)

#}}}
def SetLayout(SName,WNumber,Layout): #{{{
    call('tmux select-layout -t '+re.escape(SName)+':'+str(WNumber)+' tiled',shell=True)
    return call('tmux select-layout -t '+re.escape(SName)+':'+str(WNumber)+' '+re.escape(Layout),shell=True)

#}}}

# Creation Functions
def CreatePanesByModel(SName,WName,WNumber,Root,Model,SpecificDir): #{{{
    Layout = Model.get('layout') or Model.get('Layout')
    Panes  = Model.get('panes')  or Model.get('Panes')
    Dir = None
    if SpecificDir is None:
        Dir    = Model.get('dir')    or Model.get('Dir')
        if Dir is not None:
            Dir = Dir.replace('<WName>',WName)
            Dir = Dir.replace('<WindowName>',WName)
            Dir = Dir.replace('<SName>',SName)
            Dir = Dir.replace('<SessionName>',SName)
    else:
        Dir = SpecificDir

    if Root is not None:
        Directory = os.path.expanduser(Root)+'/'+str(Dir)
    else:
        Directory = Dir

    print('    --> Window: '+WName)

    for PNumber in range(len(Panes)):
        Command = Panes[PNumber]
        NewPane(SName,WNumber,PNumber,Command,Directory)

    SetLayout(SName,WNumber,Layout)

#}}}
def CreateWindows(SName,Root,Models,Windows): #{{{
    if Models == None:
        print('Without Models')
    else:
        #print('With Models')
        for WNumber in range(len(Windows)):
            Window = Windows[WNumber]
            WName = Window[0]
            WModel = Window[1]
            SpecificDir = None
            if len(Window) == 3:
                SpecificDir = Window[2]

            Model = Models[WModel]
            NewWindow(SName,WName,WNumber)
            CreatePanesByModel(SName,WName,WNumber,Root,Model,SpecificDir)

#}}}
def CreateSession(YAML): #{{{

    SName   = YAML.get('name')    or YAML.get('Name')
    Root    = YAML.get('root')    or YAML.get('Root')
    Models  = YAML.get('models')  or YAML.get('Models')
    Windows = YAML.get('windows') or YAML.get('Windows')

    if Models == None:
        LoadSessions(YAML)

    print()
    print('  Creating Session: '+SName)
    if not NewSession(SName):
        CreateWindows(SName,Root,Models,Windows)


#}}}
def CreateSessions(FilesDirectory): #{{{
    SNames = []
    YAMLs = []
    Files = system('ls '+FilesDirectory).split("\n")
    for SNumber in range(len(Files)):
        File = FilesDirectory+'/'+Files[SNumber]
        Stream = open(File,'r')
        try:
            YAMLs.append(load(Stream))
            SName = YAMLs[SNumber].get('name') or \
                    YAMLs[SNumber].get('Name')
            SNames.append(SName)
        except:
            pass
        Stream.close()

    print()
    print('Select The Sessions [0 1 2 ...]:')
    print()
    for SNumber in range(len(SNames)):
        print('    ['+str(SNumber)+'] '+SNames[SNumber])

    print()
    Option = input('Create All Sessions [Enter To Chose All]?')
    call('clear')

    SessionsToLoad = []
    if Option == '':
        SessionsToLoad = range(len(SNames))
    else:
        for Choice in Option.strip().split(' '):
            if Choice and (not Choice in SessionsToLoad) and Choice.isdigit():
                SessionsToLoad.append(Choice)

    for SNumber in SessionsToLoad:
        SNumber = int(SNumber)
        if SNumber in range(len(SNames)):
            CreateSession(YAMLs[SNumber])

#}}}

# Default Directory
FilesDirectory = os.path.expanduser('~/.config/IniTmux')

call('clear')
print()
print('---------------------------------------------')
CreateSessions(FilesDirectory)
print()
print('Done. Type: "tmux attach-session" To Checkout your Sessions!')
