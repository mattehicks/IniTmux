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

WPattern = r"<(?i)(windown|wn|winn|windn)ame>"
SPattern = r"<(?i)(sessionn|sn|sesn|sessn)ame>"
TmuxLayouts = []
TmuxLayouts.append('tiled')
TmuxLayouts.append('even-horizontal')
TmuxLayouts.append('even-vertical')
TmuxLayouts.append('main-horizontal')
TmuxLayouts.append('main-vertical')
FilesDirectory = os.path.expanduser('~/.config/IniTmux')

# Tmux Functions {{{
def SwapWindows(SName,WNumber1,WNumber2): #{{{
    Command = 'tmux swap-window'+ ' -s '+SName+':'+str(WNumber1)+ ' -t '+SName+':'+str(WNumber2)
    print(Command)
    return call(Command,shell=True)
#}}}
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
    if Directory is None:
        return
    else:
        return call(
                'tmux send-keys -t '+
                re.escape(SName)+':'+str(WNumber)+'.'+str(PNumber)+
                ' "cd '+Directory+'" C-m',shell=True)

#}}}
def ApplyCommand(SName,WNumber,PNumber,Command): #{{{
    if Command is None:
        return
    else:
        return call(
                'tmux send-keys -t '+
                re.escape(SName)+':'+str(WNumber)+'.'+str(PNumber)+' '+
                re.escape(Command)+' C-m',shell=True)

#}}}
def SetLayout(SName,WNumber,Layout): #{{{
    if Layout in TmuxLayouts:
        return call('tmux select-layout -t '+re.escape(SName)+':'+str(WNumber)+' '+re.escape(Layout),shell=True)
    elif Layout is None:
        return call('tmux select-layout -t '+re.escape(SName)+':'+str(WNumber)+' tiled',shell=True)
    else:
        call('tmux select-layout -t '+re.escape(SName)+':'+str(WNumber)+' tiled',shell=True)
        return call('tmux select-layout -t '+re.escape(SName)+':'+str(WNumber)+' '+re.escape(Layout),shell=True)

#}}}

#}}}

# Load and Get Functions {{{
def LoadYAMLs(FilesDirectory): #{{{
    YAMLs = []
    Files = system('ls '+FilesDirectory).split("\n")
    for SNumber in range(len(Files)):
        File = FilesDirectory+'/'+Files[SNumber]
        Stream = open(File,'r')
        try:
            YAMLs.append(load(Stream))
        except:
            pass
        Stream.close()
    return YAMLs
#}}}
def GetSessionsNamesFromYAMLs(YAMLs): #{{{
    SNames = []
    for SNumber in range(len(YAMLs)):
        SName = YAMLs[SNumber].get('name')
        if SName not in SNames+[None]:
            SNames.append(SName)

    return SNames
#}}}
def GetSesssionsToLoad(SNames): #{{{

    print()
    print('Select The Sessions [0 1 2 ...]:')
    print()
    for SNumber in range(len(SNames)):
        print('    ['+str(SNumber)+'] '+SNames[SNumber])

    print()
    Input = input('Create All Sessions [Enter To Chose All]?')
    call('clear')

    SessionsToLoad = []
    if Input == '':
        SessionsToLoad = range(len(SNames))
    else:
        for Choice in Input.strip().split(' '):
            if Choice and (not Choice in SessionsToLoad) and Choice.isdigit():
                SessionsToLoad.append(Choice)

    return SessionsToLoad
#}}}
def GetTmuxSessionsNames(): #{{{
    ListSessions = system('tmux list-sessions')
    if not ListSessions == 'failed to connect to server: Connection refused':
        ListSessions = system("tmux list-sessions -F '#S'")
        return ListSessions.split("\n")
    else:
        return []

#}}}
def GetTmuxWindowsNames(SName): #{{{
    ListSessions = system('tmux list-sessions')
    if not ListSessions == 'failed to connect to server: Connection refused':
        ListWindows = system("tmux list-windows -t "+SName+" -F '#W'")
        return ListWindows.split("\n")
    else:
        return []

#}}}
def GetTmuxNPanes(SName): #{{{
    ListSessions = system('tmux list-sessions')
    if not ListSessions == 'failed to connect to server: Connection refused':
        NPanes = system("tmux list-windows -t "+SName+" -F '#{window_panes}'")
        return NPanes.split("\n")
    else:
        return []

#}}}
def GetTmuxWorkspace(): #{{{

    ListSessions = system('tmux list-sessions')
    if not ListSessions == 'failed to connect to server: Connection refused':
        ListSessions = ListSessions.split("\n")

        Sessions = []

        for i in range(len(ListSessions)):
            ListSessions[i] = ListSessions[i].split("windows")[0].split(":")[0]
            Sessions.append({'name':ListSessions[i],'windows':[]})
        
        for i in range(len(Sessions)):
            ListWindows = system('tmux list-windows -t '+Sessions[i]['name'])
            ListWindows = ListWindows.split("\n")
            for j in range(len(ListWindows)):
                # Search for Number and Name
                find = re.findall(r"[0-9]+: [\w]+",ListWindows[j])
                find = find[0].split(":")
                WNumber = int(find[0])
                WName   = find[1].strip()

                # Search for Size
                WSize = re.findall(r"\[[\d]+x[\d]+\]",ListWindows[j])[0].strip(r"(?:[|])")

                # Search for Layout
                WLayout = re.findall(r"\[layout [\d\w,\[\]\{\}]+\]",ListWindows[j])[0].strip(r"[layout")
                WLayout = re.sub(r"]$","",WLayout)

                # Search for Number of Panes
                NPanes = int(re.findall(r"\([\d]+ panes\)",ListWindows[j])[0].strip(r"(?:\(|panes\))"))

                Window = {}
                Window['WName']   = WName
                Window['WNumber'] = WNumber
                Window['WSize']   = WSize
                Window['WLayout'] = WLayout.strip()
                Window['NPanes']  = NPanes

                Sessions[i]['windows'].append(Window)

                #print(ListWindows[j])

        print(dump(Sessions[0]))
        stream = open("samples/Project.yml",'r')
        pprint(load(stream))
    
#SPattern = r"<(?i)(sessionn|sn|sesn|sessn)ame>"
#}}}
def GetWindowsNames(Windows): #{{{
    WNames = []
    for WNumber in range(len(Windows)):
        Window = Windows[WNumber]
        if type(Window) == type([]):
            WName = Window[0]
        elif type(Window) == type({}):
            WName = list(Window.keys())[0]

        if WName not in WNames:
            WNames.append(WName)

    return WNames
#}}}
def GetWindowsModels(Models,Windows):#{{{
    WModels = []
    for WNumber in range(len(Windows)):
        Window = Windows[WNumber]
        if type(Window) == type([]):
            WModelName = Window[1]
            Model = Models[WModelName]
        elif type(Window) == type({}):
            WName = list(Window.keys())[0]
            Model = Window[WName]
            if type(Model) == type(''):
                Model = Models[Model]
            elif type(Model) == type({}):
                WModelName = Model.get('model')
                if WModelName is not None:
                    Model = Models[WModelName]

        if Model not in WModels:
            WModels.append(Model)

    return WModels
#}}}
def ReloadWindows(SName): #{{{
    pass

#}}}
#}}}

# Creation Functions {{{
def CreatePanes(SName,WName,WNumber,Root,Model,SpecificDir,SpecificLayout): #{{{

    if SpecificLayout is None:
        Layout = Model.get('layout')
    else:
        Layout = SpecificLayout

    if SpecificDir is None:
        Dir    = Model.get('dir')
        if Dir is not None:
            Dir = re.sub(WPattern,WName,Dir)
            Dir = re.sub(SPattern,SName,Dir)
    else:
        Dir = SpecificDir
        Dir = re.sub(WPattern,WName,Dir)
        Dir = re.sub(SPattern,SName,Dir)


    if   Root is None and Dir is None:
        Directory = os.path.expanduser('~')

    elif Root is None and Dir is not None:
        Dir = re.sub(r" ",'\ ',Dir)
        Directory = os.path.expanduser(Dir)

    elif Root is not None and Dir is None:
        Root = re.sub(WPattern,WName,Root)
        Root = re.sub(SPattern,SName,Root)
        Directory = os.path.expanduser(Root)

    elif Root is not None and Dir is not None:
        Root = re.sub(WPattern,WName,Root)
        Root = re.sub(SPattern,SName,Root)
        Dir = re.sub(r" ",'\ ',Dir)
        Directory = os.path.expanduser(Root)+'/'+str(Dir)

    print('    --> Window: '+WName)

    Panes  = Model.get('panes')

    if type(Panes) is int:
        for PNumber in range(Panes):
            Command = None
            NewPane(SName,WNumber,PNumber,Command,Directory)
    elif type(Panes) == type([]):
        for PNumber in range(len(Panes)):
            if type(Panes[PNumber]) == type({}):
                Command = None
                NewPane(SName,WNumber,PNumber,Command,Directory)
                for Command in list(Panes[PNumber].values())[0]:
                    Command = re.sub(WPattern,WName,Command)
                    Command = re.sub(SPattern,SName,Command)
                    ApplyCommand(SName,WNumber,PNumber,Command)
            else:
                Command = Panes[PNumber]
                Command = re.sub(WPattern,WName,Command)
                Command = re.sub(SPattern,SName,Command)
                NewPane(SName,WNumber,PNumber,Command,Directory)


    SetLayout(SName,WNumber,Layout)

#}}}
def CreateWindows(SName,Root,Models,Windows): #{{{
    for WNumber in range(len(Windows)):
        Window = Windows[WNumber]
        SpecificDir = None
        SpecificLayout = None
        if type(Window) == type([]):
            WName = Window[0]
            WModelName = Window[1]
            if len(Window) == 3:
                SpecificDir = Window[2]
    
            Model = Models[WModelName]
        elif type(Window) == type({}):
            WName = list(Window.keys())[0]
            Model = Window[WName]
            if type(Model) == type(''):
                Model = Models[Model]
            elif type(Model) == type({}):
                SpecificLayout = Model.get('layout')
                WModelName = Model.get('model')
                SpecificDir = Model.get('dir')
                if WModelName is not None:
                    Model = Models[WModelName]
            elif type(Model) == type(0):
                NPanes = Model
                Model = {'panes':NPanes}

        if WName not in GetTmuxWindowsNames(SName):
            NewWindow(SName,WName,WNumber)
            CreatePanes(SName,WName,WNumber,Root,Model,SpecificDir,SpecificLayout)

    ReloadWindows(SName)

#}}}
def CreateSession(YAML): #{{{

    SName   = YAML.get('name')
    Root    = YAML.get('root')
    Models  = YAML.get('models')
    Windows = YAML.get('windows')

    print()
    if not SName in GetTmuxSessionsNames():
        print('  Creating  Session: '+SName)
        NewSession(SName)
    else:
        print('  Reloading Session: '+SName)

    CreateWindows(SName,Root,Models,Windows)


#}}}
def CreateSessions(FilesDirectory): #{{{
    YAMLs = LoadYAMLs(FilesDirectory)
    SNames = GetSessionsNamesFromYAMLs(YAMLs)

    for SNumber in GetSesssionsToLoad(SNames):
        SNumber = int(SNumber)
        if SNumber in range(len(SNames)):
            CreateSession(YAMLs[SNumber])

#}}}
#}}}
# Default Directory

call('clear')
print()
print('---------------------------------------------')
CreateSessions(FilesDirectory)
print()
print('Done. Type: "tmux attach-session" To Checkout your Sessions!')

#input('')
#call('killall tmux',shell=True)

#ReloadWindows('Test')
