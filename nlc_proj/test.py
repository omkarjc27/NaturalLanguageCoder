
def portal_encoder(d2d,ava):


	def encode_array(array,n):
			n=n+1
			al=len(array)
			for x in range(0,al) :
				are = array[x]
				typeoare=str(type(are))
				try: encoded_array
											
				except NameError:
					if typeoare=="<type 'str'>":
						encoded_array='"'+"[s"+str(n)+"]"+str(are)+'"'
					elif typeoare=="<type 'list'>":
						det=encode_array(are,n)
						encoded_array="[s"+str(n)+"]"+det
					else :
						encoded_array="[s"+str(n)+"]"+str(are)
														
				else:
					if typeoare=="<type 'str'>":
						encoded_array=encoded_array+"[s"+str(n)+"]"+'"'+str(are)+'"'
					elif typeoare=="<type 'list'>":
						det=encode_array(are,n)
						encoded_array=encoded_array+"[s"+str(n)+"]"+det
					else :
						encoded_array=encoded_array+"[s"+str(n)+"]"+str(are)
													
								
			return(encoded_array)





	length=len(d2d) 

	for x in xrange(0,length):
		var=ava[d2d[x]]
		typeov = str(type(var))
		try: encoded_data
			
		except NameError:
				
			if typeov=="<type 'str'>":
				encoded_data=str(d2d[x])+":"+'"'+str(var)+'"'+"];["
			elif typeov=="<type 'list'>":
				n=int('0')				
				encoded_data=str(d2d[x])+":"+"="+encode_array(var,n)+"];["	
			else :
				encoded_data=str(d2d[x])+":"+str(var)+"];["	
		else:

			if typeov=="<type 'str'>":
				encoded_data=encoded_data+str(d2d[x])+":"+'"'+str(var)+'"'+"];["
			elif typeov=="<type 'list'>":
				n=int('0')
				encoded_data=encoded_data+str(d2d[x])+":"+"="+encode_array(var,n)+"];["	
			else :
				encoded_data=encoded_data+str(d2d[x])+":"+str(var)+"];["
		


	return(encoded_data)



def portal_decoder(encoded_data):
	def decode_array(string,x):
		arr2ret = []
		x=x+1
		if "[s"+str(x)+"]" in string:
			sarr=string.split("[s"+str(x)+"]")
			del sarr[0]
			for mss in sarr:
				if mss[:1]=='"' :
					mss=mss.strip('"')
					arr2ret.append(str(mss))
				elif mss[:4]=='[s'+str(x+1)+']' :
					mss=decode_array(mss,x)
					arr2ret.append(mss)	
				else:
					arr2ret.append(mss)	
					

		

		return(arr2ret)			


	main_arr=encoded_data.split("];[")
	ps=len(main_arr)-1
	del main_arr[ps]
	for sub_str in main_arr :
		sub_arr = sub_str.split(":")
		v_name=sub_arr[0]
		v_val=sub_arr[1]
		if v_val[:1]=='"' :
			v_val=v_val.strip('"')
			globals()[v_name]=str(v_val)
		elif v_val[:1]=='=' :
			v_val=v_val.lstrip("=")
			x=0
			ret_arr=decode_array(v_val,x)
			globals()[v_name]=ret_arr	
		else:
			globals()[v_name]=v_value
