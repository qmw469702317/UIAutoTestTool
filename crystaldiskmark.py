#！python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import ctypes
import uiautomation as auto


def _crystaldiskmark_run():
    try:
        auto.WindowControl(searchDepath = 1, Name = 'CrystalDiskMark 6.0.2 x64').GetWindowPattern().Close()
    except:
        time.sleep(1)
        
    run_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    run_path += '//Performance Benchmark Tool//CrystalDiskMark//'
    os.chdir(run_path)
    #通过命令行安装，不使用strat以让程序阻塞
    os.system('start DiskMark64.exe')
    
    #打开程序并运行
    while(1):
        try:
            main_win = auto.WindowControl(searchDepath = 1, Name = 'CrystalDiskMark 6.0.2 x64')
            break
        except:
            time.sleep(1)
            
    main_win.HyperlinkControl(Name = 'All',searchDepath = 8).Click()
    #等待程序运行结束
    """ControlType: HyperlinkControl    ClassName:     AutomationId: All    Rect: (1193,145,1255,195)[62x50]    Name: Stop    Handle: 0x0(0)    Depth: 8    ValuePattern.Value: file:///C:/U"""
    while(1):
        time.sleep(10)
        if not auto.HyperlinkControl(searchDepath = 8,AutomationId = 'All',Name = 'Stop').Exists():
            break
        
            
    main_win = auto.WindowControl(searchDepath = 1, Name = 'CrystalDiskMark 6.0.2 x64')

    result_dict = {}
    result_dict['Seq_Q32T1_Read'] = main_win.DataItemControl(searchDepath = 7,foundIndex = 6).Name
    print(main_win.DataItemControl(searchDepath = 7,FoundIndex = 6))
    result_dict['Seq_Q32T1_Write'] = main_win.DataItemControl(searchDepath = 7,foundIndex = 7).Name    
    result_dict['4KiB_Q8T8_Read'] = main_win.DataItemControl(searchDepath = 7,foundIndex = 9).Name
    result_dict['4KiB_Q8T8_Write'] = main_win.DataItemControl(searchDepath = 7,foundIndex = 10).Name
    result_dict['4KiB_Q32T1_Read'] = main_win.DataItemControl(searchDepath = 7,foundIndex = 12).Name
    result_dict['4KiB_Q32T1_Write'] = main_win.DataItemControl(searchDepath = 7,foundIndex = 13).Name
    result_dict['4KiB_Q1T1_Read'] = main_win.DataItemControl(searchDepath = 7,foundIndex = 15).Name
    result_dict['4KiB_Q1T1_Write'] = main_win.DataItemControl(searchDepath = 7, foundIndex = 16).Name
    main_win.GetWindowPattern().Close()
    return result_dict
    
