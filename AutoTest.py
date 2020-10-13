#！python_3
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import ctypes
import uiautomation as auto
import _3dmark 
import _3dmark11
import cinebenchr20
import crystaldiskmark
import geekbench4
import passmark9
import pcmark10
import csv
import wx
from comtypes.gen.UIAutomationClient import *


class MyFrame(wx.Frame):
    def __init__(self,parent,id):
       wx.Frame.__init__(self,parent,id,'AutotestTool',size = (500,400))
       self.Center()
       panel = wx.Panel(self)
       
       #创建运行按钮
       self.runButton = wx.Button(panel,label = '运行')
       self.runButton.Bind(wx.EVT_BUTTON,self.OnClickRun)
       #复选框，程序名称，次数填写
       self.checkbox_all = wx.CheckBox(panel,-1,"测试项目")
       self.checkbox_all.Bind(wx.EVT_CHECKBOX,self.OnCheck)
       self.label_times = wx.StaticText(panel,label = "请输入测试次数")
       self.text_all = wx.TextCtrl(panel,-1,"2",style = wx.TE_LEFT)
       self.text_all.Bind(wx.EVT_TEXT,self.OnText)
       self.checkbox_3DMark11 = wx.CheckBox(panel,-1,"3DMark11")
       self.checkbox_3DMark = wx.CheckBox(panel,-1,"3DMark")
       #增加3DMark版本
       #self.checkbox_3DMark11_new = wx.CheckBox(panel,-1,"3DMark11_new")
       #self.checkbox_3DMark_new = wx.CheckBox(panel,-1,"3DMark_new")
       
       self.checkbox_PCMark10 = wx.CheckBox(panel,-1,"PCMark10")
       self.checkbox_CineBenchR20 = wx.CheckBox(panel,-1,"CineBenchR20")
       self.checkbox_PassMark9 = wx.CheckBox(panel,-1,"PassMark9")
       self.checkbox_CryStalDiskMark = wx.CheckBox(panel,-1,"CryStalDiskMark")
       self.checkbox_GeekBench4 = wx.CheckBox(panel,-1,"GeekBench4")   
       #测试模式选择
       self.label_model = wx.StaticText(panel,label = "测试模式")
       self.checkbox_ACmodel = wx.CheckBox(panel,-1,"AC模式")
       self.checkbox_DCmodel = wx.CheckBox(panel,-1,"DC模式")
       self.checkbox_ACmodel.SetValue(True)
       self.checkbox_DCmodel.SetValue(True)
       #测试等待时间
       self.label_waitTime = wx.StaticText(panel,label = "请输入每次测试等待时间(单位s)")
       self.text_waitTime = wx.TextCtrl(panel,-1,"300",style = wx.TE_LEFT)
       self.text_waitTime.Bind(wx.EVT_TEXT,self.OnTextWaitTime)
       #添加容器，控件按横向并排排列
       hsizer_run = wx.BoxSizer(wx.HORIZONTAL)
       hsizer_run.Add(self.label_times, proportion = 0,flag=wx.ALL, border = 5)
       hsizer_run.Add(self.text_all, proportion = 0,flag=wx.ALL, border = 5)
       hsizer_run.Add(self.runButton, proportion = 0,flag=wx.ALL, border = 5)
       
       hsizer_model = wx.BoxSizer(wx.HORIZONTAL)
       hsizer_model.Add(self.label_model,proportion = 0,flag=wx.ALL, border = 5)
       hsizer_model.Add(self.checkbox_ACmodel,proportion = 0,flag=wx.ALL, border = 5)
       hsizer_model.Add(self.checkbox_DCmodel,proportion = 0,flag=wx.ALL, border = 5)
       
       hsizer_waittime = wx.BoxSizer(wx.HORIZONTAL)
       hsizer_waittime.Add(self.label_waitTime,proportion = 0,flag=wx.ALL, border = 5)
       hsizer_waittime.Add(self.text_waitTime,proportion = 0,flag=wx.ALL, border = 5)
       #添加容器，控件按纵向并排排列
       vsizer_all = wx.BoxSizer(wx.VERTICAL)
       vsizer_all.Add(self.checkbox_all,proportion = 0,flag = wx.LEFT |wx.EXPAND|wx.TOP,border = 45)
       vsizer_all.Add(self.checkbox_3DMark11,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       vsizer_all.Add(self.checkbox_3DMark,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       
       # vsizer_all.Add(self.checkbox_3DMark11_new,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       # vsizer_all.Add(self.checkbox_3DMark_new,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       vsizer_all.Add(self.checkbox_PCMark10,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       vsizer_all.Add(self.checkbox_CineBenchR20,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       vsizer_all.Add(self.checkbox_PassMark9,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       vsizer_all.Add(self.checkbox_CryStalDiskMark,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       vsizer_all.Add(self.checkbox_GeekBench4,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 45)
       vsizer_all.Add(hsizer_model,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 43)
       vsizer_all.Add(hsizer_waittime,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 43)
       vsizer_all.Add(hsizer_run,proportion = 0,flag =wx.LEFT |wx.EXPAND,border = 43)
       panel.SetSizer(vsizer_all)
       
           
    def OnText(self,event):
        message = ""
        run_times = self.text_all.GetValue()
        try:
            if run_times == "":
                return 
            temp_times = int(run_times)
            if temp_times > 0 and temp_times <= 100:
                return
            else:
                message = "请输入1到100之间的数字"
        except:
            message = '请输入1到100之间的数字'
            
        self.text_all.SetValue("2")    
        wx.MessageBox(message)
        
    #按下运行之后执行
    def OnClickRun(self,event):
        #获取等待时间,保存目录为桌面
        if self.text_waitTime.GetValue()=="":
            message = "等待时间不可为空"
            wx.MessageBox(message)
            return 
        wait_time = int(self.text_waitTime.GetValue())
        test_times = int(self.text_all.GetValue())
        save_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        message = ""
        
        #安装
        
        if self.checkbox_3DMark.IsChecked():
            _3dmark._3dmark_setup()
            
        # if self.checkbox_3DMark11_new.IsChecked():
            # _3dmark11_n._3dmark11_setup_n()
            
        # if self.checkbox_3DMark_new.IsChecked():
            # _3dmark_n._3dmark_setup_n()
            
        if self.checkbox_3DMark11.IsChecked():
            _3dmark11._3dmark11_setup()
            
        if self.checkbox_GeekBench4.IsChecked():    
            geekbench4._geekbench4_setup()
        
        if self.checkbox_PassMark9.IsChecked():
            passmark9._passmark9_setup()
        
        if self.checkbox_PCMark10.IsChecked():
            pcmark10._pcmark10_setup()
        
        #保存的文件名
        #如果选择了AC模式
        if self.checkbox_ACmodel.IsChecked():
            result_file =  save_path + '\\ACresult.csv'
            f = open(result_file,'w',newline = '',encoding = 'utf-8')
            csv_write = csv.writer(f)
            f.close()
            result_ac = {}     
            #如果选择了3DMark11
            if self.checkbox_3DMark11.IsChecked():
                #将每一行标题写入字典列表
                result_ac['3DMark11']={}
                result_ac['3DMark11']['Score'] = ['[3DMark11]']
                result_ac['3DMark11']['Graphics Score']=['_Graphics Score']
                result_ac['3DMark11']['Physics Score']=['_Physics Score']
                result_ac['3DMark11']['Combined Score']=['_Combined Score']
                result_ac['3DMark11']['GT1']=['_GT1']
                result_ac['3DMark11']['GT2']=['_GT2']
                result_ac['3DMark11']['GT3']=['_GT3']
                result_ac['3DMark11']['GT4']=['_GT4']
                result_ac['3DMark11']['PT']=['_PT']
                result_ac['3DMark11']['CT']=['_CT']

                for i in range(test_times):
                    try:
                        temp_ac=_3dmark11._3dmark11_run()
                        result_ac['3DMark11']['Score'].append(temp_ac['Score'])
                        result_ac['3DMark11']['Graphics Score'].append(temp_ac['Graphics Score'])
                        result_ac['3DMark11']['Physics Score'].append(temp_ac['Physics Score'])
                        result_ac['3DMark11']['Combined Score'].append(temp_ac['Combined Score'])
                        result_ac['3DMark11']['GT1'].append(temp_ac['GT1'])
                        result_ac['3DMark11']['GT2'].append(temp_ac['GT2'])
                        result_ac['3DMark11']['GT3'].append(temp_ac['GT3'])
                        result_ac['3DMark11']['GT4'].append(temp_ac['GT4'])
                        result_ac['3DMark11']['PT'].append(temp_ac['PT'])
                        result_ac['3DMark11']['CT'].append(temp_ac['CT'])
                    except:
                        print('第%d次运行3DMark11失败' %i)
                    
                    time.sleep(wait_time)
                 
                 
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                               
                #循环结束，将字典写入文件
                csv_write.writerow(result_ac['3DMark11']['Score'])
                csv_write.writerow(result_ac['3DMark11']['Graphics Score'])
                csv_write.writerow(result_ac['3DMark11']['Physics Score'])
                csv_write.writerow(result_ac['3DMark11']['Combined Score'])
                csv_write.writerow(result_ac['3DMark11']['GT1'])
                csv_write.writerow(result_ac['3DMark11']['GT2'])
                csv_write.writerow(result_ac['3DMark11']['GT3'])
                csv_write.writerow(result_ac['3DMark11']['GT4'])
                csv_write.writerow(result_ac['3DMark11']['PT'])
                csv_write.writerow(result_ac['3DMark11']['CT'])
                f.close()  
                
                
            #如果选择了3DMark    
            if self.checkbox_3DMark.IsChecked():
                result_ac['3DMark']={}
                result_ac['3DMark']['[3DMark]'] = ['[3DMark]']
                result_ac['3DMark']['_Time Spy']=['_Time Spy']
                result_ac['3DMark']['.Graphics Score1']=['.Graphics Score']
                result_ac['3DMark']['.CPU score1']=['.CPU score']
                result_ac['3DMark']['_Fire Strike']=['_Fire Strike']
                result_ac['3DMark']['.Graphics score2']=['.Graphics score']
                result_ac['3DMark']['.Physics score2']=['.Physics score']
                result_ac['3DMark']['.Combined score2']=['.Combined score']
                result_ac['3DMark']['_Night Raid']=['_Night Raid']
                result_ac['3DMark']['.Graphics score3']=['.Graphics score']
                result_ac['3DMark']['.CPU score3']=['.CPU score']
                result_ac['3DMark']['_Sky Drive']=['_Sky Drive']
                result_ac['3DMark']['.Graphics score4']=['.Graphics score']
                result_ac['3DMark']['.Physics score4']=['.Physics score']
                result_ac['3DMark']['.Combined score4']=['.Combined score']
                result_ac['3DMark']['_API']=['_API']
                result_ac['3DMark']['.DirectX 11 multi-thread5']=['.DirectX 11 multi-thread']
                result_ac['3DMark']['.DirectX 11 single-thread5']=['.DirectX 11 single-thread']
                result_ac['3DMark']['.DirectX 12']=['.DirectX 12']
                result_ac['3DMark']['.Vulkan5']=['.Vulkan']
                
                for i in range(test_times):
                    try:
                        temp_ac=_3dmark._3dmark_run()
                        print(temp_ac)
                        result_ac['3DMark']['_Time Spy'].append(temp_ac['Time Spy']['Score'])
                        result_ac['3DMark']['.Graphics Score1'].append(temp_ac['Time Spy']['Graphics Score'])
                        result_ac['3DMark']['.CPU score1'].append(temp_ac['Time Spy']['CPU score'])
                        
                        result_ac['3DMark']['_Fire Strike'].append(temp_ac['Fire Strike']['Score'])
                        result_ac['3DMark']['.Graphics score2'].append(temp_ac['Fire Strike']['Graphics score'])
                        result_ac['3DMark']['.Physics score2'].append(temp_ac['Fire Strike']['Physics score'])
                        result_ac['3DMark']['.Combined score2'].append(temp_ac['Fire Strike']['Combined score'])
                        
                        result_ac['3DMark']['_Night Raid'].append(temp_ac['Night Raid']['Score'])
                        result_ac['3DMark']['.Graphics score3'].append(temp_ac['Night Raid']['Graphics score'])
                        result_ac['3DMark']['.CPU score3'].append(temp_ac['Night Raid']['CPU score'])
                        
                        result_ac['3DMark']['_Sky Drive'].append(temp_ac['Sky Drive']['Score'])
                        result_ac['3DMark']['.Graphics score4'].append(temp_ac['Sky Drive']['Graphics score'])
                        result_ac['3DMark']['.Physics score4'].append(temp_ac['Sky Drive']['Physics score'])
                        result_ac['3DMark']['.Combined score4'].append(temp_ac['Sky Drive']['Combined score'])
                       
                        result_ac['3DMark']['.DirectX 11 multi-thread5'].append(temp_ac['api']['DirectX 11 multi-thread'])
                        result_ac['3DMark']['.DirectX 11 single-thread5'].append(temp_ac['api']['DirectX 11 single-thread'])
                        result_ac['3DMark']['.DirectX 12'].append(temp_ac['api']['DirectX 12'])
                        result_ac['3DMark']['.Vulkan5'].append(temp_ac['api']['Vulkan'])

                    except:
                        print('第%d次运行3DMark失败' %i)
                        
                    time.sleep(wait_time)
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)                
                #循环结束，将字典写入文件
                csv_write.writerow(result_ac['3DMark']['[3DMark]'])
                csv_write.writerow(result_ac['3DMark']['_Time Spy'])
                csv_write.writerow(result_ac['3DMark']['.Graphics Score1'])
                csv_write.writerow(result_ac['3DMark']['.CPU score1'])
                csv_write.writerow(result_ac['3DMark']['_Fire Strike'])
                csv_write.writerow(result_ac['3DMark']['.Graphics score2'])
                csv_write.writerow(result_ac['3DMark']['.Physics score2'])
                csv_write.writerow(result_ac['3DMark']['.Combined score2'])
                csv_write.writerow(result_ac['3DMark']['_Night Raid'])
                csv_write.writerow(result_ac['3DMark']['.Graphics score3'])
                csv_write.writerow(result_ac['3DMark']['.CPU score3'])
                csv_write.writerow(result_ac['3DMark']['_Sky Drive'])
                csv_write.writerow(result_ac['3DMark']['.Graphics score4'])
                csv_write.writerow(result_ac['3DMark']['.Physics score4'])
                csv_write.writerow(result_ac['3DMark']['.Combined score4'])
                csv_write.writerow(result_ac['3DMark']['_API'])
                csv_write.writerow(result_ac['3DMark']['.DirectX 11 multi-thread5'])
                csv_write.writerow(result_ac['3DMark']['.DirectX 11 single-thread5'])
                csv_write.writerow(result_ac['3DMark']['.DirectX 12'])
                csv_write.writerow(result_ac['3DMark']['.Vulkan5'])
                f.close()  
                

            result_ac = {} 
            # #如果选择了3DMark11
            # if self.checkbox_3DMark11_new.IsChecked():
                # #将每一行标题写入字典列表
                # result_ac['3DMark11']={}
                # result_ac['3DMark11']['Score'] = ['[3DMark11_new]']
                # result_ac['3DMark11']['Graphics Score']=['_Graphics Score']
                # result_ac['3DMark11']['Physics Score']=['_Physics Score']
                # result_ac['3DMark11']['Combined Score']=['_Combined Score']
                # result_ac['3DMark11']['GT1']=['_GT1']
                # result_ac['3DMark11']['GT2']=['_GT2']
                # result_ac['3DMark11']['GT3']=['_GT3']
                # result_ac['3DMark11']['GT4']=['_GT4']
                # result_ac['3DMark11']['PT']=['_PT']
                # result_ac['3DMark11']['CT']=['_CT']

                # for i in range(test_times):
                    # try:
                        # temp_ac=_3dmark11_n._3dmark11_run_n()
                        # result_ac['3DMark11']['Score'].append(temp_ac['Score'])
                        # result_ac['3DMark11']['Graphics Score'].append(temp_ac['Graphics Score'])
                        # result_ac['3DMark11']['Physics Score'].append(temp_ac['Physics Score'])
                        # result_ac['3DMark11']['Combined Score'].append(temp_ac['Combined Score'])
                        # result_ac['3DMark11']['GT1'].append(temp_ac['GT1'])
                        # result_ac['3DMark11']['GT2'].append(temp_ac['GT2'])
                        # result_ac['3DMark11']['GT3'].append(temp_ac['GT3'])
                        # result_ac['3DMark11']['GT4'].append(temp_ac['GT4'])
                        # result_ac['3DMark11']['PT'].append(temp_ac['PT'])
                        # result_ac['3DMark11']['CT'].append(temp_ac['CT'])
                    # except:
                        # print('第%d次运行3DMark11失败' %i)
                    
                    # time.sleep(wait_time)
                 
                 
                # f = open(result_file,'a',newline = '',encoding = 'utf-8')
                # csv_write = csv.writer(f)
                               
                # #循环结束，将字典写入文件
                # csv_write.writerow(result_ac['3DMark11']['Score'])
                # csv_write.writerow(result_ac['3DMark11']['Graphics Score'])
                # csv_write.writerow(result_ac['3DMark11']['Physics Score'])
                # csv_write.writerow(result_ac['3DMark11']['Combined Score'])
                # csv_write.writerow(result_ac['3DMark11']['GT1'])
                # csv_write.writerow(result_ac['3DMark11']['GT2'])
                # csv_write.writerow(result_ac['3DMark11']['GT3'])
                # csv_write.writerow(result_ac['3DMark11']['GT4'])
                # csv_write.writerow(result_ac['3DMark11']['PT'])
                # csv_write.writerow(result_ac['3DMark11']['CT'])
                # f.close()  
                
                
            # #如果选择了3DMark    
            # if self.checkbox_3DMark_new.IsChecked():
                # result_ac['3DMark']={}
                # result_ac['3DMark']['[3DMark]'] = ['[3DMark_new]']
                # result_ac['3DMark']['_Time Spy']=['_Time Spy']
                # result_ac['3DMark']['.Graphics Score1']=['.Graphics Score']
                # result_ac['3DMark']['.CPU score1']=['.CPU score']
                # result_ac['3DMark']['_Fire Strike']=['_Fire Strike']
                # result_ac['3DMark']['.Graphics score2']=['.Graphics score']
                # result_ac['3DMark']['.Physics score2']=['.Physics score']
                # result_ac['3DMark']['.Combined score2']=['.Combined score']
                # result_ac['3DMark']['_Night Raid']=['_Night Raid']
                # result_ac['3DMark']['.Graphics score3']=['.Graphics score']
                # result_ac['3DMark']['.CPU score3']=['.CPU score']
                # result_ac['3DMark']['_Sky Drive']=['_Sky Drive']
                # result_ac['3DMark']['.Graphics score4']=['.Graphics score']
                # result_ac['3DMark']['.Physics score4']=['.Physics score']
                # result_ac['3DMark']['.Combined score4']=['.Combined score']
                # result_ac['3DMark']['_API']=['_API']
                # result_ac['3DMark']['.DirectX 11 multi-thread5']=['.DirectX 11 multi-thread']
                # result_ac['3DMark']['.DirectX 11 single-thread5']=['.DirectX 11 single-thread']
                # result_ac['3DMark']['.DirectX 12']=['.DirectX 12']
                # result_ac['3DMark']['.Vulkan5']=['.Vulkan']
                
                # for i in range(test_times):
                    # try:
                        # temp_ac=_3dmark_n._3dmark_run_n()
                        # print(temp_ac)
                        # result_ac['3DMark']['_Time Spy'].append(temp_ac['Time Spy']['Score'])
                        # result_ac['3DMark']['.Graphics Score1'].append(temp_ac['Time Spy']['Graphics Score'])
                        # result_ac['3DMark']['.CPU score1'].append(temp_ac['Time Spy']['CPU score'])
                        
                        # result_ac['3DMark']['_Fire Strike'].append(temp_ac['Fire Strike']['Score'])
                        # result_ac['3DMark']['.Graphics score2'].append(temp_ac['Fire Strike']['Graphics score'])
                        # result_ac['3DMark']['.Physics score2'].append(temp_ac['Fire Strike']['Physics score'])
                        # result_ac['3DMark']['.Combined score2'].append(temp_ac['Fire Strike']['Combined score'])
                        
                        # result_ac['3DMark']['_Night Raid'].append(temp_ac['Night Raid']['Score'])
                        # result_ac['3DMark']['.Graphics score3'].append(temp_ac['Night Raid']['Graphics score'])
                        # result_ac['3DMark']['.CPU score3'].append(temp_ac['Night Raid']['CPU score'])
                        
                        # result_ac['3DMark']['_Sky Drive'].append(temp_ac['Sky Drive']['Score'])
                        # result_ac['3DMark']['.Graphics score4'].append(temp_ac['Sky Drive']['Graphics score'])
                        # result_ac['3DMark']['.Physics score4'].append(temp_ac['Sky Drive']['Physics score'])
                        # result_ac['3DMark']['.Combined score4'].append(temp_ac['Sky Drive']['Combined score'])
                       
                        # result_ac['3DMark']['.DirectX 11 multi-thread5'].append(temp_ac['api']['DirectX 11 multi-thread'])
                        # result_ac['3DMark']['.DirectX 11 single-thread5'].append(temp_ac['api']['DirectX 11 single-thread'])
                        # result_ac['3DMark']['.DirectX 12'].append(temp_ac['api']['DirectX 12'])
                        # result_ac['3DMark']['.Vulkan5'].append(temp_ac['api']['Vulkan'])

                    # except:
                        # print('第%d次运行3DMarkn失败' %i)
                        
                    # time.sleep(wait_time)
                
                # f = open(result_file,'a',newline = '',encoding = 'utf-8')
                # csv_write = csv.writer(f)                
                # #循环结束，将字典写入文件
                # csv_write.writerow(result_ac['3DMark']['[3DMark]'])
                # csv_write.writerow(result_ac['3DMark']['_Time Spy'])
                # csv_write.writerow(result_ac['3DMark']['.Graphics Score1'])
                # csv_write.writerow(result_ac['3DMark']['.CPU score1'])
                # csv_write.writerow(result_ac['3DMark']['_Fire Strike'])
                # csv_write.writerow(result_ac['3DMark']['.Graphics score2'])
                # csv_write.writerow(result_ac['3DMark']['.Physics score2'])
                # csv_write.writerow(result_ac['3DMark']['.Combined score2'])
                # csv_write.writerow(result_ac['3DMark']['_Night Raid'])
                # csv_write.writerow(result_ac['3DMark']['.Graphics score3'])
                # csv_write.writerow(result_ac['3DMark']['.CPU score3'])
                # csv_write.writerow(result_ac['3DMark']['_Sky Drive'])
                # csv_write.writerow(result_ac['3DMark']['.Graphics score4'])
                # csv_write.writerow(result_ac['3DMark']['.Physics score4'])
                # csv_write.writerow(result_ac['3DMark']['.Combined score4'])
                # csv_write.writerow(result_ac['3DMark']['_API'])
                # csv_write.writerow(result_ac['3DMark']['.DirectX 11 multi-thread5'])
                # csv_write.writerow(result_ac['3DMark']['.DirectX 11 single-thread5'])
                # csv_write.writerow(result_ac['3DMark']['.DirectX 12'])
                # csv_write.writerow(result_ac['3DMark']['.Vulkan5'])
                # f.close()  
                

            #如果选择PCMark10
            if self.checkbox_PCMark10.IsChecked():
                #将每一行标题写入字典列表
                result_ac['PCMark10']={}
                result_ac['PCMark10']['[PCMark10]'] = ['[PCMark10]']
                
                result_ac['PCMark10']['_Essentials']=['_Essentials']
                result_ac['PCMark10']['.App Start-up Score']=['.App Start-up Score']
                result_ac['PCMark10']['.Video Conferencing Score']=['.Video Conferencing Score']
                result_ac['PCMark10']['.Web Browsing Score']=['.Web Browsing Score']
                
                result_ac['PCMark10']['_Productivity']=['_Productivity']
                result_ac['PCMark10']['.Spreadsheets Score']=['.Spreadsheets Score']
                result_ac['PCMark10']['.Writing Score']=['.Writing Score']
                
                result_ac['PCMark10']['_Digital Content Creation']=['_Digital Content Creation']
                result_ac['PCMark10']['.Photo Editing Score']=['.Photo Editing Score']
                result_ac['PCMark10']['.Rendering and Visualization Score']=['.Rendering and Visualization Score']
                result_ac['PCMark10']['.Video Editing Score']=['.Video Editing Score']
                
                result_ac['PCMark10']['_Gaming']=['_Gaming']
                result_ac['PCMark10']['.Graphics score']=['.Graphics score']
                result_ac['PCMark10']['.Physics score']=['.Physics score']
                result_ac['PCMark10']['.Combined score']=['.Combined score']

                for i in range(test_times):
                    try:
                        temp_ac=pcmark10._pcmark10_run()
                        result_ac['PCMark10']['[PCMark10]'].append(temp_ac['Score'])
                        result_ac['PCMark10']['_Essentials'].append(temp_ac['Essentials'])
                        result_ac['PCMark10']['.App Start-up Score'].append(temp_ac['App Start-up Score'])
                        result_ac['PCMark10']['.Video Conferencing Score'].append(temp_ac['Video Conferencing Score'])
                        result_ac['PCMark10']['.Web Browsing Score'].append(temp_ac['Web Browsing Score'])
                        
                        result_ac['PCMark10']['_Productivity'].append(temp_ac['Productivity'])
                        result_ac['PCMark10']['.Spreadsheets Score'].append(temp_ac['Spreadsheets Score'])
                        result_ac['PCMark10']['.Writing Score'].append(temp_ac['Writing Score'])
                        
                        result_ac['PCMark10']['_Digital Content Creation'].append(temp_ac['Digital Content Creation'])
                        result_ac['PCMark10']['.Photo Editing Score'].append(temp_ac['Photo Editing Score'])
                        result_ac['PCMark10']['.Rendering and Visualization Score'].append(temp_ac['Rendering and Visualization Score'])
                        result_ac['PCMark10']['.Video Editing Score'].append(temp_ac['Video Editing Score'])
                        
                        result_ac['PCMark10']['_Gaming'].append(temp_ac['Gaming'])
                        result_ac['PCMark10']['.Graphics score'].append(temp_ac['Graphics score'])
                        result_ac['PCMark10']['.Physics score'].append(temp_ac['Physics score'])
                        result_ac['PCMark10']['.Combined score'].append(temp_ac['Combined score'])

                    except:
                        print('第%d次运行PCMark10失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f) 
                #循环结束，将字典写入文件
                csv_write.writerow(result_ac['PCMark10']['[PCMark10]'])
                
                csv_write.writerow(result_ac['PCMark10']['_Essentials'])
                csv_write.writerow(result_ac['PCMark10']['.App Start-up Score'])
                csv_write.writerow(result_ac['PCMark10']['.Video Conferencing Score'])
                csv_write.writerow(result_ac['PCMark10']['.Web Browsing Score'])
                
                csv_write.writerow(result_ac['PCMark10']['_Productivity'])
                csv_write.writerow(result_ac['PCMark10']['.Spreadsheets Score'])
                csv_write.writerow(result_ac['PCMark10']['.Writing Score'])
                
                csv_write.writerow(result_ac['PCMark10']['_Digital Content Creation'])
                csv_write.writerow(result_ac['PCMark10']['.Photo Editing Score'])
                csv_write.writerow(result_ac['PCMark10']['.Rendering and Visualization Score'])
                csv_write.writerow(result_ac['PCMark10']['.Video Editing Score'])
                
                csv_write.writerow(result_ac['PCMark10']['_Gaming'])
                csv_write.writerow(result_ac['PCMark10']['.Graphics score'])
                csv_write.writerow(result_ac['PCMark10']['.Physics score'])
                csv_write.writerow(result_ac['PCMark10']['.Combined score'])
                f.close()  
                
                
            #如果选择了CineBenchR20
            if self.checkbox_CineBenchR20.IsChecked():
                #将每一行标题写入字典列表
                result_ac['CineBenchR20']={}
                result_ac['CineBenchR20']['Score'] = ['[CineBenchR20]']
               

                for i in range(test_times):
                    try:
                        temp_ac=cinebenchr20._cinebenchr20_run()
                        result_ac['CineBenchR20']['Score'].append(temp_ac['CpuX_Score'])
                   
                    except:
                        print('第%d次运行CineBenchR20失败' %i)
                    
                    time.sleep(wait_time)
                    
        
                #循环结束，将字典写入文件
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f) 
                csv_write.writerow(result_ac['CineBenchR20']['Score'])
                f.close()  
           
            #如果选择了CrystalDiskMark
            if self.checkbox_CryStalDiskMark.IsChecked():
                #将每一行标题写入字典列表
                result_ac['CrystalDiskMark']={}
                result_ac['CrystalDiskMark']['[CrystalDiskMark]'] = ['[CrystalDiskMark]']
                result_ac['CrystalDiskMark']['_Seq_Q32T1_Read']=['_Seq_Q32T1_Read']
                result_ac['CrystalDiskMark']['_Seq_Q32T1_Write']=['_Seq_Q32T1_Write']
                result_ac['CrystalDiskMark']['_4KiB_Q8T8_Read']=['_4KiB_Q8T8_Read']
                result_ac['CrystalDiskMark']['_4KiB_Q8T8_Write']=['_4KiB_Q8T8_Write']
                result_ac['CrystalDiskMark']['_4KiB_Q32T1_Read']=['_4KiB_Q32T1_Read']
                result_ac['CrystalDiskMark']['_4KiB_Q32T1_Write']=['_4KiB_Q32T1_Write']
                result_ac['CrystalDiskMark']['_4KiB_Q1T1_Read']=['_4KiB_Q1T1_Read']
                result_ac['CrystalDiskMark']['_4KiB_Q1T1_Write']=['_4KiB_Q1T1_Write']
        

                for i in range(test_times):
                    try:
                        temp_ac=crystaldiskmark._crystaldiskmark_run()
                        result_ac['CrystalDiskMark']['[CrystalDiskMark]'].append('MB/S')
                        result_ac['CrystalDiskMark']['_Seq_Q32T1_Read'].append(temp_ac['Seq_Q32T1_Read'])
                        result_ac['CrystalDiskMark']['_Seq_Q32T1_Write'].append(temp_ac['Seq_Q32T1_Write'])
                        result_ac['CrystalDiskMark']['_4KiB_Q8T8_Read'].append(temp_ac['4KiB_Q8T8_Read'])
                        result_ac['CrystalDiskMark']['_4KiB_Q8T8_Write'].append(temp_ac['4KiB_Q8T8_Write'])
                        result_ac['CrystalDiskMark']['_4KiB_Q32T1_Read'].append(temp_ac['4KiB_Q32T1_Read'])
                        result_ac['CrystalDiskMark']['_4KiB_Q32T1_Write'].append(temp_ac['4KiB_Q32T1_Write'])
                        result_ac['CrystalDiskMark']['_4KiB_Q1T1_Read'].append(temp_ac['4KiB_Q1T1_Read'])
                        result_ac['CrystalDiskMark']['_4KiB_Q1T1_Write'].append(temp_ac['4KiB_Q1T1_Write'])
                      
                    except:
                        print('第%d次运行CrystalDiskMark失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f) 
                #循环结束，将字典写入文件
                csv_write.writerow(result_ac['CrystalDiskMark']['[CrystalDiskMark]'])
                csv_write.writerow(result_ac['CrystalDiskMark']['_Seq_Q32T1_Read'])
                csv_write.writerow(result_ac['CrystalDiskMark']['_Seq_Q32T1_Write'])
                csv_write.writerow(result_ac['CrystalDiskMark']['_4KiB_Q8T8_Read'])
                csv_write.writerow(result_ac['CrystalDiskMark']['_4KiB_Q8T8_Write'])
                csv_write.writerow(result_ac['CrystalDiskMark']['_4KiB_Q32T1_Read'])
                csv_write.writerow(result_ac['CrystalDiskMark']['_4KiB_Q32T1_Write'])
                csv_write.writerow(result_ac['CrystalDiskMark']['_4KiB_Q1T1_Read'])
                csv_write.writerow(result_ac['CrystalDiskMark']['_4KiB_Q1T1_Write'])
                f.close()  
                
            #如果选择PassMark9
            if self.checkbox_PassMark9.IsChecked():
                #将每一行标题写入字典列表
                result_ac['PassMark9']={}
                result_ac['PassMark9']['[PassMark9]'] = ['[PassMark9]']
                result_ac['PassMark9']['_PassMark Rating']=['_PassMark Rating']
                result_ac['PassMark9']['_CPU Mark']=['_CPU Mark']
                result_ac['PassMark9']['_3D Graphics Mark']=['_3D Graphics Mark']
                result_ac['PassMark9']['_Disk Mark']=['_Disk Mark']
                result_ac['PassMark9']['_2D Graphics Mark']=['_2D Graphics Mark']
                result_ac['PassMark9']['_Memory Mark']=['_Memory Mark']
       
                for i in range(test_times):
                    try:
                        temp_ac=passmark9._passmark9_run()
                        result_ac['PassMark9']['_PassMark Rating'].append(temp_ac['PassMark Rating'])
                    
                        result_ac['PassMark9']['_CPU Mark'].append(temp_ac['CPU Mark'])
                        result_ac['PassMark9']['_3D Graphics Mark'].append(temp_ac['3D Graphics Mark'])
                        result_ac['PassMark9']['_Disk Mark'].append(temp_ac['Disk Mark'])
                        result_ac['PassMark9']['_2D Graphics Mark'].append(temp_ac['2D Graphics Mark'])
                        result_ac['PassMark9']['_Memory Mark'].append(temp_ac['Memory Mark'])
                 
                    except:
                        print('第%d次运行PassMark9失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f) 
                #循环结束，将字典写入文件
                csv_write.writerow(result_ac['PassMark9']['[PassMark9]'])
   
                csv_write.writerow(result_ac['PassMark9']['_PassMark Rating'])
                csv_write.writerow(result_ac['PassMark9']['_CPU Mark'])
                csv_write.writerow(result_ac['PassMark9']['_3D Graphics Mark'])
                csv_write.writerow(result_ac['PassMark9']['_Disk Mark'])
                csv_write.writerow(result_ac['PassMark9']['_2D Graphics Mark'])
                csv_write.writerow(result_ac['PassMark9']['_Memory Mark'])
                f.close()  
                

            #如果选择GeekBench4
            if self.checkbox_GeekBench4.IsChecked():
                #将每一行标题写入字典列表
                result_ac['GeekBench4']={}
                result_ac['GeekBench4']['[GeekBench4]'] = ['[GeekBench4]']
                result_ac['GeekBench4']['_Single-Core Score']=['_Single-Core Score']
                result_ac['GeekBench4']['_Multi-Core Score']=['_Multi-Core Score']
       
                for i in range(test_times):
                    try:
                        temp_ac=geekbench4._geekbench4_run()
                        result_ac['GeekBench4']['_Single-Core Score'].append(temp_ac['Single-Core Score'])
                    
                        result_ac['GeekBench4']['_Multi-Core Score'].append(temp_ac['Multi-Core Score'])
                 
                    except:
                        print('第%d次运行GeekBench4失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                #循环结束，将字典写入文件
                csv_write.writerow(result_ac['GeekBench4']['[GeekBench4]'])
   
                csv_write.writerow(result_ac['GeekBench4']['_Single-Core Score'])
                csv_write.writerow(result_ac['GeekBench4']['_Multi-Core Score'])
                f.close()  
   
     
     
     
        if self.checkbox_DCmodel.IsChecked():
            run_bat = os.path.join(os.path.expanduser("~"), 'Desktop')
            run_bat = run_bat+'//Performance Benchmark Tool 2020316//SABIInvoker//'
            os.chdir(run_bat)
            os.system('start SetBatteryEmulationMode.bat')
            
            result_file =  save_path + '\\DCresult.csv'
            f = open(result_file,'w',newline = '',encoding = 'utf-8')
            csv_write = csv.writer(f)
            f.close()  
            result_dc = {}       
                
            if self.checkbox_3DMark11.IsChecked():
                #将每一行标题写入字典列表
                result_dc['3DMark11']={}
                result_dc['3DMark11']['Score'] = ['[3DMark11]']
                result_dc['3DMark11']['Graphics Score']=['_Graphics Score']
                result_dc['3DMark11']['Physics Score']=['_Physics Score']
                result_dc['3DMark11']['Combined Score']=['_Combined Score']
                result_dc['3DMark11']['GT1']=['_GT1']
                result_dc['3DMark11']['GT2']=['_GT2']
                result_dc['3DMark11']['GT3']=['_GT3']
                result_dc['3DMark11']['GT4']=['_GT4']
                result_dc['3DMark11']['PT']=['_PT']
                result_dc['3DMark11']['CT']=['_CT']

                for i in range(test_times):
                    try:
                        temp_ac=_3dmark11._3dmark11_run()
                        result_dc['3DMark11']['Score'].append(temp_ac['Score'])
                        result_dc['3DMark11']['Graphics Score'].append(temp_ac['Graphics Score'])
                        result_dc['3DMark11']['Physics Score'].append(temp_ac['Physics Score'])
                        result_dc['3DMark11']['Combined Score'].append(temp_ac['Combined Score'])
                        result_dc['3DMark11']['GT1'].append(temp_ac['GT1'])
                        result_dc['3DMark11']['GT2'].append(temp_ac['GT2'])
                        result_dc['3DMark11']['GT3'].append(temp_ac['GT3'])
                        result_dc['3DMark11']['GT4'].append(temp_ac['GT4'])
                        result_dc['3DMark11']['PT'].append(temp_ac['PT'])
                        result_dc['3DMark11']['CT'].append(temp_ac['CT'])
                    except:
                        print('第%d次运行3DMark11失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                #循环结束，将字典写入文件
                csv_write.writerow(result_dc['3DMark11']['Score'])
                csv_write.writerow(result_dc['3DMark11']['Graphics Score'])
                csv_write.writerow(result_dc['3DMark11']['Physics Score'])
                csv_write.writerow(result_dc['3DMark11']['Combined Score'])
                csv_write.writerow(result_dc['3DMark11']['GT1'])
                csv_write.writerow(result_dc['3DMark11']['GT2'])
                csv_write.writerow(result_dc['3DMark11']['GT3'])
                csv_write.writerow(result_dc['3DMark11']['GT4'])
                csv_write.writerow(result_dc['3DMark11']['PT'])
                csv_write.writerow(result_dc['3DMark11']['CT'])
                f.close()  
                
            #如果选择了3DMark    
            if self.checkbox_3DMark.IsChecked():
                result_dc['3DMark']={}
                result_dc['3DMark']['[3DMark]'] = ['[3DMark]']
                result_dc['3DMark']['_Time Spy']=['_Time Spy']
                result_dc['3DMark']['.Graphics Score1']=['.Graphics Score']
                result_dc['3DMark']['.CPU score1']=['.CPU score']
                result_dc['3DMark']['_Fire Strike']=['_Fire Strike']
                result_dc['3DMark']['.Graphics score2']=['.Graphics score']
                result_dc['3DMark']['.Physics score2']=['.Physics score']
                result_dc['3DMark']['.Combined score2']=['.Combined score']
                result_dc['3DMark']['_Night Raid']=['_Night Raid']
                result_dc['3DMark']['.Graphics score3']=['.Graphics score']
                result_dc['3DMark']['.CPU score3']=['.CPU score']
                result_dc['3DMark']['_Sky Drive']=['_Sky Drive']
                result_dc['3DMark']['.Graphics score4']=['.Graphics score']
                result_dc['3DMark']['.Physics score4']=['.Physics score']
                result_dc['3DMark']['.Combined score4']=['.Combined score']
                result_dc['3DMark']['_API']=['_API']
                result_dc['3DMark']['.DirectX 11 multi-thread5']=['.DirectX 11 multi-thread']
                result_dc['3DMark']['.DirectX 11 single-thread5']=['.DirectX 11 single-thread']
                result_dc['3DMark']['.DirectX 12']=['.DirectX 12']
                result_dc['3DMark']['.Vulkan5']=['.Vulkan']
                
                for i in range(test_times):
                    try:
                        temp_ac=_3dmark._3dmark_run()
                        result_dc['3DMark']['_Time Spy'].append(temp_ac['Time Spy']['Score'])
                        result_dc['3DMark']['.Graphics Score1'].append(temp_ac['Time Spy']['Graphics Score'])
                        result_dc['3DMark']['.CPU score1'].append(temp_ac['Time Spy']['CPU score'])
                        result_dc['3DMark']['_Fire Strike'].append(temp_ac['Fire Strike']['Score'])
                        result_dc['3DMark']['.Graphics score2'].append(temp_ac['Fire Strike']['Graphics score'])
                        result_dc['3DMark']['.Physics score2'].append(temp_ac['Fire Strike']['Physics score'])
                        result_dc['3DMark']['.Combined score2'].append(temp_ac['Fire Strike']['Combined score'])
                        result_dc['3DMark']['_Night Raid'].append(temp_ac['Night Raid']['Score'])
                        result_dc['3DMark']['.Graphics score3'].append(temp_ac['Night Raid']['Graphics score'])
                        result_dc['3DMark']['.CPU score3'].append(temp_ac['Night Raid']['CPU score'])
                        result_dc['3DMark']['_Sky Drive'].append(temp_ac['Sky Drive']['Score'])
                        result_dc['3DMark']['.Graphics score4'].append(temp_ac['Sky Drive']['Graphics score'])
                        result_dc['3DMark']['.Physics score4'].append(temp_ac['Sky Drive']['Physics score'])
                        result_dc['3DMark']['.Combined score4'].append(temp_ac['Sky Drive']['Combined score'])
                       
                        result_dc['3DMark']['.DirectX 11 multi-thread5'].append(temp_ac['api']['DirectX 11 multi-thread'])
                        result_dc['3DMark']['.DirectX 11 single-thread5'].append(temp_ac['api']['DirectX 11 single-thread'])
                        result_dc['3DMark']['.DirectX 12'].append(temp_ac['api']['DirectX 12'])
                        result_dc['3DMark']['.Vulkan5'].append(temp_ac['api']['Vulkan'])

                    except:
                        print('第%d次运行3DMark失败' %i)
                        
                    time.sleep(wait_time)
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                #循环结束，将字典写入文件
                csv_write.writerow(result_dc['3DMark']['[3DMark]'])
                csv_write.writerow(result_dc['3DMark']['_Time Spy'])
                csv_write.writerow(result_dc['3DMark']['.Graphics Score1'])
                csv_write.writerow(result_dc['3DMark']['.CPU score1'])
                csv_write.writerow(result_dc['3DMark']['_Fire Strike'])
                csv_write.writerow(result_dc['3DMark']['.Graphics score2'])
                csv_write.writerow(result_dc['3DMark']['.Physics score2'])
                csv_write.writerow(result_dc['3DMark']['.Combined score2'])
                csv_write.writerow(result_dc['3DMark']['_Night Raid'])
                csv_write.writerow(result_dc['3DMark']['.Graphics score3'])
                csv_write.writerow(result_dc['3DMark']['.CPU score3'])
                csv_write.writerow(result_dc['3DMark']['_Sky Drive'])
                csv_write.writerow(result_dc['3DMark']['.Graphics score4'])
                csv_write.writerow(result_dc['3DMark']['.Physics score4'])
                csv_write.writerow(result_dc['3DMark']['.Combined score4'])
                csv_write.writerow(result_dc['3DMark']['_API'])
                csv_write.writerow(result_dc['3DMark']['.DirectX 11 multi-thread5'])
                csv_write.writerow(result_dc['3DMark']['.DirectX 11 single-thread5'])
                csv_write.writerow(result_dc['3DMark']['.DirectX 12'])
                csv_write.writerow(result_dc['3DMark']['.Vulkan5'])
                f.close()  

            result_dc = {}      
            # if self.checkbox_3DMark11_new.IsChecked():
                # #将每一行标题写入字典列表
                # result_dc['3DMark11']={}
                # result_dc['3DMark11']['Score'] = ['[3DMark11_new]']
                # result_dc['3DMark11']['Graphics Score']=['_Graphics Score']
                # result_dc['3DMark11']['Physics Score']=['_Physics Score']
                # result_dc['3DMark11']['Combined Score']=['_Combined Score']
                # result_dc['3DMark11']['GT1']=['_GT1']
                # result_dc['3DMark11']['GT2']=['_GT2']
                # result_dc['3DMark11']['GT3']=['_GT3']
                # result_dc['3DMark11']['GT4']=['_GT4']
                # result_dc['3DMark11']['PT']=['_PT']
                # result_dc['3DMark11']['CT']=['_CT']

                # for i in range(test_times):
                    # try:
                        # temp_ac=_3dmark11_n._3dmark11_run_n()
                        # result_dc['3DMark11']['Score'].append(temp_ac['Score'])
                        # result_dc['3DMark11']['Graphics Score'].append(temp_ac['Graphics Score'])
                        # result_dc['3DMark11']['Physics Score'].append(temp_ac['Physics Score'])
                        # result_dc['3DMark11']['Combined Score'].append(temp_ac['Combined Score'])
                        # result_dc['3DMark11']['GT1'].append(temp_ac['GT1'])
                        # result_dc['3DMark11']['GT2'].append(temp_ac['GT2'])
                        # result_dc['3DMark11']['GT3'].append(temp_ac['GT3'])
                        # result_dc['3DMark11']['GT4'].append(temp_ac['GT4'])
                        # result_dc['3DMark11']['PT'].append(temp_ac['PT'])
                        # result_dc['3DMark11']['CT'].append(temp_ac['CT'])
                    # except:
                        # print('第%d次运行3DMark11失败' %i)
                    
                    # time.sleep(wait_time)
                    
                
                # f = open(result_file,'a',newline = '',encoding = 'utf-8')
                # csv_write = csv.writer(f)
                # #循环结束，将字典写入文件
                # csv_write.writerow(result_dc['3DMark11']['Score'])
                # csv_write.writerow(result_dc['3DMark11']['Graphics Score'])
                # csv_write.writerow(result_dc['3DMark11']['Physics Score'])
                # csv_write.writerow(result_dc['3DMark11']['Combined Score'])
                # csv_write.writerow(result_dc['3DMark11']['GT1'])
                # csv_write.writerow(result_dc['3DMark11']['GT2'])
                # csv_write.writerow(result_dc['3DMark11']['GT3'])
                # csv_write.writerow(result_dc['3DMark11']['GT4'])
                # csv_write.writerow(result_dc['3DMark11']['PT'])
                # csv_write.writerow(result_dc['3DMark11']['CT'])
                # f.close()  
                
            # #如果选择了3DMark    
            # if self.checkbox_3DMark_new.IsChecked():
                # result_dc['3DMark']={}
                # result_dc['3DMark']['[3DMark]'] = ['[3DMark_new]']
                # result_dc['3DMark']['_Time Spy']=['_Time Spy']
                # result_dc['3DMark']['.Graphics Score1']=['.Graphics Score']
                # result_dc['3DMark']['.CPU score1']=['.CPU score']
                # result_dc['3DMark']['_Fire Strike']=['_Fire Strike']
                # result_dc['3DMark']['.Graphics score2']=['.Graphics score']
                # result_dc['3DMark']['.Physics score2']=['.Physics score']
                # result_dc['3DMark']['.Combined score2']=['.Combined score']
                # result_dc['3DMark']['_Night Raid']=['_Night Raid']
                # result_dc['3DMark']['.Graphics score3']=['.Graphics score']
                # result_dc['3DMark']['.CPU score3']=['.CPU score']
                # result_dc['3DMark']['_Sky Drive']=['_Sky Drive']
                # result_dc['3DMark']['.Graphics score4']=['.Graphics score']
                # result_dc['3DMark']['.Physics score4']=['.Physics score']
                # result_dc['3DMark']['.Combined score4']=['.Combined score']
                # result_dc['3DMark']['_API']=['_API']
                # result_dc['3DMark']['.DirectX 11 multi-thread5']=['.DirectX 11 multi-thread']
                # result_dc['3DMark']['.DirectX 11 single-thread5']=['.DirectX 11 single-thread']
                # result_dc['3DMark']['.DirectX 12']=['.DirectX 12']
                # result_dc['3DMark']['.Vulkan5']=['.Vulkan']
                
                # for i in range(test_times):
                    # try:
                        # temp_ac=_3dmark_n._3dmark_run_n()
                        # result_dc['3DMark']['_Time Spy'].append(temp_ac['Time Spy']['Score'])
                        # result_dc['3DMark']['.Graphics Score1'].append(temp_ac['Time Spy']['Graphics Score'])
                        # result_dc['3DMark']['.CPU score1'].append(temp_ac['Time Spy']['CPU score'])
                        # result_dc['3DMark']['_Fire Strike'].append(temp_ac['Fire Strike']['Score'])
                        # result_dc['3DMark']['.Graphics score2'].append(temp_ac['Fire Strike']['Graphics score'])
                        # result_dc['3DMark']['.Physics score2'].append(temp_ac['Fire Strike']['Physics score'])
                        # result_dc['3DMark']['.Combined score2'].append(temp_ac['Fire Strike']['Combined score'])
                        # result_dc['3DMark']['_Night Raid'].append(temp_ac['Night Raid']['Score'])
                        # result_dc['3DMark']['.Graphics score3'].append(temp_ac['Night Raid']['Graphics score'])
                        # result_dc['3DMark']['.CPU score3'].append(temp_ac['Night Raid']['CPU score'])
                        # result_dc['3DMark']['_Sky Drive'].append(temp_ac['Sky Drive']['Score'])
                        # result_dc['3DMark']['.Graphics score4'].append(temp_ac['Sky Drive']['Graphics score'])
                        # result_dc['3DMark']['.Physics score4'].append(temp_ac['Sky Drive']['Physics score'])
                        # result_dc['3DMark']['.Combined score4'].append(temp_ac['Sky Drive']['Combined score'])
                       
                        # result_dc['3DMark']['.DirectX 11 multi-thread5'].append(temp_ac['api']['DirectX 11 multi-thread'])
                        # result_dc['3DMark']['.DirectX 11 single-thread5'].append(temp_ac['api']['DirectX 11 single-thread'])
                        # result_dc['3DMark']['.DirectX 12'].append(temp_ac['api']['DirectX 12'])
                        # result_dc['3DMark']['.Vulkan5'].append(temp_ac['api']['Vulkan'])

                    # except:
                        # print('第%d次运行3DMark失败' %i)
                        
                    # time.sleep(wait_time)
                
                # f = open(result_file,'a',newline = '',encoding = 'utf-8')
                # csv_write = csv.writer(f)
                # #循环结束，将字典写入文件
                # csv_write.writerow(result_dc['3DMark']['[3DMark]'])
                # csv_write.writerow(result_dc['3DMark']['_Time Spy'])
                # csv_write.writerow(result_dc['3DMark']['.Graphics Score1'])
                # csv_write.writerow(result_dc['3DMark']['.CPU score1'])
                # csv_write.writerow(result_dc['3DMark']['_Fire Strike'])
                # csv_write.writerow(result_dc['3DMark']['.Graphics score2'])
                # csv_write.writerow(result_dc['3DMark']['.Physics score2'])
                # csv_write.writerow(result_dc['3DMark']['.Combined score2'])
                # csv_write.writerow(result_dc['3DMark']['_Night Raid'])
                # csv_write.writerow(result_dc['3DMark']['.Graphics score3'])
                # csv_write.writerow(result_dc['3DMark']['.CPU score3'])
                # csv_write.writerow(result_dc['3DMark']['_Sky Drive'])
                # csv_write.writerow(result_dc['3DMark']['.Graphics score4'])
                # csv_write.writerow(result_dc['3DMark']['.Physics score4'])
                # csv_write.writerow(result_dc['3DMark']['.Combined score4'])
                # csv_write.writerow(result_dc['3DMark']['_API'])
                # csv_write.writerow(result_dc['3DMark']['.DirectX 11 multi-thread5'])
                # csv_write.writerow(result_dc['3DMark']['.DirectX 11 single-thread5'])
                # csv_write.writerow(result_dc['3DMark']['.DirectX 12'])
                # csv_write.writerow(result_dc['3DMark']['.Vulkan5'])
                # f.close()  


            #如果选择PCMark10
            if self.checkbox_PCMark10.IsChecked():
                #将每一行标题写入字典列表
                result_dc['PCMark10']={}
                result_dc['PCMark10']['[PCMark10]'] = ['[PCMark10]']
                
                result_dc['PCMark10']['_Essentials']=['_Essentials']
                result_dc['PCMark10']['.App Start-up Score']=['.App Start-up Score']
                result_dc['PCMark10']['.Video Conferencing Score']=['.Video Conferencing Score']
                result_dc['PCMark10']['.Web Browsing Score']=['.Web Browsing Score']
                
                result_dc['PCMark10']['_Productivity']=['_Productivity']
                result_dc['PCMark10']['.Spreadsheets Score']=['.Spreadsheets Score']
                result_dc['PCMark10']['.Writing Score']=['.Writing Score']
                
                result_dc['PCMark10']['_Digital Content Creation']=['_Digital Content Creation']
                result_dc['PCMark10']['.Photo Editing Score']=['.Photo Editing Score']
                result_dc['PCMark10']['.Rendering and Visualization Score']=['.Rendering and Visualization Score']
                result_dc['PCMark10']['.Video Editing Score']=['.Video Editing Score']
                
                result_dc['PCMark10']['_Gaming']=['_Gaming']
                result_dc['PCMark10']['.Graphics score']=['.Graphics score']
                result_dc['PCMark10']['.Physics score']=['.Physics score']
                result_dc['PCMark10']['.Combined score']=['.Combined score']

                for i in range(test_times):
                    try:
                        temp_ac=pcmark10._pcmark10_run()
                        result_dc['PCMark10']['[PCMark10]'].append(temp_ac['Score'])
                        result_dc['PCMark10']['_Essentials'].append(temp_ac['Essentials'])
                        result_dc['PCMark10']['.App Start-up Score'].append(temp_ac['App Start-up Score'])
                        result_dc['PCMark10']['.Video Conferencing Score'].append(temp_ac['Video Conferencing Score'])
                        result_dc['PCMark10']['.Web Browsing Score'].append(temp_ac['Web Browsing Score'])
                        
                        result_dc['PCMark10']['_Productivity'].append(temp_ac['Productivity'])
                        result_dc['PCMark10']['.Spreadsheets Score'].append(temp_ac['Spreadsheets Score'])
                        result_dc['PCMark10']['.Writing Score'].append(temp_ac['Writing Score'])
                        
                        result_dc['PCMark10']['_Digital Content Creation'].append(temp_ac['Digital Content Creation'])
                        result_dc['PCMark10']['.Photo Editing Score'].append(temp_ac['Photo Editing Score'])
                        result_dc['PCMark10']['.Rendering and Visualization Score'].append(temp_ac['Rendering and Visualization Score'])
                        result_dc['PCMark10']['.Video Editing Score'].append(temp_ac['Video Editing Score'])
                        
                        result_dc['PCMark10']['_Gaming'].append(temp_ac['Gaming'])
                        result_dc['PCMark10']['.Graphics score'].append(temp_ac['Graphics score'])
                        result_dc['PCMark10']['.Physics score'].append(temp_ac['Physics score'])
                        result_dc['PCMark10']['.Combined score'].append(temp_ac['Combined score'])

                    except:
                        print('第%d次运行PCMark10失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                #循环结束，将字典写入文件
                csv_write.writerow(result_dc['PCMark10']['[PCMark10]'])
                
                csv_write.writerow(result_dc['PCMark10']['_Essentials'])
                csv_write.writerow(result_dc['PCMark10']['.App Start-up Score'])
                csv_write.writerow(result_dc['PCMark10']['.Video Conferencing Score'])
                csv_write.writerow(result_dc['PCMark10']['.Web Browsing Score'])
                
                csv_write.writerow(result_dc['PCMark10']['_Productivity'])
                csv_write.writerow(result_dc['PCMark10']['.Spreadsheets Score'])
                csv_write.writerow(result_dc['PCMark10']['.Writing Score'])
                
                csv_write.writerow(result_dc['PCMark10']['_Digital Content Creation'])
                csv_write.writerow(result_dc['PCMark10']['.Photo Editing Score'])
                csv_write.writerow(result_dc['PCMark10']['.Rendering and Visualization Score'])
                csv_write.writerow(result_dc['PCMark10']['.Video Editing Score'])
                
                csv_write.writerow(result_dc['PCMark10']['_Gaming'])
                csv_write.writerow(result_dc['PCMark10']['.Graphics score'])
                csv_write.writerow(result_dc['PCMark10']['.Physics score'])
                csv_write.writerow(result_dc['PCMark10']['.Combined score'])
                f.close()  
                
                
            #如果选择了CineBenchR20
            if self.checkbox_CineBenchR20.IsChecked():
                #将每一行标题写入字典列表
                result_dc['CineBenchR20']={}
                result_dc['CineBenchR20']['Score'] = ['[CineBenchR20]']
               

                for i in range(test_times):
                    try:
                        temp_ac=cinebenchr20._cinebenchr20_run()
                        result_dc['CineBenchR20']['Score'].append(temp_ac['CpuX_Score'])
                   
                    except:
                        print('第%d次运行CineBenchR20失败' %i)
                    
                    time.sleep(wait_time)
                    
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                #循环结束，将字典写入文件
                csv_write.writerow(result_dc['CineBenchR20']['Score'])
                f.close()  
                
           
            #如果选择了CrystalDiskMark
            if self.checkbox_CryStalDiskMark.IsChecked():
                #将每一行标题写入字典列表
                result_dc['CrystalDiskMark']={}
                result_dc['CrystalDiskMark']['[CrystalDiskMark]'] = ['[CrystalDiskMark]']
                result_dc['CrystalDiskMark']['_Seq_Q32T1_Read']=['_Seq_Q32T1_Read']
                result_dc['CrystalDiskMark']['_Seq_Q32T1_Write']=['_Seq_Q32T1_Write']
                result_dc['CrystalDiskMark']['_4KiB_Q8T8_Read']=['_4KiB_Q8T8_Read']
                result_dc['CrystalDiskMark']['_4KiB_Q8T8_Write']=['_4KiB_Q8T8_Write']
                result_dc['CrystalDiskMark']['_4KiB_Q32T1_Read']=['_4KiB_Q32T1_Read']
                result_dc['CrystalDiskMark']['_4KiB_Q32T1_Write']=['_4KiB_Q32T1_Write']
                result_dc['CrystalDiskMark']['_4KiB_Q1T1_Read']=['_4KiB_Q1T1_Read']
                result_dc['CrystalDiskMark']['_4KiB_Q1T1_Write']=['_4KiB_Q1T1_Write']
        

                for i in range(test_times):
                    try:
                        temp_ac=crystaldiskmark._crystaldiskmark_run()
                        result_dc['CrystalDiskMark']['[CrystalDiskMark]'].append('MB/S')
                        result_dc['CrystalDiskMark']['_Seq_Q32T1_Read'].append(temp_ac['Seq_Q32T1_Read'])
                        result_dc['CrystalDiskMark']['_Seq_Q32T1_Write'].append(temp_ac['Seq_Q32T1_Write'])
                        result_dc['CrystalDiskMark']['_4KiB_Q8T8_Read'].append(temp_ac['4KiB_Q8T8_Read'])
                        result_dc['CrystalDiskMark']['_4KiB_Q8T8_Write'].append(temp_ac['4KiB_Q8T8_Write'])
                        result_dc['CrystalDiskMark']['_4KiB_Q32T1_Read'].append(temp_ac['4KiB_Q32T1_Read'])
                        result_dc['CrystalDiskMark']['_4KiB_Q32T1_Write'].append(temp_ac['4KiB_Q32T1_Write'])
                        result_dc['CrystalDiskMark']['_4KiB_Q1T1_Read'].append(temp_ac['4KiB_Q1T1_Read'])
                        result_dc['CrystalDiskMark']['_4KiB_Q1T1_Write'].append(temp_ac['4KiB_Q1T1_Write'])
                      
                    except:
                        print('第%d次运行CrystalDiskMark失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                #循环结束，将字典写入文件
                csv_write.writerow(result_dc['CrystalDiskMark']['[CrystalDiskMark]'])
                csv_write.writerow(result_dc['CrystalDiskMark']['_Seq_Q32T1_Read'])
                csv_write.writerow(result_dc['CrystalDiskMark']['_Seq_Q32T1_Write'])
                csv_write.writerow(result_dc['CrystalDiskMark']['_4KiB_Q8T8_Read'])
                csv_write.writerow(result_dc['CrystalDiskMark']['_4KiB_Q8T8_Write'])
                csv_write.writerow(result_dc['CrystalDiskMark']['_4KiB_Q32T1_Read'])
                csv_write.writerow(result_dc['CrystalDiskMark']['_4KiB_Q32T1_Write'])
                csv_write.writerow(result_dc['CrystalDiskMark']['_4KiB_Q1T1_Read'])
                csv_write.writerow(result_dc['CrystalDiskMark']['_4KiB_Q1T1_Write'])
                f.close()  
                
            #如果选择PassMark9
            if self.checkbox_PassMark9.IsChecked():
                #将每一行标题写入字典列表
                result_dc['PassMark9']={}
                result_dc['PassMark9']['[PassMark9]'] = ['[PassMark9]']
                result_dc['PassMark9']['_PassMark Rating']=['_PassMark Rating']
                result_dc['PassMark9']['_CPU Mark']=['_CPU Mark']
                result_dc['PassMark9']['_3D Graphics Mark']=['_3D Graphics Mark']
                result_dc['PassMark9']['_Disk Mark']=['_Disk Mark']
                result_dc['PassMark9']['_2D Graphics Mark']=['_2D Graphics Mark']
                result_dc['PassMark9']['_Memory Mark']=['_Memory Mark']
       
                for i in range(test_times):
                    try:
                        temp_ac=passmark9._passmark9_run()
                        result_dc['PassMark9']['_PassMark Rating'].append(temp_ac['PassMark Rating'])
                    
                        result_dc['PassMark9']['_CPU Mark'].append(temp_ac['CPU Mark'])
                        result_dc['PassMark9']['_3D Graphics Mark'].append(temp_ac['3D Graphics Mark'])
                        result_dc['PassMark9']['_Disk Mark'].append(temp_ac['Disk Mark'])
                        result_dc['PassMark9']['_2D Graphics Mark'].append(temp_ac['2D Graphics Mark'])
                        result_dc['PassMark9']['_Memory Mark'].append(temp_ac['Memory Mark'])
                 
                    except:
                        print('第%d次运行PassMark9失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                #循环结束，将字典写入文件
                csv_write.writerow(result_dc['PassMark9']['[PassMark9]'])
   
                csv_write.writerow(result_dc['PassMark9']['_PassMark Rating'])
                csv_write.writerow(result_dc['PassMark9']['_CPU Mark'])
                csv_write.writerow(result_dc['PassMark9']['_3D Graphics Mark'])
                csv_write.writerow(result_dc['PassMark9']['_Disk Mark'])
                csv_write.writerow(result_dc['PassMark9']['_2D Graphics Mark'])
                csv_write.writerow(result_dc['PassMark9']['_Memory Mark'])
                f.close()  

            #如果选择GeekBench4
            if self.checkbox_GeekBench4.IsChecked():
                #将每一行标题写入字典列表
                result_dc['GeekBench4']={}
                result_dc['GeekBench4']['[GeekBench4]'] = ['[GeekBench4]']
                result_dc['GeekBench4']['_Single-Core Score']=['_Single-Core Score']
                result_dc['GeekBench4']['_Multi-Core Score']=['_Multi-Core Score']
       
                for i in range(test_times):
                    try:
                        temp_ac=geekbench4._geekbench4_run()
                        result_dc['GeekBench4']['_Single-Core Score'].append(temp_ac['Single-Core Score'])
                    
                        result_dc['GeekBench4']['_Multi-Core Score'].append(temp_ac['Multi-Core Score'])
                 
                    except:
                        print('第%d次运行GeekBench4失败' %i)
                    
                    time.sleep(wait_time)
                    
                
                f = open(result_file,'a',newline = '',encoding = 'utf-8')
                csv_write = csv.writer(f)
                #循环结束，将字典写入文件
                csv_write.writerow(result_dc['GeekBench4']['[GeekBench4]'])
   
                csv_write.writerow(result_dc['GeekBench4']['_Single-Core Score'])
                csv_write.writerow(result_dc['GeekBench4']['_Multi-Core Score'])
                f.close()  
  
       
            run_bat = os.path.join(os.path.expanduser("~"), 'Desktop')
            run_bat = run_bat+'//Performance Benchmark Tool 2020316//SABIInvoker//'
            os.chdir(run_bat)            
            os.system('start ClearBatteryEmulationMode.bat')
        
        message = "Test run out!!!"
        wx.MessageBox(message)

        
    def OnCheck(self,event):
        CheckValue = self.checkbox_all.GetValue()
        self.checkbox_3DMark11.SetValue(CheckValue)
        self.checkbox_3DMark.SetValue(CheckValue)
        self.checkbox_PCMark10.SetValue(CheckValue)
        self.checkbox_CineBenchR20.SetValue(CheckValue)
        self.checkbox_PassMark9.SetValue(CheckValue)
        self.checkbox_CryStalDiskMark.SetValue(CheckValue)
        self.checkbox_GeekBench4.SetValue(CheckValue)
       
    def OnTextWaitTime(self,event):
        message = ""
        wait_time = self.text_waitTime.GetValue()
        try:
            if wait_time == "":
                return
                
            temp_time = int(wait_time)
            if  temp_time > 0 :
                return
                
            else:
                message = "请输入大于0的数字作为等待时间！！！"
        except:
            message = '请输入大于0的数字作为等待时间！！！'
            
        self.text_waitTime.SetValue("300")    
        wx.MessageBox(message)
        
        
        
        
if __name__ == '__main__':
    app = wx.App(True,filename = "debug.txt")
    frame = MyFrame(parent = None, id = -1)
    frame.Show()
    app.MainLoop()
    
    
    