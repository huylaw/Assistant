import subprocess
#import wmi
import subprocess as sp
import os
import sys
import webbrowser

paths = {
    'word': "C:\Program Files\Microsoft Office\Office16\WINWORD.EXE",
    'discord': "C:\\Users\LUONG VAN LAM\\AppData\\Local\\Discord\\app-1.0.9004\\Discord.exe",
    'calculator': "C:\Windows\System32\calc.exe",
    'excel': "C:\Program Files\Microsoft Office\Office16\EXCEL.EXE",
    'powerpoint':"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE"
}

def isContain(text, list):
	for word in list:
		if word in text:
			return True
	return False

def openFile(text):
	if isContain(text, ["ppt","power point","powerpoint"]):
		os.startfile(paths['powerpoint'])
	elif isContain(text, ['excel','spreadsheet']):
		os.startfile(paths['excel'])
	elif isContain(text, ['word','document']):
		os.startfile(paths['word'])
	elif isContain(text, ['discord']):
		os.startfile(paths['discord'])
	elif isContain(text, ['máy tính']):
		os.startfile(paths['calculator'])
	elif isContain(text, ['command prompt','cmd']):
		os.system('start cmd')
	elif isContain(text, ['camera','máy ảnh']):
		sp.run('start microsoft.windows.camera:', shell=True)
	return "Phần mềm đã được mở"

