#！python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import ctypes
import uiautomation as auto

#以管理员身份安装geekbench4
def _geekbench4_setup():
    setup_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    setup_path += '//Performance Benchmark Tool//Geekbench4//'
    os.chdir(setup_path)
    #通过命令行安装
    os.system('start Geekbench-4.3.3-WindowsSetup.exe')
    time.sleep(1)
    auto.WindowControl(searchDepth = 1,Name = 'Geekbench 4 Setup').SetActive()
 
    auto.ButtonControl(searchDepth = 2,AutomationId = '1',Name = 'Next >').Click()
    time.sleep(1)
    auto.ButtonControl(searchDepth = 2,AutomationId = '1',Name = 'I Agree').Click()
    time.sleep(1)
    auto.ButtonControl(searchDepth = 2,AutomationId = '1',Name = 'Next >').Click()
    time.sleep(1)
    auto.ButtonControl(searchDepth = 2,AutomationId = '1',Name = 'Install').Click()
    while(1):
        if auto.ButtonControl(searchDepth = 2,AutomationId = '1',Name = 'Finish').Exists():
            auto.CheckBoxControl(ClassName = 'Button',searchDepth = 3,Name = 'Run Geekbench 4').Click()
            auto.ButtonControl(searchDepth = 2,AutomationId = '1',Name = 'Finish').Click()
            break
            
    
    
    
def _geekbench4_run():
    try:
        
        auto.WindowControl(searchDepth = 1,Name = 'Untitled - Geekbench 4 Pro').GetWindowPattern().Close()
    except:
        time.sleep(1)
        
    try:
        auto.WindowControl(searchDepth = 1,Name = 'Geekbench 4 Pro').GetWindowPattern().Close()
    except:
        time.sleep(1)
    
    run_path = 'C://Program Files (x86)//Geekbench 4//'

    os.chdir(run_path)
    
    os.system('start "" ".\Geekbench 4.exe"')
    
    """
     ControlType: ButtonControl    ClassName: CCPushButton    AutomationId: CommandButton_101    Rect: (837,586,949,611)[112x25]    Name: Enter License    Handle: 0x90DA0(593312)    Depth: 4    SupportedPattern: InvokePattern LegacyIAccessiblePattern
    """
    time.sleep(2)
    i = 1
    while(1):
        try:
            if auto.ButtonControl(Name = 'Run CPU Benchmark',searchDepth = 2,AutomationId = '120').Exists():
                
                if auto.WindowControl(Name = 'Geekbench 4 Pro',searchDepth = 1).Exists(0.1):
                    auto.ButtonControl(Name = 'Run CPU Benchmark',searchDepth = 2,AutomationId = '120').Click()
                    break
                
                if auto.WindowControl(Name = 'Geekbench 4 Tryout',searchDepth = 1).Exists(0.1):
                    auto.ButtonControl(Name = 'Enter License').Click()
                    time.sleep(1)
                    auto.EditControl(AutomationId = '1004',searchDepth = 4).Click()
                    auto.EditControl(AutomationId = '1004',searchDepth = 4).SendKeys('john@primatelabs.com')
                    auto.EditControl(AutomationId = '1006',searchDepth = 4).Click()
                    auto.EditControl(AutomationId = '1006',searchDepth = 4).SendKeys('OTCRR-HDYE4-UPAJA-SJZPR-PSYTY-TUR3C-ECRZJ-QMJZF-3C6LE')
                    auto.ButtonControl(Name = 'Unlock',searchDepth = 4).Click()
                    auto.ButtonControl(searchDepth = 5, AutomationId = '2').Click()
                    auto.WindowControl(Name = 'Geekbench 4 Tryout',searchDepth = 1).GetWindowPattern().Close()
                    os.chdir(run_path)
                    os.system('start "" "Geekbench 4.exe"')
                i = i+1
        
        except:
            time.sleep(1)

  
            
    time.sleep(1)
    while(1):
        try:
            if not auto.WindowControl(Name = 'Benchmark Progress',searchDepth = 2).Exists():
                
                break
        except:
            time.sleep(1)
            
    
    score_win = auto.PaneControl(Name = 'Geekbench Score',searchDepth = 6)
    result_dict = {}
    result_dict['Single-Core Score'] = score_win.TextControl(searchDepth = 7,foundIndex = 2).Name
    result_dict['Multi-Core Score'] = score_win.TextControl(searchDepth = 7,foundIndex = 4).Name
    
    time.sleep(10)
    
    auto.WindowControl(searchDepth = 1,Name = 'Untitled - Geekbench 4 Pro').GetWindowPattern().Close()
    auto.WindowControl(searchDepth = 1,Name = 'Geekbench 4 Pro').GetWindowPattern().Close()
    return result_dict





