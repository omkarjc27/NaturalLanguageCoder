import jsonlines
import json
import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import re
import readline
import tkFont
snippet = []
intent = []

root = Tkinter.Tk()
#root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
#root.geometry('%dx%d+%d+%d' % (width*0.5, height*0.5, width*0.25, height*0.25))
#canvas = Tkinter.Canvas(root, height=height*0.5, width=width*0.5, bg="black")
#text_1 = canvas.create_text(width*0.5/2, (height*0.5/2)-50,fill='red',font="Times 100 bold" ,text="N L C")
#text_2 = canvas.create_text(width*0.5/2, (height*0.5/2)+40,fill='pink',font="Times 20 bold" ,text="STARTING NLC")
#canvas.pack()
def initiate():
	global snippet
	global intent
	#canvas.itemconfigure(text_2, text="INITIATING SYSTEM")
	with open('conala-corpus/conala-train.json', 'rb') as f:
		for item in json.load(f):
			snippet.append(item['snippet'])
			intent.append(item['intent'])		
	#		canvas.itemconfigure(text_2, text="Acessing DATABASE :"+str(len(snippet)*100/(500*33))+"%")
	with open('conala-corpus/conala-train.json', 'rb') as f:
		for item in json.load(f):
			snippet.append(item['snippet'])
			intent.append(item['intent'])		
	#		canvas.itemconfigure(text_2, text="Acessing DATABASE :"+str(len(snippet)*100/(2879*33))+"%")
	
			
	
	#canvas.itemconfigure(text_2, text="Completed")

#root.after(1000,initiate)
#root.after(2000, root.destroy)
#root.mainloop()
#initiate()
root.destroy()
#						M 	A 	I 	N 		S 	C 	R 	E 	E 	N


root = Tkinter.Tk(className=" Natural Language Coder - ( Editor ) ")
tbox = Tkinter.Canvas(root,bg='#f2f2f2')
fileopened = False
root.geometry('%dx%d+%d+%d' % (width, height, width, height))
current_line = False
button_list = []
class AutocompleteEntry(Entry):
	def __init__(self, autocompleteList,line_button, *args, **kwargs):
		self.line_button = line_button
		# Listbox length
		if 'listboxLength' in kwargs:
			self.listboxLength = kwargs['listboxLength']
			del kwargs['listboxLength']
		else:
			self.listboxLength = 20
		self.parentbutton = line_button	
		# Custom matches function
		if 'matchesFunction' in kwargs:
			self.matchesFunction = kwargs['matchesFunction']
			del kwargs['matchesFunction']
		else:
			def matches(fieldValue, acListEntry):
				pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
				return re.match(pattern, acListEntry)
				
			self.matchesFunction = matches
		
		Entry.__init__(self, *args, **kwargs)
		self.focus()

		self.autocompleteList = autocompleteList
		
		self.var = self["textvariable"]
		if self.var == '':
			self.var = self["textvariable"] = StringVar()

		self.var.trace('w', self.changed)
		self.bind("<Right>", self.selection)
		self.bind("<Up>", self.moveUp)
		self.bind("<Down>", self.moveDown)
		
		self.listboxUp = False

	def changed(self, name, index, mode):
		if self.var.get() == '':
			if self.listboxUp:
				self.listbox.destroy()
				self.listboxUp = False
		else:
			words = self.comparison()
			if words:
				if not self.listboxUp:
					self.listbox = Listbox(width=self["width"], height=self.listboxLength)
					self.listbox.bind("<Button-1>", self.selection)
					self.listbox.bind("<Right>", self.selection)
					self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
					self.listboxUp = True
				
				self.listbox.delete(0, END)
				for w in words:
					self.listbox.insert(END,w)
			else:
				if self.listboxUp:
					self.listbox.destroy()
					self.listboxUp = False
		
	def selection(self, event):
		if self.listboxUp:
			self.var.set(self.listbox.get(ACTIVE))
			#self.parentbutton.text = self.listbox.get(ACTIVE)
			self.listbox.destroy()
			self.listboxUp = False
			self.icursor(END)

	def moveUp(self, event):
		if self.listboxUp:
			if self.listbox.curselection() == ():
				index = '0'
			else:
				index = self.listbox.curselection()[0]
				
			if index != '0':				
				self.listbox.selection_clear(first=index)
				index = str(int(index) - 1)
				self.listbox.see(index) # Scroll!
				self.listbox.selection_set(first=index)
				self.listbox.activate(index)
		else:
			global new_edit_row
			global button_list
			new_edit_row = int(self.line_button.row)-1
			for line in button_list:
				if line.row == new_edit_row:
					line.lineclick()
			
	def moveDown(self, event):
		if self.listboxUp:
			if self.listbox.curselection() == ():
				index = '0'
			else:
				index = self.listbox.curselection()[0]
			if index != END:						
				self.listbox.selection_clear(first=index)
				index = str(int(index) + 1)
				self.listbox.see(index) # Scroll!
				self.listbox.selection_set(first=index)
				self.listbox.activate(index) 
		else:
			global new_edit_row
			global button_list
			new_edit_row = int(self.line_button.row)+1
			for line in button_list:
				if line.row == new_edit_row:
					line.lineclick()			
					
	def comparison(self):
		return [ w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w) ]

class linebutton():
	def __init__(self,line,i):
		colort,font = self.find_color(line)
		self.id = Tkinter.Button(tbox,text=line,font=font,highlightthickness=0,anchor="w",command=lambda:self.lineclick(),width=width,relief = FLAT,fg=colort,bg="#f2f2f2",activebackground='#f2f2f2',activeforeground=colort)
		self.wind = tbox.create_window(0,i*28,width=width,height=28,window=self.id,anchor=NW)
		self.row = i
		self.text = line
		global button_list
		button_list.append(self)
		#self.id.place(y=i*28,width=width*0.7)
		
	def set_text(self,sugg,text):
		sugg.delete(0,END)
		sugg.insert(0,text)

	def lineclick(self):
		self.sugg = AutocompleteEntry(intent,self, tbox)
		self.sugg.config({"background": "#f2f2f2","fg": "#000000"},bd=0,selectborderwidth=0)
		global current_line
		if current_line != False:
			current_line.text = current_line.sugg.get() 
			current_line.sugg.destroy()
			current_line.declare()	
		tbox.itemconfigure(self.wind, window=self.sugg)
		self.set_text(self.sugg,self.text)
		current_line = self
		button_list.remove(self)
		
	def declare(self):
		colort,font = self.find_color(self.text)
		self.id = Tkinter.Button(tbox,text=self.text,font=font,highlightthickness=0,anchor="w",command=lambda:self.lineclick(),width=width,relief = FLAT,fg=colort,bg="#f2f2f2",activebackground='#f2f2f2',activeforeground=colort)
		self.wind = tbox.create_window(0,self.row*28,width=width,height=28,window=self.id,anchor=NW)
		global button_list
		button_list.append(self)

	def find_color(self,line):
		#009933=green=import
		#002080=blue=defining classes.functions
		#800000=red=loops
		#
		color = "#000000"
		font = tkFont.Font(family='Noto Sans ',size=10)
		if "import" in line:
			color = "#009933"
			font = tkFont.Font(family='Khmer OS System Bold Italic',size=12)
		if "def" in line:
 			color = "#002080"
			font = tkFont.Font(family='Khmer OS System Bold',size=14)
		if "return" in line:
			color = "#002080"
			font = tkFont.Font(family='Noto Sans Italic',size=12)
		if "if" in line:
			color = "#800000"
			font = tkFont.Font(family='Liberation Sans Bold Italic',size=12)
		if "else" in line:
			color = "#800000"
			font = tkFont.Font(family='Liberation Sans Bold Italic',size=12)
		if "elif" in line:
			color = "#800000"
			font = tkFont.Font(family='Liberation Sans Bold Italic',size=12)
		if "while" in line:
			color = "#800000"
			font = tkFont.Font(family='Liberation Sans Bold Italic',size=12)
		if "for" in line:
			color = "#800000"
			font = tkFont.Font(family='Liberation Sans Bold Italic',size=12)
		if "class" in line:
			color = "#002080"
			font = tkFont.Font(family='Times Bold',size=14)	
		return color,font	

def readin(rfile):#read a text file
	file = open(rfile,"r")
	result = file.read()
	file.close()
	return(result)

def writeout(data,file): 															#write to a text file
	file = open(file,"w")
	result = file.write(data)
	file.close()

def open_command():	
	file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file to Open')
	if file != None:
		root.title(" Natural Language Coder - ( Editor ) - "+file.name)
		writeout(file.name,"cache_nlc")
		globals()["tbox"] = tbox
		fileopened = True
		contents = file.read()
		if "nobutton" in globals():
			nobutton.destroy()
		editor(contents)
		file.close()

def save_command():
	file = tkFileDialog.asksaveasfile(mode='w')
	if file != None:
		data = textPad.get('1.0', END+'-1c')
		file.write(data)
		file.close()
	else :
		print('file=none')	
		
def exit_command():
	if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
		root.destroy()

def about_command():
	label = tkMessageBox.showinfo("About", "For Help Go to : link")
	
def doc_command():
	label = tkMessageBox.showinfo("About", "For Documentations Go to : link")

def editor(content):
	lines = content.splitlines()
	i = 0
	for line in lines:
		bid = linebutton(line,i)
		globals()["line"+str(i)]=bid
		i+=1 
	tbox.config(width=width,height=height-30)
	vbar=Scrollbar(root,orient=VERTICAL)
	vbar.config(command=tbox.yview,bg ='#333333',activebackground='#333333',bd=0)
	vbar.place(x=(width)-20,y=0,height=120,width=15)
	tbox.place(x=0,y=0)
	tbox.config(scrollregion=(0,0,0,28*i))
	tbox.config(yscrollcommand=vbar.set)

def add_data():
	with open('conala-corpus/conala-mined.jsonl', 'rb') as f:
		
		for item in jsonlines.Reader(f):
			snippet.append(item['snippet'])
			intent.append(item['intent'])		
def runfile():
	proc = subprocess.Popen("python ", shell=True, stdout=subprocess.PIPE)			
			

#				T 	H 	E 	M 	E 		 V 	A 	R 	I 	A 	B 	L 	E 	S

Font1 = tkFont.Font(family='Noto Sans ',size=20)
Font2 = tkFont.Font(family='Noto Sans ',size=10)
Font3 = tkFont.Font(family='Noto Mono ',size=16)

#	C 	O 	D 	E 		M 	E 	N 	U

if readin("cache_nlc") == '':
	nobutton = Tkinter.Button(root,text='Open a PROJECT',font=Font2,command=open_command,bg ='#333333',foreground='#d9d9d9')
	nobutton.place(x=10,y=45)
else :
	file = readin("cache_nlc")	
	if file != None:
		root.title(" Natural Language Coder - ( Editor ) - "+file)
		writeout(file,"cache_nlc")
		globals()["tbox"] = tbox
		fileopened = True
		contents = readin(file)
		editor(contents)

save=Button(root,text="Save",font=Font2,bg ='#333333',foreground='#d9d9d9')		
run=Button(root,text="Run",font=Font2,bg ='#333333',foreground='#d9d9d9')
st=Button(root,text="Stop",font=Font2,bg ='#333333',foreground='#d9d9d9')
ce=Button(root,text="Errors",font=Font2,bg ='#333333',foreground='#d9d9d9')		
save.place(x=width-70,y=0,width=50,height=30)
run.place(x=width-70,y=30,width=50,height=30)
st.place(x=width-70,y=60,width=50,height=30)
ce.place(x=width-70,y=90,width=50,height=30)


#			M 	E 	N 	U


menu = Menu(root ,bg ='#333333',foreground='#d9d9d9')
root.config(menu=menu)
# Project MENU CASCADE
promenu = Menu(menu,bg ='#333333',foreground='#d9d9d9')
menu.add_cascade(label="NLC", menu=promenu ,font=Font2)
promenu.add_separator()
promenu.add_command(label="  World",font=Font2)
promenu.add_command(label="  Modules",font=Font2)
promenu.add_command(label="  Languages",font=Font2)
promenu.add_separator()
promenu.add_command(label="  New Project",font=Font2)
promenu.add_command(label="  Open Project", command=open_command,font=Font2)
promenu.add_command(label="  Save Project", command=save_command,font=Font2)
promenu.add_separator()
promenu.add_command(label="  UI Themes",font=Font2)
promenu.add_command(label="  Color Schemes",font=Font2)
promenu.add_command(label="  Fonts",font=Font2)
promenu.add_separator()
promenu.add_command(label="  Settings",font=Font2)
promenu.add_command(label="  Prefrences",font=Font2)
promenu.add_separator()
promenu.add_command(label="  Credits",font=Font2)
promenu.add_command(label="  Forum",font=Font2)
promenu.add_command(label="  Contact",font=Font2)
promenu.add_command(label="  License",font=Font2)
promenu.add_command(label="  About",font=Font2)
promenu.add_separator()
promenu.add_command(label=" Extract Complete Data ", command=add_data,font=Font2)
promenu.add_separator()
promenu.add_command(label=" Exit ", command=exit_command,font=Font2)

'''
# cloud 
cloudmenu = Menu(menu,bg ='#333333',foreground='#d9d9d9')
menu.add_cascade(label="Cloud", menu=cloudmenu ,font=Font2)
cloudmenu.add_command(label=" My Cloud", command=dummy,font=Font2)
cloudmenu.add_command(label=" Upload to Cloud", command=dummy,font=Font2)
cloudmenu.add_command(label=" World Cloud", command=dummy,font=Font2)
# WORLDMENU 
worldmenu = Menu(menu,bg ='#333333',foreground='#d9d9d9')
menu.add_cascade(label="World", menu=worldmenu ,font=Font2)
worldmenu.add_command(label=" Browse Projects  ", command=dummy,font=Font2)
worldmenu.add_command(label=" Browse Modules", command=dummy,font=Font2)
worldmenu.add_command(label=" Forum/Help", command=doc_command ,font=Font2)
worldmenu.add_command(label=" Documentation", command=doc_command ,font=Font2)
worldmenu.add_command(label=" Skins", command=dummy,font=Font2)
#EDIT
editmenu = Menu(menu,bg ='#333333',foreground='#d9d9d9')
menu.add_cascade(label="Edit", menu=editmenu ,font=Font2)
editmenu.add_command(label="Undo		", command=dummy,font=Font2)
editmenu.add_command(label="Redo", command=dummy,font=Font2)
editmenu.add_command(label="Cut", command=dummy,font=Font2)
editmenu.add_command(label="Copy", command=dummy,font=Font2)
editmenu.add_command(label="Paste", command=dummy,font=Font2)
# general
menu.add_command(label="Find", command=dummy,font=Font2)
menu.add_command(label="Settings", command=dummy,font=Font2)
'''
root.mainloop()