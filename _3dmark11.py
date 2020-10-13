#！python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import ctypes
import uiautomation as auto

#以管理员身份安装3dmark11
def _3dmark11_setup():
    if os.path.exists('C://Program Files//Futuremark//3DMark 11//3DMarkLauncher.exe') == True:
        #print('3DMark11已安装')
        return 0
        
    #进入安装程序工作目录并运行安装程序
    setup_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    setup_path += '//Performance Benchmark Tool//3DMark11//'
    os.chdir(setup_path)
    #通过命令行安装，不使用strat以让程序阻塞
    os.system('setup.exe /install /quiet /silent')
    
    #判断是否安装完成，未完成报错
  
    register_path = 'C://Program Files//Futuremark//3DMark 11//bin//x64//'    
    os.chdir(register_path)
    #注册
    os.system('3DMark11Cmd.exe --register=3D11-ADV-2T39-M27U-9ZMA-HPAN-2HVX') #根据官网给出的命令行指令
    
    return 0
    #另一种安装方法


def _3dmark11_run():
    try:
        auto.WindowControl(Name = '3DMark 11 Advanced Edition',searchDepth = 1,AutomationId = 'Window').GetWindowPattern().Close()
    except:
        time.sleep(1)

    run_path = 'C://Program Files//Futuremark//3DMark 11//'
    os.chdir(run_path)
    os.system('start 3DMarkLauncher.exe')
    #等待更新窗口出现并关闭
    time.sleep(10)
    
    try:
        if auto.WindowControl(searchDepth = 1,Name = 'Update Available' ).Exists():
            auto.WindowControl(searchDepth = 1,Name = 'Update Available' ).GetWindowPattern().Close()
    except:
        if auto.WindowControl(searchDepth = 1,Name = '更新可用' ).Exists():
            auto.WindowControl(searchDepth = 1,Name = '更新可用' ).GetWindowPattern().Close()
              
          
    auto.WindowControl(Name = '3DMark 11 Advanced Edition',searchDepth = 1,AutomationId = 'Window').SetActive()
    auto.TabItemControl(searchDepth = 3,AutomationId = 'ResultTab').Click()
    tab_result = auto.TabItemControl(searchDepth = 3,AutomationId = 'ResultTab')

    if tab_result.CheckBoxControl(searchDepth = 4).GetTogglePattern().ToggleState == 1:
        tab_result.CheckBoxControl(searchDepth = 4).Click()
    
 
    
    
    #跳转到basic选项卡运行测试并等待结果
    auto.TabItemControl(searchDepth = 3,Name = 'Basic',AutomationId = 'BasicTab').Click(waitTime = 1)
    auto.RadioButtonControl(searchDepth = 4,AutomationId = 'PresetPerformanceRadioButton').Click(waitTime = 1)
    auto.RadioButtonControl(searchDepth = 4,AutomationId = 'RunBenchmarkRadioButton').Click(waitTime = 1)
    auto.RadioButtonControl(searchDepth = 4,AutomationId = 'StretchedScalingModeRadioButton').Click(waitTime = 1)
    try:
        auto.ButtonControl(searchDepth = 4,Name = 'Run 3DMark 11').Click(waitTime = 1)
    except:
        auto.ButtonControl(searchDepth = 4,Name = '运行 3DMark 11').Click(waitTime = 1)
        
 
    #等待运行结果
    while(1):
        time.sleep(30)
        try:
            if auto.TabItemControl(AutomationId = 'ResultTab',searchDepth = 3).GetSelectionItemPattern().IsSelected == True :
                time.sleep(2)
                break
        except:
            time.sleep(10)
    
        
    auto.WindowControl(Name = '3DMark 11 Advanced Edition').SetActive()
    #光标移动到结果读取结果  
    auto.TabItemControl(searchDepth = 3,AutomationId = 'ResultTab').Click()
    result_dict = {}
    result_dict['Score'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflineScoreLabel').Name
    result_dict['Graphics Score'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflineGraphicsScoreLabel').Name
    result_dict['Physics Score'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflinePhysicsScoreLabel').Name
    result_dict['Combined Score'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflineCombinedScoreLabel').Name
    result_dict['GT1'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflineGT1ResultLabel').Name
    result_dict['GT2'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflineGT2ResultLabel').Name
    result_dict['GT3'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflineGT3ResultLabel').Name
    result_dict['GT4'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflineGT4ResultLabel').Name
    result_dict['PT'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflinePTResultLabel').Name
    result_dict['CT'] = auto.TextControl(searchDepth = 4, AutomationId = 'OfflineCTResultLabel').Name
    
    #关闭窗口
    auto.WindowControl(Name = '3DMark 11 Advanced Edition',searchDepth = 1,AutomationId = 'Window').GetWindowPattern().Close()
    
    return result_dict


 
 
 
 
 
 
 
 
 
