import sys
import os


class Shell:

	def ShellGet(self, parameter, element):
		res = os.popen('tcam-ctrl -p 20110147').readlines()
	
		
		if parameter == 'Brightness':
			command = res[1]
		
		elif parameter == 'Gamma':
			command = res[2]
		
		elif parameter == 'Gain':
			command = res[3]
		
		elif parameter == 'Exposure':
			command = res[5]
		
		elif parameter == 'ExposureAuto':
			command = res[4]
			
		else:
			command = None

	
		if element == 'MinValue':
			i = 0
			while(command[i+2] != '\n'):
				name = command[i]
				name += command[i+1]
				name += command[i+2]
				if name == 'min':
					break
				i+=1
			i+=4
			value = ''
			while(command[i] != ' '):
				value += command[i]
				i+=1
			valuenum = int(value)
			return valuenum
	
		elif element == 'MaxValue':
			i = 0
			while(command[i+2] != '\n'):
				name = command[i]
				name += command[i+1]
				name += command[i+2]
				if name == 'max':
					break
				i+=1
			i+=4
			value = ''
			while(command[i] != ' '):
				value += command[i]
				i+=1
			valuenum = int(value)
			return valuenum
	
		elif element == 'DefaultValue':
			i = 0
			while(command[i+6] != '\n'):
				name = command[i]
				name += command[i+1]
				name += command[i+2]
				name += command[i+3]
				name += command[i+4]
				name += command[i+5]
				name += command[i+6]
				if name == 'default':
					break
				i+=1
			i+=8
			value = ''
			while(command[i] != ' '):
				value += command[i]
				i+=1
			valuenum = int(value)
			return valuenum
			
		elif element == 'CurrentValue':
			i = 0
			while(command[i+4] != '\n'):
				name = command[i]
				name += command[i+1]
				name += command[i+2]
				name += command[i+3]
				name += command[i+4]
				if name == 'value':
					break
				i+=1
			i+=6
			value = ''
			while(command[i] != ' '):
				value += command[i]
				i+=1
			valuenum = int(value)
			return valuenum
	
		else:
			return None


	def ShellPut(self, parameter, value):
		command = 'tcam-ctrl -p -s "'
		command += parameter
		command += '='
		command += str(value)
		command += '" 20110147'
		res = os.popen(command).readlines()
									 
