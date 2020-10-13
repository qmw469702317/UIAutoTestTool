#！python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import ctypes
import uiautomation as auto


def _cinebenchr20_run():

    run_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    run_path += '//Performance Benchmark Tool//CinebenchR20//'
    
    #通过命令行安装，不使用strat以让程序阻塞
    os.chdir(run_path)
    os.system('run.bat')
      
           
        
        
    
    
    filename = run_path+'temp.txt'
    
    result_dict = {}
    temp_str = 'CB '
    with open(filename) as read_file:
        for line in read_file:
            if temp_str in line:
                line = line.replace(temp_str,'')
                line = line.replace('(0.00)','')
                result_dict['CpuX_Score'] = "".join(line.split())
                return result_dict
                break
                
     
     
     

