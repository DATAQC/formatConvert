import tkinter as tk
from tkinter import filedialog
import sys
import csv_mangler as cm

default_stdout =sys.stdout
default_stderr = sys.stderr

# This is GUI for CSV_Mangler
class GUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.initialize()
        self.childWindow = None

    def initialize(self):    
        # Open File
        self.buttonOpen = tk.Button(self, text=str.center('Browse ...',25), command = self.click_openFile)
        self.buttonOpen.grid(row=0,column=0,sticky = 'EWSN')
        
        # Choose Tool
        self.groupRadioTemplate = tk.Radiobutton(self, text=str.center('Split by Size',25), value=1,indicatoron=0,command = self.click_window_splitBySize)
        self.groupRadioTemplate.grid(row=2,column=0,sticky='EWSN')
        self.groupRadioTemplate = tk.Radiobutton(self, text=str.center('Split by Batchcode',25), value=2,indicatoron=0,command = self.click_window_splitByBatchcode)
        self.groupRadioTemplate.grid(row=3,column=0,sticky='EWSN')
        self.groupRadioTemplate = tk.Radiobutton(self, text=str.center('Covert to MultiUp',25), value=3,indicatoron=0,command = self.click_window_convertToMultiUp)
        self.groupRadioTemplate.grid(row=4,column=0,sticky='EWSN')
        self.groupRadioTemplate = tk.Radiobutton(self, text=str.center('Split by Size + MultiUp',25), value=4,indicatoron=0,command = self.click_window_splitAndMultiUp)
        self.groupRadioTemplate.grid(row=5,column=0,sticky='EWSN')
        self.groupRadioTemplate = tk.Radiobutton(self, text=str.center('Split by BatchCode + MultiUp',25), value=5,indicatoron=0,command = self.click_window_splitAndMultiUp2)
        self.groupRadioTemplate.grid(row=6,column=0,sticky='EWSN')

        # Signature
        self.labelSignature = tk.Label(self,text = 'By: QCDATA')
        self.labelSignature.grid(row=7,column=0,sticky='WS')            

        # FAQ
        self.buttonFAQ = tk.Button(self,text=str.center('?',3),command = self.click_FAQ)
        self.buttonFAQ.grid(row=7,column=0,sticky = 'SE')

        # ScrollBar for status window
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row = 0, rowspan = 8, column = 3, stick = 'NS')

        # Status window
        self.textStatusWindow = tk.Text(self, height=25, width=100,yscrollcommand = self.scrollbar.set)
        self.textStatusWindow.grid(row = 0, rowspan = 8,column = 1,columnspan = 2)
        self.scrollbar.config(command = self.textStatusWindow.yview)

        # redirect stdout and stderr to our status window
        sys.stdout = TextRedirector(self.textStatusWindow, "stdout")
        sys.stderr = TextRedirector(self.textStatusWindow, "stderr")

    def click_openFile(self):
        self.inputFileName = tk.filedialog.askopenfilename()
        print('Input File: ',self.inputFileName)

    def click_splitBySize(self):
        cm.printStatus('  Starting Process  ')
        cm.splitDFIntoChunks(self.inputFileName,cm.getOutputPath(self.inputFileName),self.chunkSize)
        cm.printStatus('  Process Completed  ')

    def click_splitByBatchCode(self):
        cm.printStatus('  Starting Process  ')
        cm.exportByBatchcode(self.inputFileName,cm.getOutputPath(self.inputFileName),self.batchCode)
        cm.printStatus('  Process Completed  ')

    def click_convertToMultiUp(self):
        cm.printStatus('  Starting Process  ')
        cm.convertToMultiUp(self.inputFileName,cm.getOutputPath(self.inputFileName), self.multiUpCount)    
        cm.printStatus('  Process Completed  ')
    
    def click_splitAndMultiUp(self):
        cm.printStatus('  Starting Process  ')
        cm.splitAndMultiUp(self.inputFileName,cm.getOutputPath(self.inputFileName),self.chunkSize,self.batchCode,self.multiUpCount,option ='bySize')    
        cm.printStatus('  Process Completed  ')

    def click_splitAndMultiUp2(self):
        cm.printStatus('  Starting Process  ')
        cm.splitAndMultiUp(self.inputFileName,cm.getOutputPath(self.inputFileName),self.chunkSize,self.batchCode,self.multiUpCount,option ='byBatchCode')    
        cm.printStatus('  Process Completed  ')

    def click_FAQ(self):
        self.topLevelFAQ = tk.Toplevel(self)
        faq = '''
        Only work for comma delimited txt or csv files at the moment.

        Split by size - Split a file into mutiple files by user defined count of records

        Split by batchcode - Split a file into mutiple files by grouping same values in the user defined column 

        Covert to Multiup - rearranging a file into multiUp formats for printing on a large sheet of paper

        Split + Multiup - split a file into smaller files and then covert them all to MultiUP
        '''
        self.topLevelFAQMessage = tk.Message(self.topLevelFAQ,text=faq)
        self.topLevelFAQMessage.pack()    
    
    def click_window_splitBySize(self):
        self.childWindow = window_splitBySize(self)

    def click_window_splitByBatchcode(self):
        self.chilWindow = window_splitByBatchCode(self)

    def click_window_convertToMultiUp(self):
        self.childWindow = window_convertToMultiUp(self)

    def click_window_splitAndMultiUp(self):
        self.childWindow = window_splitAndMultiUp(self)
        
    def click_window_splitAndMultiUp2(self): 
        self.childWindow = window_splitAndMultiUp2(self)

    def set_chunkSize(self,chunkSize):
        self.chunkSize = chunkSize

    def set_batchCode(self,batchCode):
        self.batchCode = batchCode

    def set_multiUpCount(self,multiUpCount):
        self.multiUpCount = multiUpCount

    def set_splitOption(self,splitOption):
        self.splitOption = splitOption

class window_splitBySize(tk.Frame):
    def __init__(self, master):                                                                     
        self.master = master
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)

        self.labelLine = tk.Label(self.frame,text ='Please enter chunk size: ')
        self.labelLine.pack()

        self.intChunkSize =  tk.IntVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.intChunkSize,width=6)
        self.entrySize.pack()

        self.buttonOK = tk.Button(self.frame, text = 'OK', width = 6, command = self.on_OK)
        self.buttonOK.pack(side='left')
        
        self.buttonCancel = tk.Button(self.frame, text = 'Cancel', width = 6, command = self.on_Cancel)
        self.buttonCancel.pack()
        self.frame.pack(side='right')

    def on_OK(self):
        self.master.set_chunkSize(self.intChunkSize.get())
        self.master.click_splitBySize()
        self.newWindow.destroy()

    def on_Cancel(self):
        self.newWindow.destroy()

class window_splitByBatchCode(tk.Frame):
    def __init__(self, master):                                                                     
        self.master = master
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)

        self.labelLine = tk.Label(self.frame,text ='Please enter batchcode: ')
        self.labelLine.pack()

        self.stringBatchCode =  tk.StringVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.stringBatchCode,width=12)
        self.entrySize.pack()

        self.buttonOK = tk.Button(self.frame, text = 'OK', width = 6, command = self.on_OK)
        self.buttonOK.pack(side='left')
        
        self.buttonCancel = tk.Button(self.frame, text = 'Cancel', width = 6, command = self.on_Cancel)
        self.buttonCancel.pack()
        self.frame.pack(side='right')
    
    def on_OK(self):
        self.master.set_batchCode(self.stringBatchCode.get())
        self.master.click_splitByBatchCode()
        self.newWindow.destroy()

    def on_Cancel(self):
        self.newWindow.destroy()

class window_convertToMultiUp(tk.Frame):
    def __init__(self, master):                                                                 
        self.master = master
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)

        self.labelLine = tk.Label(self.frame,text ='Please enter how many UP\'s ')
        self.labelLine.pack()

        self.intMultiUpCount =  tk.IntVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.intMultiUpCount,width=6)
        self.entrySize.pack()

        self.buttonOK = tk.Button(self.frame, text = 'OK', width = 6, command = self.on_OK)
        self.buttonOK.pack(side='left')

        self.buttonCancel = tk.Button(self.frame, text = 'Cancel', width = 6, command = self.on_Cancel)
        self.buttonCancel.pack()
        self.frame.pack(side='right')
    
    def on_OK(self):
        self.master.set_multiUpCount(self.intMultiUpCount.get())
        self.master.click_convertToMultiUp()
        self.newWindow.destroy()

    def on_Cancel(self):
        self.newWindow.destroy()

class window_splitAndMultiUp(tk.Frame):
    def __init__(self, master):                                                                 
        self.master = master
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)

        self.labelLine = tk.Label(self.frame,text ='Please enter chunk size: ')
        self.labelLine.pack()

        self.intChunkSize =  tk.IntVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.intChunkSize,width=6)
        self.entrySize.pack()

        self.labelLine2 = tk.Label(self.frame,text ='Please enter batchcode: ')
        self.labelLine2.pack()

        self.stringBatchCode =  tk.StringVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.stringBatchCode,width=12)
        self.entrySize.pack()

        self.labelLine3 = tk.Label(self.frame,text ='Please enter how many UP\'s ')
        self.labelLine3.pack()

        self.intMultiUpCount =  tk.IntVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.intMultiUpCount,width=6)
        self.entrySize.pack()

        self.buttonOK = tk.Button(self.frame, text = 'OK', width = 6, command = self.on_OK)
        self.buttonOK.pack(side='left')

        self.buttonCancel = tk.Button(self.frame, text = 'Cancel', width = 6, command = self.on_Cancel)
        self.buttonCancel.pack()
        self.frame.pack(side='right')
    
    def on_OK(self):
        self.master.set_chunkSize(self.intChunkSize.get())
        self.master.set_batchCode(self.stringBatchCode.get())
        self.master.set_multiUpCount(self.intMultiUpCount.get())
        self.master.click_splitAndMultiUp()
        self.newWindow.destroy()

    def on_Cancel(self):
        self.newWindow.destroy()

class window_splitAndMultiUp2(tk.Frame):
    def __init__(self, master):                                                                 
        self.master = master
        self.newWindow = tk.Toplevel(self.master)
        self.frame = tk.Frame(self.newWindow)

        self.labelLine = tk.Label(self.frame,text ='Please enter chunk size: ')
        self.labelLine.pack()

        self.intChunkSize =  tk.IntVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.intChunkSize,width=6)
        self.entrySize.pack()

        self.labelLine2 = tk.Label(self.frame,text ='Please enter batchcode: ')
        self.labelLine2.pack()

        self.stringBatchCode =  tk.StringVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.stringBatchCode,width=12)
        self.entrySize.pack()

        self.labelLine3 = tk.Label(self.frame,text ='Please enter how many UP\'s ')
        self.labelLine3.pack()

        self.intMultiUpCount =  tk.IntVar()
        self.entrySize = tk.Entry(self.frame,textvariable=self.intMultiUpCount,width=6)
        self.entrySize.pack()

        self.buttonOK = tk.Button(self.frame, text = 'OK', width = 6, command = self.on_OK)
        self.buttonOK.pack(side='left')

        self.buttonCancel = tk.Button(self.frame, text = 'Cancel', width = 6, command = self.on_Cancel)
        self.buttonCancel.pack()
        self.frame.pack(side='right')
    
    def on_OK(self):
        self.master.set_chunkSize(self.intChunkSize.get())
        self.master.set_batchCode(self.stringBatchCode.get())
        self.master.set_multiUpCount(self.intMultiUpCount.get())
        self.master.click_splitAndMultiUp2()

        self.newWindow.destroy()

    def on_Cancel(self):
        self.newWindow.destroy()
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")

def main():
    root = tk.Tk()
    GUI(root).pack()
    root.mainloop()

    sys.stdout = default_stdout 
    sys.stderr = default_stderr

if __name__ == '__main__':
    main()
