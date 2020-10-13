#！python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import ctypes
import uiautomation as auto

#以管理员身份安装pcmark10
def _pcmark10_setup():
    if os.path.exists('C://Program Files//UL//PCMark 10//PCMark10.exe') == True:
        register_path = 'C://Program Files//UL//PCMark 10//'
        os.chdir(register_path)
        os.system('PCMark10Cmd.exe --register=PCM10-TPRO-20200910-3RWYW-KC6MC-S56MV-TWYKV --language=en-US')
        #print('PCMark10已安装')
        return 0
        
    #进入安装程序工作目录并运行安装程序
    setup_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    setup_path += '//Performance Benchmark Tool//PCMark10//'
    os.chdir(setup_path)
    #通过命令行安装，不使用strat以让程序阻塞
    os.system('pcmark10-setup.exe /install /quiet /silent')
    
    #判断是否安装完成，未完成报错
    """
    if os.path.exists('C://Program Files//UL//PCMark 10//PCMark10.exe') == True:
        print('PCMark10安装完成')
    else :
        print('PCMark10安装失败')
    """
    register_path = 'C://Program Files//UL//PCMark 10//'
    os.chdir(register_path)
    os.system('PCMark10Cmd.exe --register=PCM10-TPRO-20200910-3RWYW-KC6MC-S56MV-TWYKV --language=en-US')
    return 0
    #另一种安装方法
    """os.system('start data_x64.msi')
    #寻找setup窗口，如果未出现就报错
    window = auto.WindowControl(searchDepth = 1, Name = '3DMark 11 Setup')
    if auto.WaitForExist(window, 3):
        auto.Logger.WriteLine("3dmark exists now")
    else:
        auto.Logger.WriteLine("3dmark does not exist after 3 seconds", auto.ConsoleColor.Yellow)
    print(window)
    #找到next按钮并点击
    auto.ButtonControl(searchDepth = 2,Name = 'Next',AutomationId = '695').Click(waitTime = 1)
    auto.CheckBoxControl(searchDepth = 2,Name = 'I accept the terms in the License Agreement').Click(waitTime = 1)
    auto.ButtonControl(searchDepth = 2,Name = 'Next',AutomationId = '695').Click(waitTime = 1)   
    auto.ButtonControl(searchDepth = 2,Name = 'Next',AutomationId = '695').Click(waitTime = 1)
    auto.ButtonControl(searchDepth = 2,Name = 'Install' ,AutomationId = '728').Click(waitTime = 1)
  
    while(1):
        time.sleep(5)
        window = auto.WindowControl(searchDepth = 1, Name = '3DMark 11 Setup')
        if window.ButtonControl(searchDepth = 2,Name = 'Finish', AutomationId = '671' ).Exists():
            window.ButtonControl(searchDepth = 2,Name = 'Finish', AutomationId = '671').Click(waitTime = 1)
            break
    """   

  
def _pcmark10_run():
 
    try:
        auto.PaneControl(searchDepth = 1,Name = 'PCMark 10 Professional Edition - Google Chrome').GetPattern(10009).Close()
    except:
        time.sleep(1)
     
    try:
        auto.WindowControl(Name = 'PCMark 10 Professional Edition',searchDepth = 1).GetWindowPattern().Close()
    except:
        time.sleep(1)

    run_path = 'C://Program Files//UL//PCMark 10//'
    os.chdir(run_path)
    
    
    os.system('start /max PCMark10.exe')
    
    time.sleep(15)

    """
    while(1):
        try:
            auto.ListItemControl(searchDepth = 7,Name = 'BENCHMARKS').Click(waitTime = 1)
            if auto.TextControl(searchDepth = 4,Name = 'IGNORE').Exists():
                auto.TextControl(searchDepth = 4,Name = 'IGNORE').Click()
            break
        except:
            time.sleep(1)
        
        time.sleep(10)
    """   

    try:
        setup_path = 'C://Program Files (x86)//Google//Chrome//Application'
        os.chdir(setup_path)
    except:
        setup_path = os.path.join(os.path.expanduser("~"), 'AppData')
        setup_path +='//Local//Google//Chrome//Application//'
        os.chdir(setup_path)
        
    
    while(1):
        try:
            web_path = 'start chrome.exe --start-maximized ' + auto.TextControl(searchDepth = 8,Name = 'HOME').GetLegacyIAccessiblePattern().Value
            break
        except:
            time.sleep(1)
            
        try:
            web_path = 'start chrome.exe --start-maximized ' + auto.HyperlinkControl(searchDepth = 8,Name = 'HOME').GetLegacyIAccessiblePattern().Value

            break
        except:
            time.sleep(1)
    
     
    os.system(web_path)   

        #关闭提示
    time.sleep(4)
 
    try: 
        auto.ButtonControl(searchDepth = 3,Name = 'Advanced').Click()
        auto.HyperlinkControl(searchDepth = 5,Name = 'Proceed to 127.0.0.1 (unsafe)').Click()
    except:
        time.sleep(1)
        
    try: 
        auto.ButtonControl(searchDepth = 3,Name = '高级').Click()
        auto.HyperlinkControl(searchDepth = 5,Name = '继续前往127.0.0.1（不安全）').Click()
    except:
        time.sleep(1)
        
  
    try:
        auto.PaneControl(searchDepth = 1,Name = 'PCMark 10 Professional Edition - Google Chrome').SetActive()
    except:
        time.sleep(1)
    

    #跳转到basic选项卡运行测试并等待结果
  
    while(1):
        try:
            auto.HyperlinkControl(searchDepth= 5,AutomationId = 'headerLogo').Click()
            auto.HyperlinkControl(searchDepth= 8,Name = 'BENCHMARKS').Click()
           
            break
        except:
            time.sleep(1)
            
            
     
            
    
    time.sleep(5)
    while(1):
        try:
            auto.TextControl(searchDepth = 13,Name = 'PCMark 10 Extended').Click()
            time.sleep(2)
            auto.HyperlinkControl(searchDepth = 10,Name = 'RUN').Click()
            break
        except:
            time.sleep(1)
    
    
    #等待运行结果
    while(1):
        try:
            if auto.PaneControl(Name = 'PCMark 10 progress - Google Chrome',searchDepth = 1).Exists() == False :
                break
        except:
            time.sleep(10)
    
        

    #光标移动到结果读取结果  
    time.sleep(2)
    result_dict = {}
    while(1):
        
        if auto.GroupControl(searchDepth = 8,AutomationId = 'viewResults').Exists(0.1):
            result_win = auto.GroupControl(searchDepth = 8,AutomationId = 'viewResults')    
            break
            
        elif auto.CustomControl(searchDepth = 8,AutomationId = 'viewResults').Exists(0.1):
            result_win = auto.CustomControl(searchDepth = 8,AutomationId = 'viewResults')
            break
        
        
    print(result_win)
    time.sleep(2)
    i = 0
    while(1):
        if i == 20:
            i = 0
            
        try:
            if result_win.CustomControl(searchDepth = 9,foundIndex = i).TextControl(searchDepth = 10,Name = 'PCMark 10 Extended').Exists(0.1):
                print(result_win.CustomControl(searchDepth = 9,foundIndex = i).TextControl(searchDepth = 10))
                result_dict['Score'] = "".join(result_win.CustomControl(Depath = 9,foundIndex = i+1).TextControl(foundIndex = 1).Name.split())
                break  
        except:
            time.sleep(1)
            
        try:    
            if result_win.GroupControl(searchDepth = 9,foundIndex = i).TextControl(searchDepth = 10,Name = 'PCMark 10 Extended').Exists(0.1):
                print(result_win.GroupControl(searchDepth = 9,foundIndex = i).TextControl(searchDepth = 10))
                result_dict['Score'] = "".join(result_win.GroupControl(Depath = 9,foundIndex = i+1).TextControl(foundIndex = 1).Name.split())
                break            
        except:
            time.sleep(1)
        
        print(i)
        i += 1  
      
 
    
    try:
        result_dict['Essentials'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 1).TextControl(foundIndex = 3).Name.split())
        result_dict['App Start-up Score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 2).TextControl(foundIndex = 5).Name.split())
        result_dict['Video Conferencing Score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 3).TextControl(foundIndex = 5).Name.split())
        result_dict['Web Browsing Score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 4).TextControl(foundIndex = 5).Name.split())
        result_dict['Productivity'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 5).TextControl(foundIndex = 3).Name.split())
        result_dict['Spreadsheets Score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 6).TextControl(foundIndex = 5).Name.split())
        result_dict['Writing Score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 7).TextControl(foundIndex = 5).Name.split())
        result_dict['Digital Content Creation'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 8).TextControl(foundIndex = 3).Name.split())
        result_dict['Photo Editing Score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 9).TextControl(foundIndex = 5).Name.split())
        result_dict['Rendering and Visualization Score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 10).TextControl(foundIndex = 5).Name.split())
        result_dict['Video Editing Score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 11).TextControl(foundIndex = 5).Name.split())
        
        result_dict['Gaming'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 12).TextControl(foundIndex = 3).Name.split())
        result_dict['Graphics score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 13).TextControl(foundIndex = 5).Name.split())           
        result_dict['Physics score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 14).TextControl(foundIndex = 5).Name.split())            
        result_dict['Combined score'] = "".join(result_win.ListControl(searchDepth = 9,foundIndex = 15).TextControl(foundIndex = 5).Name.split()) 
        
     
        #关闭窗口
 
        auto.PaneControl(searchDepth = 1,Name = 'PCMark 10 Professional Edition - Google Chrome').GetPattern(10009).Close()
        auto.WindowControl(Name = 'PCMark 10 Professional Edition',searchDepth = 1).GetWindowPattern().Close()
    except:
        auto.PaneControl(searchDepth = 1,Name = 'PCMark 10 Professional Edition - Google Chrome').GetPattern(10009).Close()
        auto.WindowControl(Name = 'PCMark 10 Professional Edition',searchDepth = 1).GetWindowPattern().Close()

    
    return result_dict
  

 
  
 
 
 
 
 
 
