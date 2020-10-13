#！python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import ctypes
import uiautomation as auto

#以管理员身份安装3dmark
def _3dmark_setup():
    if os.path.exists('C://Program Files//UL//3DMark//3DMark.exe') == True:
        register_path = 'C://Program Files//UL//3DMark//'
        os.chdir(register_path)
        os.system('3DMarkCmd.exe --register=3DM-PICFT-2U57K-XN77L-ZMCUH-LMT4T --language=en-US')
        #print('3dmark已安装')
        return 0
        
    #进入安装程序工作目录并运行安装程序
    setup_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    setup_path += '//Performance Benchmark Tool//3DMark//'
    os.chdir(setup_path)
    #通过命令行安装，不使用strat以让程序阻塞
    os.system('3dmark-setup.exe /install /quiet /silent')
    

    register_path = 'C://Program Files//UL//3DMark//'
    os.chdir(register_path)
    os.system('3DMarkCmd.exe --register=3DM-PICFT-2U57K-XN77L-ZMCUH-LMT4T --language=en-US')
    return 0
   

  
def _3dmark_run():
    try:
        auto.PaneControl(searchDepth = 1,Name = '3DMark Professional Edition - Google Chrome').GetPattern(10009).Close()
    except:
        time.sleep(1)
    
    try:
    
        auto.WindowControl(Name = '3DMark Professional Edition',searchDepth = 1).GetWindowPattern().Close()
            
    except:
        time.sleep(1)


    run_path = 'C://Program Files//UL//3DMark//'
    os.chdir(run_path)
    os.system('start 3DMark.exe')
   
    time.sleep(5)
    
    
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
        auto.PaneControl(searchDepth = 1,Name = '3DMark Professional Edition - Google Chrome').SetActive()
    except:
        time.sleep(1)
        
    result_dict = {}
    #跳转到basic选项卡运行测试并等待结果
    while(1):
        try:
            auto.HyperlinkControl(searchDepth= 8,Name = 'BENCHMARKS').Click()
           
            break
        except:
            time.sleep(1)
            
            
     
    time.sleep(3)
      
    while(1):
        try:
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').SendKeys('{Down 3}')
            auto.TextControl(searchDepth = 14,Name = 'Time Spy').Click()
            time.sleep(2)
            auto.HyperlinkControl(searchDepth = 15,Name = 'RUN').Click()
            break
        except:
            time.sleep(1)
    
    
    #等待运行结果
    while(1):
        try:
            if not auto.TextControl(searchDepth = 11,Name = 'Running benchmark').Exists(0.1):
                break
        except:
            time.sleep(3)
            
   
    #光标移动到结果读取结果  
    
    
    time_spy = {}
       
        
    while(1):
        try:    
            try:
                time_spy['Score'] = "".join(auto.CustomControl(searchDepth = 10,AutomationId = 'viewResultsControls').TextControl(foundIndex = 3).Name.split())
                time_result = auto.CustomControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')
            except:
                time_spy['Score'] = "".join(auto.GroupControl(searchDepth = 10,AutomationId = 'viewResultsControls').TextControl(foundIndex = 3).Name.split())
                time_result = auto.GroupControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')
                
  
            time_spy['Graphics Score'] = "".join(time_result.ListControl(searchDepth = 11,foundIndex = 1).TextControl(foundIndex = 3).Name.split())  

            time_spy['CPU score'] = "".join(time_result.ListControl(searchDepth = 11,foundIndex = 4).TextControl(foundIndex = 3).Name.split())

            result_dict['Time Spy'] = time_spy
       
            break
        except:
       
            time.sleep(1)
    


    time.sleep(180)
    #fire strike
    while(1):
        try:
            auto.HyperlinkControl(searchDepth= 8,Name = 'BENCHMARKS').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').SendKeys('{Down 15}')
            auto.TextControl(searchDepth = 14,Name = 'Fire Strike').Click()
            time.sleep(2)
            auto.HyperlinkControl(searchDepth = 15,Name = 'RUN').Click()
            break
        except:
            time.sleep(1)
            
    while(1):
        try:
            if not auto.TextControl(searchDepth = 11,Name = 'Running benchmark').Exists():
                break
        except:
            time.sleep(3)
            
    fire_strike = {}  

    while(1):
        try:
        
            try:
                fire_strike['Score'] = "".join(auto.CustomControl(searchDepth = 10,AutomationId = 'viewResultsControls').TextControl(foundIndex = 3).Name.split())      
                fire_result = auto.CustomControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')
            except:
                fire_strike['Score'] = "".join(auto.GroupControl(searchDepth = 10,AutomationId = 'viewResultsControls').TextControl(foundIndex = 3).Name.split())
                fire_result = auto.GroupControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')
                
            fire_strike['Graphics score'] = "".join(fire_result.ListControl(searchDepth = 11,foundIndex = 1).TextControl(foundIndex = 3).Name.split())
            fire_strike['Physics score'] = "".join(fire_result.ListControl(searchDepth = 11,foundIndex = 4).TextControl(foundIndex = 3).Name.split())
            fire_strike['Combined score'] = "".join(fire_result.ListControl(searchDepth = 11,foundIndex = 6).TextControl(foundIndex = 3).Name.split())    
            result_dict['Fire Strike'] = fire_strike
            break
        except:
            time.sleep(1)
            
    time.sleep(180)
    #Night raid
    while(1):
        try:
            auto.HyperlinkControl(searchDepth= 8,Name = 'BENCHMARKS').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').SendKeys('{Down 25}')
            auto.TextControl(searchDepth = 14,Name = 'Night Raid').Click()
            time.sleep(2)
            break
        except:
            time.sleep(1)
            
    try:     
        if auto.HyperlinkControl(searchDepth = 15,Name = 'INSTALL').Exists():
            auto.HyperlinkControl(searchDepth = 15,Name = 'INSTALL').Click()
    except:
        time.sleep(1)
        
        
    while(1):
        try:
            auto.HyperlinkControl(searchDepth = 15,Name = 'RUN').Click()
            break
        except:
            time.sleep(10)
            
    while(1):
        try:
            if not auto.TextControl(searchDepth = 11,Name = 'Running benchmark').Exists():
                break
        except:
            time.sleep(3)
            
    night_raid = {}

    while(1):
        try:
            try:
                night_raid['Score'] = "".join(auto.CustomControl(searchDepth = 10,AutomationId = 'viewResultsControls').TextControl(foundIndex = 3).Name.split())

                night_result = auto.CustomControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')
            except:
                night_raid['Score'] = "".join(auto.GroupControl(searchDepth = 10,AutomationId = 'viewResultsControls').TextControl(foundIndex = 3).Name.split())
                night_result = auto.GroupControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')   
                
            night_raid['Graphics score'] = "".join(night_result.ListControl(searchDepth = 11,foundIndex = 1).TextControl(foundIndex = 3).Name.split())
            night_raid['CPU score'] = "".join(night_result.ListControl(searchDepth = 11,foundIndex = 4).TextControl(foundIndex = 3).Name.split())
            result_dict['Night Raid'] = night_raid
            break
        except:
            time.sleep(1)
    
    time.sleep(180)        
    #sky drive
    while(1):
        try:
        
            auto.HyperlinkControl(searchDepth= 8,Name = 'BENCHMARKS').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').SendKeys('{Down 25}')
            auto.TextControl(searchDepth = 14,Name = 'Sky Diver').Click()
            time.sleep(2)
            auto.HyperlinkControl(searchDepth = 15,Name = 'RUN').Click()
            break
        except:
            time.sleep(1)
            
    while(1):
        try:
            if not auto.TextControl(searchDepth = 11,Name = 'Running benchmark').Exists():
                break
        except:
            time.sleep(3)
    
    sky_drive = {}
    while(1):
        try:
            try:
                sky_drive['Score'] = "".join(auto.CustomControl(searchDepth = 10,AutomationId = 'viewResultsControls').TextControl(foundIndex = 3).Name.split())
                sky_result = auto.CustomControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')
            except:
                sky_drive['Score'] = "".join(auto.GroupControl(searchDepth = 10,AutomationId = 'viewResultsControls').TextControl(foundIndex = 3).Name.split())
                sky_result = auto.GroupControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')   
                
            sky_drive['Graphics score'] = "".join(sky_result.ListControl(searchDepth = 11,foundIndex = 1).TextControl(foundIndex = 3).Name.split())
            sky_drive['Physics score'] = "".join(sky_result.ListControl(searchDepth = 11,foundIndex = 4).TextControl(foundIndex = 3).Name.split())
            sky_drive['Combined score'] = "".join(sky_result.ListControl(searchDepth = 11,foundIndex = 9).TextControl(foundIndex = 3).Name.split())
            result_dict['Sky Drive'] = sky_drive  
            break
        except:
            time.sleep(1)
      
    time.sleep(180)
    
    #api
    while(1):
        try:
            auto.HyperlinkControl(searchDepth= 8,Name = 'BENCHMARKS').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').Click()
            auto.TextControl(searchDepth = 11,Name = 'Benchmarks').SendKeys('{Down 30}')
            auto.TextControl(searchDepth = 14,Name = 'API Overhead feature test').Click()
            time.sleep(2)
            auto.HyperlinkControl(searchDepth = 15,Name = 'RUN').Click()
            break
        except:
            time.sleep(1)
         
    while(1):
        try:
            if not auto.TextControl(searchDepth = 11,Name = 'Running benchmark').Exists():
                break
        except:
            time.sleep(3)
    
    
    api_score = {}

    while(1):
        try:  
            api_result = auto.GroupControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')
               
            api_score['DirectX 11 multi-thread'] = "".join(api_result.ListControl(searchDepth = 11,foundIndex = 1).TextControl(foundIndex = 3).Name.split())
            api_score['DirectX 11 single-thread'] = "".join(api_result.ListControl(searchDepth = 11,foundIndex = 2).TextControl(foundIndex = 3).Name.split())
            api_score['DirectX 12'] = "".join(api_result.ListControl(searchDepth = 11,foundIndex = 3).TextControl(foundIndex = 3).Name.split())
            api_score['Vulkan'] = "".join(api_result.ListControl(searchDepth = 11,foundIndex = 4).TextControl(foundIndex = 3).Name.split())
            result_dict['api'] = api_score
            break
            
        except:
            api_result = auto.CustomControl(searchDepth = 10,AutomationId = 'RESULT_SINGLE')       
            api_score['DirectX 11 multi-thread'] = "".join(api_result.ListControl(searchDepth = 11,foundIndex = 1).TextControl(foundIndex = 3).Name.split())
            api_score['DirectX 11 single-thread'] = "".join(api_result.ListControl(searchDepth = 11,foundIndex = 2).TextControl(foundIndex = 3).Name.split())
            api_score['DirectX 12'] = "".join(api_result.ListControl(searchDepth = 11,foundIndex = 3).TextControl(foundIndex = 3).Name.split())
            api_score['Vulkan'] = "".join(api_result.ListControl(searchDepth = 11,foundIndex = 4).TextControl(foundIndex = 3).Name.split())
            result_dict['api'] = api_score  
            break
            
    #关闭窗口
    while(1):
        try:
            auto.PaneControl(searchDepth = 1,Name = '3DMark Professional Edition - Google Chrome').GetPattern(10009).Close()
            auto.WindowControl(Name = '3DMark Professional Edition',searchDepth = 1).GetWindowPattern().Close()
            break
        except:
            time.sleep(1)
    
    return result_dict
  

 
    
 

 
 
 
 
 
 
 
 
