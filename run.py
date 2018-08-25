import subprocess
import jsonlines
import json
import Tkinter
from Tkinter import *
import tkFileDialog
import tkMessageBox
import re
import readline
import tkFont
import ast

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
	with open('nlc_data.json', 'rb') as f:
		for item in json.load(f):
			snippet.append(item['snippet'])
			intent.append(item['rewritten_intent'])		
	#		canvas.itemconfigure(text_2, text="Acessing DATABASE :"+str(len(snippet)*100/(500*33))+"%")
	#with open('conala-corpus/conala-train.json', 'rb') as f:
	#	for item in json.load(f):
	#		snippet.append(item['snippet'])
	#		intent.append(item['intent'])		
	#		canvas.itemconfigure(text_2, text="Acessing DATABASE :"+str(len(snippet)*100/(2879*33))+"%")
	
			
	
	#canvas.itemconfigure(text_2, text="Completed")

#root.after(1000,initiate)
#root.after(2000, root.destroy)
#root.mainloop()
initiate()
root.destroy()
#						M 	A 	I 	N 		S 	C 	R 	E 	E 	N

current_nlc_version = "(v0.2)"
root = Tkinter.Tk(className=" Natural Language Coder - "+current_nlc_version)
tbox = Tkinter.Canvas(root,bg='#f2f2f2')
file = None
fileopened = False
root.geometry('%dx%d+%d+%d' % (width, height, width, height-100))
current_line = False
button_list = []
er_pyf = ""
op_fil = ""
listboxUp_b = False
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
				print(type(acListEntry))
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
		self.bind("<Return>", lambda event:self.moveDown(event,ent=True))
		self.bind("<Control-s>",lambda event:save_command())
		self.bind("<Control-r>",lambda event:runfile())
		self.bind("<Tab>",lambda event:self.add_short(event,"\t"))
		self.bind("<parenleft>",lambda event:self.add_short(event,"()"))
		self.bind('<quotedbl>',lambda event:self.add_short(event,"\"\""))
		self.bind("<quoteright>",lambda event:self.add_short(event,"\'\'"))
		
	def changed(self, name, index, mode):
		global listboxUp_b
		if self.var.get() == '':
			if listboxUp_b == True:
				self.listbox.destroy()
				self.listboxUp = False
				listboxUp_b = False
		else:
			words = self.comparison()
			if words:
				if listboxUp_b != True:
					global width
					self.listbox = Listbox(width=50, height=len(words))
					self.listbox.bind("<Button-1>", self.selection)
					self.listbox.bind("<Return>", self.selection)
					self.listbox.bind("<Right>", self.selection)
					self.listbox.bind("<Tab>",lambda event:self.add_short(event,"\t"))
					self.listbox.bind("<parenleft>",lambda event:self.add_short(event,"()"))
					self.listbox.bind('<quotedbl>',lambda event:self.add_short(event,"\"\""))
					self.listbox.bind("<quoteright>",lambda event:self.add_short(event,"\'\'"))
					self.listbox.place(x=0, y=(self.line_button.row+1)*28)
					self.listbox.config(font=Font2)
					self.listboxUp = True
					listboxUp_b = True
				
				self.listbox.delete(0, END)
				for w in words:
					self.listbox.insert(END,w)
			else:
				if listboxUp_b == True:
					self.listbox.destroy()
					self.listboxUp = False
					listboxUp_b = False
		
	def selection(self, event):
		global listboxUp_b
		if listboxUp_b == True:
			self.var.set(self.listbox.get(ACTIVE))
			self.icursor(self.listbox.get(ACTIVE).find('\'')+1)
			self.listbox.destroy()
			self.listboxUp = False
			listboxUp_b = False
			
	def moveUp(self, event):
		global listboxUp_b
		if listboxUp_b == True:
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
			global tbox
			new_edit_row = int(self.line_button.row)-1
			for line in button_list:
				if line.row == new_edit_row:
					line.lineclick()
			tbox.focus_set()
			#tbox.yview_scroll(1, "pages")
				
			
	def moveDown(self, event,ent=False):

		global listboxUp_b
		if listboxUp_b == True and ent == False:
			if self.listbox.curselection() == ():
				index = '0'
			else:
				index = self.listbox.curselection()[0]
			if index != END:						
				self.listbox.selection_clear(first=index)
				index = str(int(index)+1)
				self.listbox.see(index) # Scroll!
				self.listbox.selection_set(first=index)
				self.listbox.activate(index) 
				
					
		elif listboxUp_b == True and ent == True:
			self.selection(event)
		elif listboxUp_b == False :
			global new_edit_row
			global button_list
			global tbox
			new_edit_row = int(self.line_button.row)+1
			got_line = False
			for line in button_list:
				if line.row == new_edit_row:
					line.lineclick()			
					got_line = True
			if got_line != True:
				new_line = linebutton("",new_edit_row)
				new_line.lineclick()
			tbox.focus_set()
				
	def comparison(self):
		pattern =  self.var.get()
		matches = []
		for w in self.autocompleteList:
			if w!= None and len(pattern)>=3 and pattern in w.encode('utf-8') :
				matches.append(w.encode('utf-8'))
		return matches
	def add_short(self,event,text):
		if listboxUp_b != True:
			t = self.index(INSERT)
			self.insert(t,text)
			if text == '\"\"' or text == '\'\'' or text== '()':
				self.icursor(t+1)
			return 'break'	
			

class linebutton():
	def __init__(self,line,i):
		colort,font = self.find_color(line)
		self.id = Tkinter.Button(tbox,text=line,font=font,highlightthickness=0,anchor="w",command=lambda:self.lineclick(),width=width,relief = FLAT,fg=colort,bg="#f2f2f2",activebackground='#f2f2f2',activeforeground=colort)
		self.wind = tbox.create_window(0,i*28,width=width-302,height=28,window=self.id,anchor=NW)
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
		self.sugg.config({"background": "#f2f2f2","fg": "#000000"},bd=0,selectborderwidth=0,font=Font2)
		global current_line
		if current_line != False:
			current_line.text = current_line.sugg.get() 
			current_line.sugg.destroy()
			current_line.declare()	
		tbox.itemconfigure(self.wind, window=self.sugg)
		self.set_text(self.sugg,self.text)
		current_line = self
		global current_row
		current_row.config(text="Editing Line "+str(self.row))
		button_list.remove(self)

		
	def declare(self):
		colort,font = self.find_color(self.text)
		self.id = Tkinter.Button(tbox,text=self.text,font=font,highlightthickness=0,anchor="w",command=lambda:self.lineclick(),width=width,relief = FLAT,fg=colort,bg="#f2f2f2",activebackground='#f2f2f2',activeforeground=colort)
		self.wind = tbox.create_window(0,self.row*28,width=width-302,height=28,window=self.id,anchor=NW)
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

def pythonize(line):
	# x = concatenate 'x' of integers
	# z = Concatenate elements of a list 'y' of multiple integers to a single integer
	#"Concatenate elements of a list 'x' of multiple integers to a single integer"
	#"sum(d * 10 ** i for i, d in enumerate(x[::-1]))",
	'''
	y =  range(10)
	z = Concatenate elements of a list 'y' of multiple integers to a single integer
	print(z)
	'''
	for inten in intent:
		if inten != None:
			varl = []
			revarl = []
			aline = line.split("=")
			if len(aline) == 2:	
				vline = str(aline[0])+"="
				tline = aline[1]
			elif len(aline) == 1:
				vline=""
				tline=aline[0]
			splits = inten.split("\'")
			i = 0
			j = 1
			nline = line
			if len(aline)==2 or len(aline)==1:
				for split in splits:
					if i%2 == 0:
						if split not in tline:
							j=0	
					else:
						if j!=0:
							varl.append(split)
					i+=1
				if j == 1:
					resultant_intent = inten
					i=0
					splits = tline.split('\'')
					for split in splits:
						if i%2 ==1:
							revarl.append(split)
						i+=1
					snip=str(snippet[intent.index(inten)])
					if snip != None:
						for var in varl:
							if var in snip:
								snip = snip.replace(var,revarl[varl.index(var)])
						return(str(vline)+str(snip)+"\t#nlc_d_$_"+str(intent.index(inten))+"_$_"+str(varl)+"_$_"+str(revarl)) 	

def depythonize(line):
	if line != None:
		if '#nlc_d_$_' in line:
			ts = line.split('#')
			ldata = ts[1]
			idata = ldata.split('_$_')
			inten = str(intent[int(idata[1])])
			varl = ast.literal_eval(idata[2])
			revarl = ast.literal_eval(idata[3])
			for var in varl:
				inten = inten.replace(var,revarl[varl.index(var)])
			return(inten)	

def readin(rfile):#read a text file
	file = open(rfile,"r")
	result = file.read()
	file.close()
	return(result)

def writeout(data,file): 															#write to a text file
	file = open(file,"w")
	result = file.write(data)
	file.close()

def open_command(n):
	global file
	if n == 0:
		file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file to Open')
	else :
		file = open(readin("cache_nlc"),"r")	
	term.config(text="Opening"+str(file.name),fg="#333333",anchor=S)
	if file != None:
		root.title(" Natural Language Coder "+current_nlc_version+" - "+file.name)
		writeout(file.name,"cache_nlc")
		globals()["tbox"] = tbox
		fileopened = True
		contents = readin(file.name)
		if "nobutton" in globals():
			nobutton.destroy()
		if contents=="":
			contents = " "	
		editor(contents)
		file.close()
	term.config(text="",fg="#333333",anchor=S)

def save_command():
	global button_list
	global file
	if file != None:
		global current_line
		if current_line != False:
			current_line.text = current_line.sugg.get() 
			current_line.sugg.destroy()
			current_line.declare()	
			current_line = False
		data = []
		for i in range(0,len(button_list)):
			for k in range(0,len(button_list)):
				if i == button_list[k].row:
					oline = button_list[k].text.replace("____","\t")
					line = pythonize(oline)
					if line != None: 
						data.append(line)
					else :
						data.append(oline)	
					
		data = '\n'.join(data)	
		writeout(data,file.name)
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
	global button_list
	if len(lines)==0:
		lines.append(" ")
	if len(button_list)>1:
		for button in button_list:
			button.id.destroy()
		del button_list[:]	

	for line in lines:
		tes = depythonize(line)
		if tes != None:
			line = depythonize(line)
		line = line.replace("\t", "____")
		bid = linebutton(line,i)
		globals()["line"+str(i)]=bid
		i+=1 
	if 'welc_screen'in globals():
		welc_screen.destroy()	
	tbox.focus_set()
	tbox.bind("<Up>",	lambda event: tbox.yview_scroll(-1, "units"))
	tbox.bind("<Down>",  lambda event: tbox.yview_scroll( 1, "units"))
	tbox.bind("<Control-s>",lambda event:save_command())
	tbox.bind("<Control-r>",lambda event:runfile())
	tbox.config(width=width,height=height-100)
	vbar=Scrollbar(root,orient=VERTICAL)
	vbar.config(command=tbox.yview,bg ='#333333',activebackground='#333333',bd=0)
	vbar.place(x=(width)-20,y=0,height=150,width=15)
	tbox.place(x=0,y=0)
	tbox.config(scrollregion=(0,0,0,28*i))
	tbox.config(yscrollcommand=vbar.set)

def add_data():
	with open('conala-corpus/conala-mined.jsonl', 'rb') as f:
		
		for item in jsonlines.Reader(f):
			snippet.append(item['snippet'])
			intent.append(item['intent'])		
def runfile():
	#pyflakes text.py
	p = subprocess.Popen("pyflakes test.py", stdout=subprocess.PIPE, shell=True)
 	(output, err) = p.communicate()
	if output == "":
		p = subprocess.Popen("python test.py", stdout=subprocess.PIPE, shell=True)
	 	(output, err) = p.communicate()
	 	term.config(text="Output:\n"+str(output),fg="#009933",anchor=S)
	else:
		term.config(text="Error:\n"+str(output),fg="#ff0000",anchor=S)


#				T 	H 	E 	M 	E 		 V 	A 	R 	I 	A 	B 	L 	E 	S

Font1 = tkFont.Font(family='Noto Sans ',size=20)
Font2 = tkFont.Font(family='Noto Sans ',size=10)
Font3 = tkFont.Font(family='Noto Mono ',size=16)

#	C 	O 	D 	E 		M 	E 	N 	U
save=Button(root,text="Save",font=Font2,bg ='#333333',foreground='#d9d9d9',command=save_command)		
run=Button(root,text="Run",font=Font2,bg ='#333333',foreground='#d9d9d9',command=runfile)
save.place(x=width-80,y=30,width=60,height=30)
run.place(x=width-80,y=60,width=60,height=30)
term = Label(root,text="",font=tkFont.Font(family='Noto Sans ',size=12),bg ='#f2f2f2',foreground='#333333',anchor=S)
current_row = Label(root,text="Not Editing",font=Font2,bg ='#f2f2f2',foreground='#333333',anchor=W)
current_row.place(x=width-300,y=2,width=280,height=30)
term.place(x=width-300,y=150,width=300,height=518)

if readin("cache_nlc") == '':
	tbox.place(x=0,y=0)
	tbox.config(width=width,height=height-100)
	welc_screen = Label(root,text="Welcome To NLC",font=tkFont.Font(family='Noto Sans ',size=20),bg ='#f2f2f2',foreground='#333333',anchor=W)
	welc_screen.place(x=0,y=0)
else :
	open_command(1)
	
#			M 	E 	N 	U


menu = Menu(root ,bg ='#333333',foreground='#d9d9d9')
root.config(menu=menu)
# Project MENU CASCADE
promenu = Menu(menu,bg ='#333333',foreground='#d9d9d9')
menu.add_cascade(label="NLC", menu=promenu ,font=Font2)
#promenu.add_separator()
#promenu.add_command(label="  World",font=Font2)
#promenu.add_command(label="  Modules",font=Font2)
#promenu.add_command(label="  Languages",font=Font2)
promenu.add_separator()
#promenu.add_command(label="  New Project",font=Font2)
promenu.add_command(label="  Open Project", command=lambda:open_command(0),font=Font2)
promenu.add_command(label="  Save Project", command=save_command,font=Font2)
#promenu.add_separator()
#promenu.add_command(label="  UI Themes",font=Font2)
#promenu.add_command(label="  Color Schemes",font=Font2)
#promenu.add_command(label="  Fonts",font=Font2)
#promenu.add_separator()
#promenu.add_command(label="  Settings",font=Font2)
#promenu.add_command(label="  Prefrences",font=Font2)
#promenu.add_separator()
#promenu.add_command(label="  Credits",font=Font2)
#promenu.add_command(label="  Forum",font=Font2)
#promenu.add_command(label="  Contact",font=Font2)
#promenu.add_command(label="  License",font=Font2)
#promenu.add_command(label="  About",font=Font2)
#promenu.add_separator()
#promenu.add_command(label=" Extract Complete Data ", command=add_data,font=Font2)
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