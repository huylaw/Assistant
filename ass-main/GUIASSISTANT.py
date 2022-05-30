#########################
# GLOBAL VARIABLES USED #
#########################
ai_name = 'P.A.N.D.A.'.lower()
EXIT_COMMANDS = ['tạm biệt','thoát','dừng chương trình','tắt chương trình']

language = 'vi'

ownerName = "Lý Tuấn Huy"
ownerDesignation = "Ngài"
ownerPhoto = "1"
rec_email, rec_phoneno = "", ""
WAEMEntry = None

avatarChoosen = 0
choosedAvtrImage = None

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1 #0 for light, 1 for dark

####################################### IMPORTING MODULES ###########################################
""" User Created Modules """
try:
	import normalChat
	import math_function
	import appControl
	import webScrapping
	import wikipedia
	from userHandler import UserData
	import timer
	import on_os
	import ToDo
	import fileHandler
	from random import choice
except Exception as e:
	raise e

""" System Modules """
try:
	import requests
	import os
	import speech_recognition as sr
	from tkinter import *
	from tkinter import ttk
	from tkinter import messagebox
	from tkinter import colorchooser
	from PIL import Image, ImageTk
	from time import sleep
	from threading import Thread
	import playsound
	from gtts import gTTS
	from until import opening_text,hello1_text,hello_text,voice,funny
	from on_os import get_weather_report,search_on_google,search_on_wikipedia,send_email,play_on_youtube,play_song,get_random_joke,find_my_ip,get_latest_news,get_random_advice,get_trending_movies,read_news_about,open_website

except Exception as e:
	print(e)

if os.path.exists('userData')==False:
	os.mkdir('userData')

wikipedia.set_lang('vi')
########################################## BOOT UP WINDOW ###########################################
def ChangeSettings(write=False):
	import pickle
	global background, textColor, chatBgColor,AITaskStatusLblBG, KCS_IMG, botChatTextBg, botChatText, userChatTextBg
	setting = {'background': background,
				'textColor': textColor,
				'chatBgColor': chatBgColor,
				'AITaskStatusLblBG': AITaskStatusLblBG,
				'KCS_IMG': KCS_IMG,
				'botChatText': botChatText,
				'botChatTextBg': botChatTextBg,
				'userChatTextBg': userChatTextBg,
			}
	if write:
		with open('userData/settings.pck', 'wb') as file:
			pickle.dump(setting, file)
		return
	try:
		with open('userData/settings.pck', 'rb') as file:
			loadSettings = pickle.load(file)
			background = loadSettings['background']
			textColor = loadSettings['textColor']
			chatBgColor = loadSettings['chatBgColor']
			AITaskStatusLblBG = loadSettings['AITaskStatusLblBG']
			KCS_IMG = loadSettings['KCS_IMG']
			botChatText = loadSettings['botChatText']
			botChatTextBg = loadSettings['botChatTextBg']
			userChatTextBg = loadSettings['userChatTextBg']
	except Exception as e:
		pass

if os.path.exists('userData/settings.pck')==False:
	ChangeSettings(True)
	
def getChatColor():
	global chatBgColor
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor

def changeTheme():
	global background, textColor, AITaskStatusLblBG, KCS_IMG, botChatText, botChatTextBg, userChatTextBg, chatBgColor
	if themeValue.get()==1:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#203647", "white", "#203647",1
		cbl['image'] = cblDarkImg
		kbBtn['image'] = kbphDark
		settingBtn['image'] = sphDark
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "white", "#007cc7", "#4da8da"
		chatBgColor = "#12232e"
		colorbar['bg'] = chatBgColor
	else:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#F6FAFB", "#303E54", "#14A769", 0
		cbl['image'] = cblLightImg
		kbBtn['image'] = kbphLight
		settingBtn['image'] = sphLight
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "#494949", "#EAEAEA", "#23AE79"
		chatBgColor = "#F6FAFB"
		colorbar['bg'] = '#E8EBEF'

	root['bg'], root2['bg'] = textColor, background
	settingsFrame['bg'] = background
	settingsLbl['fg'], userPhoto['fg'], userName['fg'], themeLbl['fg'], chooseChatLbl['fg'] = textColor, textColor, textColor, textColor, textColor
	settingsLbl['bg'], userPhoto['bg'], userName['bg'], themeLbl['bg'], chooseChatLbl['bg'] = background, background, background, background, background
	s.configure('Wild.TRadiobutton', background=background, foreground=textColor)
	chat_frame['bg'], root1['bg'] = chatBgColor, chatBgColor
	userPhoto['activebackground'] = background
	ChangeSettings(True)

ChangeSettings()

############################################ SET UP VOICE ###########################################


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
	AITaskStatusLbl['text'] = 'Nói...'
	if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)
	if display: attachTOframe(text, True)
	print('\n'+ai_name.upper()+': '+text)
	try:
		tts = gTTS(text=text, lang=language, slow=False)
		tts.save("sound.mp3")
		playsound.playsound("sound.mp3", True)
		os.remove("sound.mp3")
	except:
		print("Đừng cố làm gì khác...")

####################################### SET UP SPEECH TO TEXT #######################################
def record(clearChat=True, iconDisplay=True):
	print('\nPanda chờ nghe lệnh...')
	AITaskStatusLbl['text'] = 'Nghe lệnh...'
	r = sr.Recognizer()
	r.dynamic_energy_threshold = False
	r.energy_threshold = 4000
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		said = ""
		try:
			AITaskStatusLbl['text'] = 'Thực hiện...'

			said = r.recognize_google(audio,language='vi-VN')
			print(f"\nNgười cùng nói: {said}")
			if clearChat:
				clearChatScreen()
			if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(said)
		except Exception as e:
			print(e)
			# speak("I didn't get it, Say that again please...")
			if "connection failed" in str(e):
				speak("Hệ thống đang Offline...", True, True)
			return 'None'
	return said.lower()

def voiceMedium():
	speak("Xin chào tôi tên Panda. Tôi giúp gì được cho ngài?", True,True)
	while True:
		query = record()
		if query == 'None': continue
		if isContain(query, EXIT_COMMANDS):
			speak("Tạm biệt "+ownerDesignation+"!", True, True)
			break
		else: main(query.lower())
	appControl.Win_Opt('close')

def keyboardInput(e):
	user_input = UserField.get().lower()
	if user_input!="":
		clearChatScreen()
		if isContain(user_input, EXIT_COMMANDS):
			speak("Tạm biệt "+ownerDesignation+"!", True, True)
		else:
			Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(user_input.capitalize())
			Thread(target=main, args=(user_input,)).start()
		UserField.delete(0, END)

###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
	for word in lst:
		if word in txt:
			return True
	return False

def main(text):

		if "mở" in text and "phần mềm" in text:
			speak(choice(opening_text))
			speak(fileHandler.openFile(text), True, True)
			return

		if "làm tốt lắm" in text or "làm rất tốt" in text or "bạn thật tuyệt vời" in text:
			speak("Không có gì , tôi có thể giúp gì thêm cho ngài.",True)
			return

		if 'khỏe không' in text:
			speak(choice(hello1_text),True)
			c=record()
			if 'bình thường' in c or 'khỏe' in c or 'không sao' in c:
				speak('Vậy tôi giúp được gì cho ngài ạ!',True,True)
			return

		if 'giọng' in text and 'hay' in text:
			speak(choice(voice), True)
			return
		if 'bạn' in text and 'hài hước' in text:
			speak(choice(funny),True)
			return

		if "dịch" in text:
			speak("Ngài muốn dịch gì ạ?", True, True)
			sentence = record(False, False)
			#speak("Ngài muốn dịch sang ngôn ngữ gì?", True)
			#language = record(False, False)
			speak(choice(opening_text))
			result = normalChat.lang_translate(sentence)
			if result=="None":
				speak("Không có ngôn ngữ như thế ạ",True)
				return
			else:
				speak(result.pronunciation)
				speak(f"Trong tiếng Việt ngài sẽ nói:", True)
				#attachTOframe(result.text, True)
				
				speak(result.text, True)
			return

		if 'danh sách' in text:
			if isContain(text, ['thêm', 'tạo', 'thực hiện']):
				speak("Ngài muốn thêm gì ạ?", True, True)
				item = record(False, False)
				ToDo.toDoList(item)
				speak(choice(opening_text))
				speak("Tôi đã thêm vào danh sách cho ngài", True)
				return
			if isContain(text, ['xem', 'danh sách của tôi']):
				speak(choice(opening_text))
				items = ToDo.showtoDoList()
				if len(items)==1:
					speak(items[0], True, True)
					return
				attachTOframe('\n'.join(items), True)
				speak(items[0])
				return

		if isContain(text, ['pin']):
			speak(choice(opening_text))
			result = appControl.OSHandler(text)
			if len(result)==2:
				speak(result[0], True, True)
				attachTOframe(result[1], True)
			else:
				speak(result, True, True)
			return
			
		if isContain(text, ['google', 'tìm trên google', 'wiki','wikipidia']):
			speak(choice(opening_text))
			if 'tìm trên google' in text or 'google' in text:
				search_on_google(text)
				speak("Đây là kết quả tìm kiếm")
			else: speak(on_os.search_on_wikipedia(text))
			return

		if 'email' in text:
			speak('Ngài muốn gửi email tới ai?', True, True)
			WAEMPOPUP("Email", "E-mail Address")
			attachTOframe(rec_email)
			speak('Tiêu đề là gì ạ?', True)
			subject = record(False, False)
			speak('Nội dung ngài muốn gửi ?', True)
			message = record(False, False)

			speak(choice(opening_text))
			#Thread(target=webScrapping.email, args=(rec_email,message,subject,) ).start()
			print(webScrapping.email(rec_email,message,subject))
			speak('Email đã được gửi', True)
			return

		if isContain(text, ['youtube','video']):
			speak(f'Ngài muốn xem gì trên Youtube ạ?', True)
			video = record()
			#speak(choice(opening_text))
			speak(choice(opening_text))
			on_os.play_on_youtube(video)
			speak("Video ngài muốn đã được mở")
			return
			
		if isContain(text, ['bản đồ', 'chỉ đường']):
			if "chỉ đường" in text:
				speak('Vị trí bắt đầu của ngài?', True, True)
				startingPoint = record(False, False)
				speak("Vâng "+ownerDesignation+", điểm đến của ngài?", True)
				destinationPoint = record(False, False)
				speak("Vâng "+ownerDesignation+", đang lấy dữ liệu...", True)
				try:
					distance = webScrapping.giveDirections(startingPoint, destinationPoint)
					speak('Quãng đường ngài phải đi là '+ distance, True)
				except:
					speak("Vị trí không phù hợp, ngài hãy thử lại!")
			else:
				webScrapping.maps(text)
				speak('Của ngài đây...', True, True)
			return

		if isContain(text, ['phân số','log','giá trị của','tính',' + ',' - ',' x ','nhân','chia','nhị phân','thập lục phân','thập phân','cotan','sin ','cos ','tan ']):
			speak(choice(opening_text))
			text.lower
			try:
				speak(('Kết quả là: ' + math_function.perform(text)), True, True)
				return
			except Exception as e:
				return
			return

		if "truyện cười" in text or "chuyện cười" in text:
			speak(choice(opening_text))
			speak('Đây ạ...', True, True)
			speak(webScrapping.jokes(), True)
			return

		if isContain(text, ['tin tức']):
			speak(f"Ngài muốn đọc tin về gì.",True,True)
			query = record()
			speak(choice(opening_text))
			on_os.read_news_about(query)
			return

		if isContain(text, ['thời tiết']):
			speak(choice(opening_text))
			ip_address = find_my_ip()
			print(ip_address)
			city = requests.get(f'https://ipapi.co/{ip_address}/city/').text
			print(city)
			speak(f"Đang xem thời tiết tại {city}",True,True)
			pressure, temperature, feels_like = get_weather_report(city)
			speak(f"Nhiệt độ hiện tại là {temperature}, độ ẩm hiện tại là  {feels_like}, áp suất không khí hiện tại là  {pressure}",True)
			return

		if isContain(text, ['chụp màn hình']):
			speak(choice(opening_text))
			Thread(target=appControl.Win_Opt, args=('screenshot',)).start()
			speak("Ảnh màn hình đã được chụp và lưu tại ...\Files and Document", True, True)
			return

		if isContain(text, ['wiki', 'là ai']):
			speak(choice(opening_text))
			speak('Đang tìm kiếm...', True, True)
			result = webScrapping.wikiResult(text)
			speak(result)
			return
		
		if isContain(text, ['chơi game']):
			speak("Ngài có muốn chơi game online không?", True, True)
			text = record()
			if text=="None":
				speak("Ngài nói lại được không?", True, True)
				return
			if 'có' in text:
				speak("Vâng "+ownerDesignation+", ngài hãy chơi một số game online ", True, True)
				webScrapping.openWebsite('https://www.agame.com/games/mini-games/')
				return
			if isContain(text, ["không"]):
				speak("Không sao "+ownerDesignation+", chúng ta có thể chơi vào lần sau.", True, True)
			return
		
		if isContain(text, ['giờ','ngày']):
			speak(choice(opening_text))
			speak(normalChat.chat(text), True, True)
			return

		if 'tên của tôi' in text:
			speak('Ngài tên là ' + ownerName, True, True)
			return

		if "phim thịnh hành mới nhất" in text:
			speak(choice(opening_text))
			speak(f"Một vài phim thịnh hành là: {get_trending_movies()}",True,True)
			return 

		if isContain(text, ['buổi sáng','buổi chiều','buổi tối']) and 'chào' in text:
			speak(normalChat.chat("chào"), True, True)
			return

		if "lời khuyên" in text:
			speak(choice(opening_text))
			speak(f"Một lời khuyên cho ngài đây ạ",True,True)
			advice = get_random_advice()
			speak(advice)
			return
		result = normalChat.reply(text)
		if result != "None": speak(result, True, True)
		else:
			speak("Panda không hiểu ngài... ", True, True)
			speak("Đây là thứ tôi tìm được trên web... ", True, True)
			webScrapping.googleSearch(text) #uncomment this if you want to show the result on web, means if nothing found
		

##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
	result = messagebox.askquestion('Alert', 'Bạn có chắc là muốn thoát ?')
	if result=='no': return
	root.destroy()
						#####################
						####### GUI #########
						#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text,bot=False):
	if bot:
		botchat = Label(chat_frame,text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250, font=('Montserrat',12, 'bold'))
		botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)
	else:
		userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250, font=('Montserrat',12, 'bold'))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
	frame.tkraise()
	clearChatScreen()

############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
	global rec_phoneno, rec_email
	data = WAEMEntry.get()
	rec_email, rec_phoneno = data, data
	WAEMEntry.delete(0, END)
	appControl.Win_Opt('close')
def send(e):
	sendWAEM()

def WAEMPOPUP(Service='None', rec='Reciever'):
	global WAEMEntry
	PopUProot = Tk()
	PopUProot.title(f'{Service} Service')
	PopUProot.configure(bg='white')

	if Service=="WhatsApp": PopUProot.iconbitmap("extrafiles/images/whatsapp.ico")
	else: PopUProot.iconbitmap("extrafiles/images/email.ico")
	w_width, w_height = 410, 200
	s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	PopUProot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	Label(PopUProot, text=f'Reciever {rec}', font=('Arial', 16), bg='white').pack(pady=(20, 10))
	WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=('Arial', 12), justify='center', bg='#DCDCDC', width=30)
	WAEMEntry.pack()
	WAEMEntry.focus()

	SendBtn = Button(PopUProot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white', command=sendWAEM)
	SendBtn.pack(pady=20, ipadx=10)
	PopUProot.bind('<Return>', send)
	PopUProot.mainloop()

######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
	global chatBgColor
	myColor = colorchooser.askcolor()
	if myColor[1] is None: return
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor
	ChangeSettings(True)

chatMode = 1
def changeChatMode():
	global chatMode
	if chatMode==1:
		appControl.volumeControl('mute')
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		UserField.focus()
		chatMode=0
	else:
		appControl.volumeControl('full')
		TextModeFrame.pack_forget()
		VoiceModeFrame.pack(fill=BOTH)
		root.focus()
		chatMode=1

#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####
def progressbar():
	s = ttk.Style()
	s.theme_use('clam')
	s.configure("white.Horizontal.TProgressbar", foreground='white', background='white')
	progress_bar = ttk.Progressbar(splash_root,style="white.Horizontal.TProgressbar", orient="horizontal",mode="determinate", length=303)
	progress_bar.pack()
	splash_root.update()
	progress_bar['value'] = 0
	splash_root.update()
 
	while progress_bar['value'] < 100:
		progress_bar['value'] += 5
		# splash_percentage_label['text'] = str(progress_bar['value']) + ' %'
		splash_root.update()
		sleep(0.1)

def destroySplash():
	splash_root.destroy()

if __name__ == '__main__':
	splash_root = Tk()
	splash_root.configure(bg='#3895d3')
	splash_root.overrideredirect(True)
	splash_label = Label(splash_root, text="Đang tải...", font=('montserrat',15),bg='#3895d3',fg='white')
	splash_label.pack(pady=40)
	# splash_percentage_label = Label(splash_root, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
	# splash_percentage_label.pack(pady=(0,10))

	w_width, w_height = 400, 200
	s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	splash_root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30))

	progressbar()
	splash_root.after(10, destroySplash)
	splash_root.mainloop()	

	root = Tk()
	root.title('P.A.N.D.A')
	w_width, w_height = 400, 650
	s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	root.configure(bg=background)
	# root.resizable(width=False, height=False)
	root.pack_propagate(0)

	root1 = Frame(root, bg=chatBgColor)
	root2 = Frame(root, bg=background)
	root3 = Frame(root, bg=background)

	for f in (root1, root2, root3):
		f.grid(row=0, column=0, sticky='news')	
	
	################################
	########  CHAT SCREEN  #########
	################################

	#Chat Frame
	chat_frame = Frame(root1, width=380,height=551,bg=chatBgColor)
	chat_frame.pack(padx=10)
	chat_frame.pack_propagate(0)

	bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
	bottomFrame1.pack(fill=X, side=BOTTOM)
	VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	VoiceModeFrame.pack(fill=BOTH)
	TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	TextModeFrame.pack(fill=BOTH)

	# VoiceModeFrame.pack_forget()
	TextModeFrame.pack_forget()

	cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
	cblDarkImg = PhotoImage(file='extrafiles/images/centralButton1.png')
	if KCS_IMG==1: cblimage=cblDarkImg
	else: cblimage=cblLightImg
	cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
	cbl.pack(pady=17)
	AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
	AITaskStatusLbl.place(x=140,y=32)
	
	#Settings Button
	sphLight = PhotoImage(file = "extrafiles/images/setting.png")
	sphLight = sphLight.subsample(2,2)
	sphDark = PhotoImage(file = "extrafiles/images/setting1.png")
	sphDark = sphDark.subsample(2,2)
	if KCS_IMG==1: sphimage=sphDark
	else: sphimage=sphLight
	settingBtn = Button(VoiceModeFrame,image=sphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf",command=lambda: raise_frame(root2))
	settingBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Keyboard Button
	kbphLight = PhotoImage(file = "extrafiles/images/keyboard.png")
	kbphLight = kbphLight.subsample(2,2)
	kbphDark = PhotoImage(file = "extrafiles/images/keyboard1.png")
	kbphDark = kbphDark.subsample(2,2)
	if KCS_IMG==1: kbphimage=kbphDark
	else: kbphimage=kbphLight
	kbBtn = Button(VoiceModeFrame,image=kbphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	kbBtn.place(x=25, y=30)

	#Mic
	micImg = PhotoImage(file = "extrafiles/images/mic.png")
	micImg = micImg.subsample(2,2)
	micBtn = Button(TextModeFrame,image=micImg,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Text Field
	TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
	UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
	UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
	UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
	UserField.place(x=20, y=30)
	UserField.insert(0, "Ask me anything...")
	UserField.bind('<Return>', keyboardInput)
	
	#User and Bot Icon
	userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")
	botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
	botIcon = botIcon.subsample(2,2)
	

	###########################
	########  SETTINGS  #######
	###########################

	settingsLbl = Label(root2, text='Cài đặt', font=('Arial Bold', 15), bg=background, fg=textColor)
	settingsLbl.pack(pady=10)
	separator = ttk.Separator(root2, orient='horizontal')
	separator.pack(fill=X)
	#User Photo
	userProfileImg = Image.open("extrafiles/images/avatars/a"+str(ownerPhoto)+".png")
	userProfileImg = ImageTk.PhotoImage(userProfileImg.resize((120, 120)))
	userPhoto = Button(root2, image=userProfileImg, bg=background, bd=0, relief=FLAT, activebackground=background)
	userPhoto.pack(pady=(20, 5))

	#Username
	userName = Label(root2, text=ownerName, font=('Arial Bold', 15), fg=textColor, bg=background)
	userName.pack()

	#Settings Frame
	settingsFrame = Frame(root2, width=300, height=300, bg=background)
	settingsFrame.pack(pady=20)
	themeLbl = Label(settingsFrame, text='Chủ đề', font=('Arial', 13), fg=textColor, bg=background)
	themeLbl.place(x=0,y=143)
	themeValue = IntVar()
	s = ttk.Style()
	s.configure('Wild.TRadiobutton', font=('Arial Bold', 10), background=background, foreground=textColor, focuscolor=s.configure(".")["background"])
	darkBtn = ttk.Radiobutton(settingsFrame, text='Tối', value=1, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	darkBtn.place(x=150,y=145)
	lightBtn = ttk.Radiobutton(settingsFrame, text='Sáng', value=2, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	lightBtn.place(x=230,y=145)
	themeValue.set(1)
	if KCS_IMG==0: themeValue.set(2)


	chooseChatLbl = Label(settingsFrame, text='Nền chat', font=('Arial', 13), fg=textColor, bg=background)
	chooseChatLbl.place(x=0,y=180)
	cimg = PhotoImage(file = "extrafiles/images/colorchooser.png")
	cimg = cimg.subsample(3,3)
	colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg=chatBgColor)
	colorbar.place(x=150, y=180)
	if KCS_IMG==0: colorbar['bg'] = '#E8EBEF'
	Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)

	backBtn = Button(settingsFrame, text='   Trở về   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=lambda:raise_frame(root1))
	clearFaceBtn = Button(settingsFrame, text='   Đóng   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=deleteUserData)
	backBtn.place(x=5, y=250)
	clearFaceBtn.place(x=120, y=250)

	try:
		# pass
		Thread(target=voiceMedium).start()
	except:
		pass
	try:
		# pass
		Thread(target=webScrapping.dataUpdate).start()
	except Exception as e:
		print('System is Offline...')
	
	root.iconbitmap('extrafiles/images/ironman.ico')
	raise_frame(root1)
	root.mainloop()