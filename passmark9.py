#！python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import ctypes
import uiautomation as auto

def _passmark9_setup():
    setup_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    setup_path += '//Performance Benchmark Tool//Pass Mark9//'
    os.chdir(setup_path)
    #通过命令行安装
    os.system('"petst  9.0.1030.0.exe" /install /quiet /silent')
    """
    if os.path.exists('C://Program Files//PerformanceTest//PerformanceTest64.exe') == True:
        print('passmark9安装完成')
    else :
        print('passmark9安装失败')
    """
            
def _passmark9_run():
    try:
        auto.WindowControl(Name = 'PerformanceTest 9.0',searchDepth = 1).GetWindowPattern().Close()
    except:
        time.sleep(1)

    run_path = 'C://Program Files//PerformanceTest//'
    os.chdir(run_path)
    os.system('start PerformanceTest64.exe')
    #等待更新窗口出现并关闭
    while(1):
        try:
            #如果出现注册窗口
            if auto.WindowControl(searchDepth = 1,ClassName = 'PT').Name == 'PerformanceTest 9.0 Evaluation Version':
                reg_win = auto.WindowControl(searchDepth = 2,Name = 'PassMark® PerformanceTest')
         
                regedit = reg_win.EditControl(searchDepth = 3,AutomationId = '1034')
          
                regedit.Click()
                regedit.GetValuePattern().SetValue('''BABAE HAN
                #AEESAQAB8VU7IDH999NMAEK9UAAPPTPKNFEUN86KXXY6V55Z5GAQHPBRUDHKZAS5553PQ5SGNSDSWX93RMZAPQ2QSN3TFSJSV536RR9ZYY5526KEUIVSUATG''')
                #regedit.SendKey('BABAE HAN{Enter}')
                #regedit.SendKey('{Ctrl}{End}{Enter}#AEESAQAB8VU7IDH999NMAEK9UAAPPTPKNFEUN86KXXY6V55Z5GAQHPBRUDHKZAS5553PQ5SGNSDSWX93RMZAPQ2QSN3TFSJSV536RR9ZYY5526KEUIVSUATG')
                auto.ButtonControl(AutomationId = '10',searchDepth = 3,Name = 'Register').Click()
                time.sleep(2)
                auto.ButtonControl(searchDepth = 4 ,AutomationId = '2').Click()
            else :
                break
        except:
            time.sleep(2)
            
    #先点击Test，然后RUN ALL Test，然后确定弹窗
    while(1):    
        try:
            auto.MenuItemControl(Name = 'Tests',searchDepth = 3).Click()
            auto.MenuItemControl(searchDepth = 3,Name = 'Run All Tests').Click()
            if  auto.ButtonControl(searchDepth = 3,AutomationId = '2').Exists():
                auto.ButtonControl(searchDepth = 3,AutomationId = '2').Click()
                time.sleep(60)
                continue
                
            auto.WindowControl(searchDepth = 2,Name = 'Run all benchmark tests?').ButtonControl(searchDepth = 3,AutomationId = '6').Click()
            break
        except:
            auto.ButtonControl(searchDepth = 3,AutomationId = '2').Click()
            time.sleep(5)
    
    
    while(1):
        try: 
            auto.CheckBoxControl(searchDepth = 3,AutomationId = '12104').Click()
            auto.ButtonControl(searchDepth = 3,AutomationId = '12100').Click()
            break
        except:
            time.sleep(5)
        
    auto.MenuItemControl(Name = 'File',searchDepth = 3).Click()
    auto.MenuItemControl(searchDepth = 3,Name = 'Save results as text...').Click()
    #C:\Users\QMW\Documents\PassMark\PerformanceTest9\PerfRes.txt
    auto.ButtonControl(searchDepth = 3,AutomationId = '1006').Click()
    if auto.WindowControl(searchDepth = 3,Name = 'WARNING').Exists():
        auto.ButtonControl(searchDepth = 4,AutomationId='6').Click()
    
    file_path = os.path.join(os.path.expanduser("~"), 'Documents')    
    filename = file_path+'//PassMark//PerformanceTest9//PerfRes.txt'
    print(filename)
    result_dict = {}
    with open(filename) as read_file:
        for line in read_file:
            if 'PassMark Rating (Composite average) : ' in line:
                line = line.replace('PassMark Rating (Composite average) : ','')
                result_dict['PassMark Rating'] = "".join(line.split())
                break
            
            if 'CPU Mark (Composite average) : ' in line:
                line = line.replace('CPU Mark (Composite average) : ','')
                result_dict['CPU Mark'] = "".join(line.split())
                
            if '3D Graphics Mark (Composite average) : ' in line:
                line = line.replace('3D Graphics Mark (Composite average) : ','')
                result_dict['3D Graphics Mark'] = "".join(line.split())   
            
            if 'Disk Mark (Composite average) : ' in line:
                line = line.replace('Disk Mark (Composite average) : ','')
                result_dict['Disk Mark'] = "".join(line.split())    
            
            if '2D Graphics Mark (Composite average) : ' in line:
                line = line.replace('2D Graphics Mark (Composite average) : ','')
                result_dict['2D Graphics Mark'] = "".join(line.split())   
            
            if 'Memory Mark (Composite average) : ' in line:
                line = line.replace('Memory Mark (Composite average) : ','')
                result_dict['Memory Mark'] = "".join(line.split())
    
    

    auto.WindowControl(Name = 'PerformanceTest 9.0',searchDepth = 1).GetWindowPattern().Close()
    return result_dict


    
