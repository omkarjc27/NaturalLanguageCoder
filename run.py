import subprocess
import Tkinter
from Tkinter import *
import tkMessageBox
import re
import readline
import tkFont
import ast
import os
import ntpath
import webbrowser


# readin and writeout are as name says

def readin(rfile):
	file = open(rfile,"r")
	result = file.read()
	file.close()
	return(result)

def writeout(data,file):
	file = open(file,"w")
	result = file.write(data)
	file.close()



# initiates the database

def initiate(file):
	global snippet
	global intent
	i=0
	m_arr = readin(data_dire+file).split('@##@@')
	del m_arr[-1] 
	for line in m_arr:
		item = line.split('##$$##')	
		snippet.append(item[1])
		intent.append(item[0])		
		i+=1	



# the entry with the suggestion box

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
		self.bind("<Up>", lambda event:self.moveUp())
		self.bind("<Down>", self.moveDown)
		self.bind("<Return>", lambda event:self.do_enter(event))
		self.bind("<Control-s>",lambda event:save_command())
		self.bind("<Control-r>",lambda event:runfile())
		self.bind("<Control-z>",lambda event:editor_undo())
		self.bind("<Tab>",lambda event:self.add_short(event,"\t"))
		self.bind("<parenleft>",lambda event:self.add_short(event,"()"))
		self.bind('<quotedbl>',lambda event:self.add_short(event,"\"\""))
		self.bind("<quoteright>",lambda event:self.add_short(event,"\'\'"))
		self.bind("<BackSpace>", self.do_backspace)
		self.bind("<Right>", self.close_lb)
	def changed(self, name, index, mode):
		global listboxUp_b
		if self.var.get() == '':
			if listboxUp_b == True:
				self.listbox.destroy()
				listboxUp_b = False
		else:
			words = self.comparison()
			if words:
				if listboxUp_b != True:
					global width
					self.listbox = Listbox(width=100, height=len(words))
					self.listbox.bind("<Button-1>", self.selection)
					self.listbox.bind("<Return>", self.selection)
					self.listbox.bind("<Right>", self.close_lb)
					self.listbox.bind("<Tab>",lambda event:self.add_short(event,"\t"))
					self.listbox.bind("<parenleft>",lambda event:self.add_short(event,"()"))
					self.listbox.bind('<quotedbl>',lambda event:self.add_short(event,"\"\""))
					self.listbox.bind("<quoteright>",lambda event:self.add_short(event,"\'\'"))
					self.listbox.place(x=0, y=(self.line_button.row+1)*28)
					self.listbox.config(font=Font2)
					listboxUp_b = True
				
				self.listbox.delete(0, END)
				for w in words:
					self.listbox.insert(END,w)
			else:
				if listboxUp_b == True:
					self.listbox.destroy()
					listboxUp_b = False
	def close_lb(self,event):
		global listboxUp_b
		if listboxUp_b == True:
			self.listbox.destroy()
			listboxUp_b = False
	def selection(self, event):
		global listboxUp_b
		if listboxUp_b == True:
			self.var.set(self.listbox.get(ACTIVE))
			self.icursor(self.listbox.get(ACTIVE).find('\'')+1)
			self.listbox.destroy()
			self.listboxUp = False
			listboxUp_b = False		
	def moveUp(self):
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
			if w== None and len(pattern)>=3 and pattern in w.decode('utf-8').strip() :
				matches.append(w.decode('utf-8').strip())
		return matches
	def add_short(self,event,text):
		if listboxUp_b != True:
			t = self.index(INSERT)
			self.insert(t,text)
			if text == '\"\"' or text == '\'\'' or text== '()':
				self.icursor(t+1)
			return 'break'	
	def do_backspace(self,event):
		
		if  self.index(INSERT)== 0 :
			global listboxUp_b
			c_position = 0
			if listboxUp_b == True:
				self.listbox.destroy()
				self.listboxUp = False
				listboxUp_b = False
			new_selection = self.line_button.row-1
			txt2add = self.get()
			self.delete(0,END)			
			for line in button_list:
				if line.row == new_selection:
					c_position = len(line.text)
					line.lineclick()
					line.set_text(line.sugg,line.text+txt2add)
					new_line = line
			new_selection = self.line_button.row+1
			old_selection = self.line_button
			for x in xrange(len(button_list)):
				for line in button_list:
					if line.row == new_selection:
						old_selection.lineclick()
						old_selection.set_text(old_selection.sugg,line.text)
						old_selection = line	
						new_selection+=1
			for line in button_list:		
				if line.row == len(button_list):
					line.lineclick()
					line.set_text(line.sugg,'')
			
			if listboxUp_b == True:
				self.listbox.destroy()
				self.listboxUp = False
				listboxUp_b = False
						
			self.moveUp()		
			new_line.sugg.icursor(c_position)			

	def do_enter(self,event):
		global listboxUp_b
		c_position = 0
		if listboxUp_b == True:
			self.listbox.destroy()
			self.listboxUp = False
			listboxUp_b = False
		new_selection = self.line_button.row+1
		f_txt = self.var.get()[self.index(INSERT):]
		self.delete(self.index(INSERT),END)

		for x in xrange(len(button_list)-self.line_button.row):
			for line in button_list:
				if line.row == new_selection:
					line.lineclick()
					line.set_text(line.sugg,f_txt)
					new_selection+=1
					f_txt = line.text 

		
		linebutton(f_txt,len(button_list)+1)
		
		for line in button_list:
			if line.row == self.line_button.row+1:
				line.lineclick()
				line.sugg.icursor(0)
		if listboxUp_b == True:
			self.listbox.destroy()
			self.listboxUp = False
			listboxUp_b = False
		
					


# line and its functions

class linebutton():
	def __init__(self,line,i):
		colort,font = self.find_color(line)
		self.row = i
		self.text = line
		self.id = Tkinter.Button(tbox,text=line,font=font,highlightthickness=0,anchor="w",command=lambda:self.lineclick(),width=width,relief = FLAT,fg=colort,bg="#f2f2f2",activebackground=color1,activeforeground=colort,background=color3)
		self.no = Tkinter.Label(tbox,text=self.row,font=tkFont.Font(family='Noto Sans ',size=8),bg=color2,fg=color1)
		self.no.place(x=2,y=(self.row*28)+2,width=18,height=28)
		self.wind = tbox.create_window(20,(i*28)+2,width=width-345,height=28,window=self.id,anchor=NW)
		global button_list
		button_list.append(self)	
	def set_text(self,sugg,text):
		sugg.delete(0,END)
		sugg.insert(0,text)
	def lineclick(self):
		self.sugg = AutocompleteEntry(intent,self, tbox)
		self.sugg.config({"background": color1 },bd=0,selectborderwidth=0,font=Font2,width=10)
		global current_line
		if current_line != False:
			if current_line.text != current_line.sugg.get():
				current_line.t_changed()

			current_line.text = current_line.sugg.get() 
			current_line.sugg.destroy()
			current_line.declare()	
		tbox.itemconfigure(self.wind, window=self.sugg)
		self.set_text(self.sugg,self.text)
		current_line = self
		global current_row
		current_row.config(text="Editing Line "+str(self.row))
		button_list.remove(self)
	def t_changed(self):
		global cache_text_arr
		global cache_line_arr	
		cache_line_arr.append(self.row)
		cache_text_arr.append(self.text)
	def declare(self):
		colort,font = self.find_color(self.text)
		self.id = Tkinter.Button(tbox,text=self.text,font=font,highlightthickness=0,anchor="w",command=lambda:self.lineclick(),width=width,relief = FLAT,fg=colort,bg="#f2f2f2",activebackground=color1,activeforeground=colort,background=color3)
		self.wind = tbox.create_window(20,(self.row*28)+2,width=width-345,height=28,window=self.id,anchor=NW)
		self.no = Tkinter.Label(tbox,text=self.row,font=tkFont.Font(family='Noto Sans ',size=8),bg=color2,fg=color1)
		self.no.place(x=2,y=(self.row*28)+2,width=18,height=28)
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



# pythonize and depythonize used to convert nlc data to python code and vice-versa

def pythonize(line):
	if "import nlc data " in line:
		i_data = line.replace("import nlc data ","")
		im_arr = i_data.split(",")
		im_line = "#import nlc data "
		for im in im_array:
			initiate(im)
			im_line += im+", "
		return(im_line)	

	else:	 
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
				splits = inten.split("`")
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
						splits = tline.split('`')
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
		elif "#import nlc data " in line:
			i_data = line.replace("#import nlc data ","")
			im_arr = i_data.split(",")
			im_line = "import nlc data "
			for im in im_array:
				initiate(im)
				im_line += im+", "
			return(im_line)



# ctrl-Z as usual

def editor_undo():
	if len(cache_line_arr)>1:	
		line_nox = cache_line_arr[-1]
		for line in button_list:
			if line.row == line_nox:
				line.text = cache_text_arr[-1]
				line.id.configure(text=line.text)
		del cache_text_arr[-1]
		del cache_line_arr[-1]		



# open,open new file and save file commands

def open_button(selection,t):
	writeout(dire+selection+".py","nlc_data/cache_nlc")
	open_command(1)
	t.destroy()

def open_command(n):
	global file
	if n != 0:
		
		if os.path.exists(readin('nlc_data/cache_nlc')):
			file = open(readin("nlc_data/cache_nlc"),"r")
			
		else:
			file = None		
	if file != None:
		root.title("Currently Editing file - \" "+ntpath.basename(file.name).replace(".py","")+" \"")
		writeout(file.name,"nlc_data/cache_nlc")
		globals()["tbox"] = tbox
		for button in button_list:
			button.id.destroy()
		del button_list[:]	
		fileopened = True
		contents = readin(file.name)
		if "welc_screen" in globals():
			global welc_screen
			welc_screen.destroy()
		if contents=="":
			contents = "# write code here"
		editor(contents)
		file.close()
	else:
		tbox.place(x=0,y=0)
		tbox.config(width=width,height=height-100)
		welc_screen = Label(root,text="Welcome To NLC",font=tkFont.Font(family='Noto Sans ',size=20),bg =color1,foreground=color2,anchor=W)
		welc_screen.place(x=0,y=0)	

class open_menu_button():
	def __init__(self):
		self.projs = os.listdir(dire)
		for p in self.projs:
			self.p = p
			self.dname = p.replace(".py","")
			openmenu.add_command(label="        "+self.dname+"        ",command=lambda:self.openfrommenu(str(self.p)))
	def openfrommenu(self,filen):
		writeout(dire+filen,"nlc_data/cache_nlc")
		open_command(1)	

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
					oline = button_list[k].text.replace("----|","\t")
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

class popupWindow(object):
	def __init__(self):
		top=self.top=Toplevel(root)
		self.l=Label(top,text=" ENTER NAME OF NEW PROJECTS")
		self.l.pack()
		self.e=Entry(top)
		self.e.pack()
		self.b=Button(top,text='Ok',command=self.cleanup)
		self.top.bind("<Return>",lambda event:self.cleanup())					
		self.b.pack()
	def cleanup(self):
		self.value=self.e.get()
		if " " in self.value:
			self.value = self.value.replace(" ","_")
		self.top.destroy()
		global file
		file = open(dire+self.value+".py","w+")
		writeout(dire+self.value+".py",'nlc_data/cache_nlc')
		open_command(1)

def new_command():
	# now redundant
	nwind = popupWindow()



#exit the gui
def exit_command():
	if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
		root.destroy()



# documentations

def about_command():
	#leads to about webpage
	label = tkMessageBox.showinfo("About", "For Help Go to : link")

def doc_command():
	label = tkMessageBox.showinfo("About", "For Documentations Go to : link")
	#filler



#main declaration of editor

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
		line = line.replace("\t", "----|")
		bid = linebutton(line,i)
		if i == 0:
			bid.lineclick()
		i+=1 
	if 'welc_screen'in globals():
		welc_screen.destroy()	
	tbox.focus_set()
	tbox.bind("<Control-s>",lambda event:save_command())
	tbox.bind("<Control-r>",lambda event:runfile())
	tbox.config(width=width,height=height-100)
	vbar=Scrollbar(root,orient=VERTICAL)
	vbar.config(command=tbox.yview,bg ='#181717',activebackground='#181717',bd=0)
	vbar.place(x=(width)-315,y=2,height=height*0.865,width=13)
	tbox.place(x=0,y=0)
	tbox.config(scrollregion=(0,0,0,28*i))
	tbox.config(yscrollcommand=vbar.set)
	west_line = Tkinter.Label(tbox,text="",bg=color2)
	west_line.place(x=2,y=2,width=18,height=height)



# add more data to db

def add_data():
	with open('conala-corpus/conala-mined.jsonl', 'rb') as f:
		
		for item in jsonlines.Reader(f):
			snippet.append(item['snippet'])
			intent.append(item['intent'])		



# execute code

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



# browses to webpage

def browser(utype):
	if utype == "cre":
		webbrowser.open("https://omkarjc27.github.io/NaturalLanguageCoder/",new=1)
	elif utype == "lic":
		webbrowser.open("https://omkarjc27.github.io/NaturalLanguageCoder/",new=1)		
	elif utype == "dev":
		webbrowser.open("https://omkarjc27.github.io/NaturalLanguageCoder/DEVLOP.html",new=1)		
	elif utype == "docs":
		webbrowser.open("https://omkarjc27.github.io/NaturalLanguageCoder/",new=1)
	elif utype == "for":
		webbrowser.open("https://github.com/omkarjc27/NaturalLanguageCoder/issues",new=1)





snippet = []
intent = []
dire = "/home/omkar/Codes/NaturalLanguageCoder/nlc_proj/"
data_dire="/home/omkar/Codes/NaturalLanguageCoder/nlc_data/"
color1='#d3d3d3'
color2='#006b85'
color3='#d0d0d0'
initiate('def_data')


#						M 	A 	I 	N 		S 	C 	R 	E 	E 	N
current_nlc_version = "(v0.2)"
root = Tkinter.Tk(className="")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()


#				T 	H 	E 	M 	E 		 V 	A 	R 	I 	A 	B 	L 	E 	S
Font1 = tkFont.Font(family='Noto Sans',size=20)
Font2 = tkFont.Font(family='Noto Sans',size=10)
Font3 = tkFont.Font(family='Noto Mono',size=16)
tbox = Tkinter.Canvas(root,bg=color1)
file = None
fileopened = False
root.geometry('%dx%d+%d+%d' % (width/2, height,0,0))
current_line = False
button_list = []
er_pyf = ""
op_fil = ""
listboxUp_b = False
#root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='nlc_data/icon.png'))
cache_line_arr = []
cache_text_arr = []


#	C 	O 	D 	E 		M 	E 	N 	U
term = Label(root,text="Terminal",font=tkFont.Font(family='Noto Sans ',size=12),bg ='#252525',foreground='#c1c1c1',anchor=N)
current_row = Label(root,text="Not Editing",font=Font2,bg ='#252525',foreground='#c1c1c1',anchor=W)
current_row.place(x=width-300,y=2,width=300,height=30)
term.place(x=width-300,y=34,width=300,height=height*0.865)


if readin("nlc_data/cache_nlc") == '':
	tbox.place(x=0,y=0)
	tbox.config(width=width,height=height-100)
	welc_screen = Label(root,text="Welcome To NLC",font=tkFont.Font(family='Noto Sans ',size=20),bg =color1,foreground=color2,anchor=W)
	welc_screen.place(x=0,y=0)
else :
	open_command(1)
if __name__ == "__main__":	
	#			M 	E 	N 	U
	menu = Menu(root ,bg =color2,foreground=color3)
	root.config(menu=menu)
	promenu = Menu(menu,bg =color2,foreground=color3)
	menu.add_cascade(label="NLC", menu=promenu ,font=Font2)
	promenu.add_command(label="    World",font=Font2)
	promenu.add_command(label="    Modules",font=Font2)
	promenu.add_command(label="    New Project                 ",font=Font2,command=new_command)
	openmenu = Menu(root,bg=color2,fg=color3)	
	open_menu_button()
	menu.add_cascade(label="Open",menu=openmenu,font=Font2)
	menu.add_command(label="Undo", command=editor_undo,font=Font2)
	menu.add_command(label="Forum/Help", command=lambda:browser("for") ,font=Font2)
	menu.add_command(label="Documentations", command=lambda:browser("docs") ,font=Font2)
	menu.add_command(label="Credits",font=Font2,command=lambda:browser("cre"))
	menu.add_command(label="License",font=Font2,command=lambda:browser("lic"))
	menu.add_command(label=" "*35+"Natural Language Coder "+current_nlc_version+" "*110)
	menu.entryconfig(8, state=DISABLED)
	menu.add_command(label="Save", command=save_command,font=Font2)
	menu.add_command(label="Run", command=runfile,font=Font2)
	menu.add_command(label="Exit ", command=exit_command,font=Font2)
root.mainloop()