import sys
import os
from typing import AsyncGenerator



if os.name != "nt":
	colors = {
		"WARNING" : '\033[93m',
		"ERROR" : '\033[91m',
		"NONE": '\033[0m',
		"SUCCESS": '\033[1;32m',
	}
else:
	colors = {
		"WARNING" : '',
		"ERROR" : '',
		"NONE": '',
		"SUCCESS": '',
	}

TOKENTYPES = [
	"INT",
	"STRING",
	"POINTER",
	"COMMAND",
	"END"
]

IGNORED_CHARS = [
	" ",
	"\n",
	"\t",
	"\r"
]

COMMANDS = [
	"OUT",
	"FIN",
	"DUN",
	"SET",
	"INP",
	"RUN",
	"ADD",
	"SUB",
	"MUL",
	"DIV",
	"SGN"
]

def inse_raise(ertype, description):
	message_col = colors['NONE']
	message_type = "UNDEFINED"
	if ertype == 1:
		message_col = colors['WARNING']
		message_type = "WARNING"
	if ertype == 2:
		message_col = colors['ERROR']
		message_type = "ERROR"
	print("\nInse " + message_col + message_type + ": " + colors['NONE'] + description)
	sys.exit()

class Token:

	def __init__(self, tokentype, val) -> None:
		if tokentype in TOKENTYPES:
			self.tokentype = tokentype
		else:
			inse_raise(2, "lexer what did you give me \n(this is a dev mistake lol this shouldnt come up unless i made a mistake) ")
		self.val = val 
	def __str__(self) -> str:
		return self.tokentype + " : " + str(self.val)
	def getreadable(self):
		if self.tokentype == "STRING":
			return str(self.val[1:-1])
		if self.tokentype == "INT" or self.tokentype == "POINTER":
			return int(self.val[1:-1])
		# if it got here, then there it is a command or period, so they can just be returned normally
		return self.val
	def getrealval(self):
		if self.tokentype != "POINTER" and self.tokentype != "COMMAND":
			if self.tokentype == "STRING":
				return self.val[1:-1]
			return int(self.val[1:-1])
		if self.tokentype == "POINTER":
			return memmanager.read(self.getreadable())
		if self.tokentype == "COMMAND":
			return self.val

class Lexer:
	def __init__(self) -> None:
		pass
	def cmd_scan(self, program, index):
		output = ""
		i = index
		loops = 0
		while program[i].isalpha():
			
			output += program[i]
			i += 1
			loops += 1

			if loops > 15:
				raise Exception
		return [output, i-1]
	def quote_scan(self, program, index, quote):
		#print(index)
		output = quote 
		i = index + 1
		loops = 0
		while i < len(program):


			if program[i] == quote:
				return [output+ quote, i]
			output += program[i]
			i += 1
		inse_raise(2, "you missed a " + quote + " to balance the one at " + str(index))		

	def bracket_scan(self, program, index):
		# find the outermost bracket from the given input
		output_ind = 0
		depth = 1
		i = index + 1
		while i < len(program):
			if program[i] == "[":
				depth += 1
			elif program[i] == "]":
				depth -= 1
				if depth == 0:
					output_ind = i
					break
			i += 1
		if depth != 0:
			inse_raise(2, "Unbalanaced brackets at starting from char " + str(index))
		output = program[index:output_ind+1]
		return [output, i]
		
	def run(self,program):
		output = []
		i = 0
		while i < len(program):
			char = program[i]
			ret_token = 0
			if char.isalpha(): # test for them sweet commands 
				scan = self.cmd_scan(program, i)

				# verification
				if scan[0].upper() not in COMMANDS:
					inse_raise(2,"Command " + scan[0] + " not recognised")
				
				ret_token = Token("COMMAND", scan[0].upper())
				i = scan[1]
			elif char == "/": # test for ints
				scan = self.quote_scan(program, i, "/")
				
				#verification
				if not (scan[0][1:-1].isnumeric() or scan[0][1] == "-" or scan[0][1] == "+"):
					inse_raise(2,"Number " + scan[0] + " must be numeric")

				ret_token = Token("INT", scan[0])
				i = scan[1]
			elif char == "&": # Test for pointers
				scan = self.quote_scan(program, i, "&")

				# verification
				if not (scan[0][1:-1].isnumeric()):
					inse_raise(2, "Pointer " + scan[0] + " must be numeric")
				if int(scan[0][1:-1]) > 99:
					inse_raise(2, "What kind of budget do you think we run here? 99 is more than enough memory for " + scan[0])
				ret_token = Token("POINTER", scan[0])
				i = scan[1]
			elif char == ".": # Test for endline
				ret_token = Token("END", ".")
			elif char == "[": # uh oh, test for string time yayy
				scan = self.bracket_scan(program, i)
				ret_token = Token("STRING", scan[0])
				i = scan[1]
			elif char == "#":
				scan = self.quote_scan(program, i, "#")
				i = scan[1] + 1
				continue
			elif char in IGNORED_CHARS:
				i += 1
				continue
			elif char == "]": #special case
				
				inse_raise(2, "unbalanced brackets at " + str(i))
			else:
				inse_raise(2, "Sorry mate, dunno what your talking about at char " + str(i))
			output.append(ret_token)				
			i += 1
		return output

class Interpreter:
	def __init__(self) -> None:
		pass
	def run(self,tokenlist, depth = 0):
		#for i, token in enumerate(tokenlist):
			#if token.tokentype == "END":
				#parent = None
				#arguments = 0
				#continue
			#if parent == None:
				#if token.tokentype == "COMMAND":
					#parent = token.val

					## special commands that take no arguments go here because i cant think of a better solution
					#if parent == "FIN":
						#return
					#if parent == "DUN":
						#print()
						#print("Inse is finished with no errors. very cool")
						#sys.exit()
					
					#continue
				#else:
					#inse_raise(2, "Statement number " + str(i) + " must begin with command")
			#if parent == "OUT":
				#if arguments > 1:
					#inse_raise(2, "Too many arguments for statement " + str(i))
				#if token.tokentype == "STRING" or token.tokentype == "INT":
					#print(token.getreadable())		
				#elif token.tokentype == "POINTER":
					#print(memmanager.read(token.getreadable()))
				#else:
					#inse_raise(2, "Statement number " + str(i) + " has bad type for the command " + str(parent))
				#arguments += 1
				#continue
			#if parent == "SET":
				#if arguments > 2:

					#inse_raise(2, "Too many arguments for statement " + str(i))
				#if arguments == 1:
					#if token.tokentype != "COMMAND":
						#memmanager.write()
		i = 0
		#print(depth)
		while i < (len(tokenlist)):
			if tokenlist[i].tokentype == "COMMAND":
				# Command: OUT
				# arguments: 1
				if tokenlist[i].val == "OUT":
					arguments = 1
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					
					if tokenlist[i+1].tokentype == "STRING" or tokenlist[i+1].tokentype == "INT":
						#print(tokenlist[i+1].getreadable())
						print(tokenlist[i+1].getreadable(), end = "")
						i += arguments + 1

					elif tokenlist[i+1].tokentype == "POINTER":
						print(memmanager.read(tokenlist[i+1].getreadable()), end= "")
						i += arguments + 1
					else:
						inse_raise(2, "Bad type arguments for statement " + str(i))
				if tokenlist[i].val == "DUN":
					arguments = 0
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))

					print()
					print(colors["SUCCESS"] + "Inse program ended without errors." + colors["NONE"])
					sys.exit()
				if tokenlist[i].val == "FIN":
					arguments = 0
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					
					return
				if tokenlist[i].val == "SET":
					arguments = 2
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					
					if tokenlist[i+2].tokentype != "POINTER":
						inse_raise(2, "Bad type arguments for statement " + str(i))

					if tokenlist[i+1].tokentype == "STRING" or tokenlist[i+1].tokentype == "INT":
						memmanager.write(tokenlist[i+2].getreadable(),tokenlist[i+1].getreadable())
						i += arguments + 1
					elif tokenlist[i+1].tokentype == "POINTER":
						
						memmanager.write(tokenlist[i+2].getreadable(),memmanager.read(tokenlist[i+1].getreadable()))
						i += arguments + 1
					else:
						inse_raise(2, "Bad type arguments for statement " + str(i))
				if tokenlist[i].val == "INP":
					arguments = 2
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					
					if tokenlist[i+2].tokentype != "INT":
						inse_raise(2, "Bad type arguments for statement " + str(i))
					
					if tokenlist[i+1].tokentype != "POINTER":
						inse_raise(2, "Bad type arguments for statement " + str(i))
					
					inputvar = input()
					outputvar = 0
					if tokenlist[i+2].getreadable() == 0: # get as int
							if inputvar.isalpha():
								outputvar = ord(inputvar[0])
							else:
								outputvar = int(inputvar)
					else:
						outputvar = inputvar
					
					memmanager.write(tokenlist[i+1].getreadable(), outputvar)
					i += arguments + 1

				if tokenlist[i].val == "RUN":
					arguments = 1
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					
					if tokenlist[i+1].tokentype != "STRING" and tokenlist[i+1].tokentype != "POINTER":
						inse_raise(2, "Bad type arguments for statement " + str(i))
					
					if tokenlist[i+1].tokentype == "STRING":

						metalist = lexer.run(tokenlist[i+1].getreadable())
					else:
						metalist = lexer.run(memmanager.read(tokenlist[i+1].getreadable()))

					try:
						self.run(metalist,depth+1)
					except RecursionError:
						inse_raise(2, "Stack overflow!")
			
					i += arguments + 1
				if tokenlist[i].val == "ADD":
					arguments = 3
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))

					arglist = []					
					for j in range(i+1, i+arguments + 1):
						if tokenlist[j].tokentype == "COMMAND":
							inse_raise(2, "Cannot pass command as arg in statement " + str(i))
						arglist.append(tokenlist[j].getrealval())
					
					if type(arglist[0]) != type(arglist[1]):

						inse_raise(2, "Bad type arguments for statement " + str(i))
					
					
					memmanager.write(tokenlist[i+3].getreadable(),arglist[0] + arglist[1])
					
					
					i += arguments + 1
				if tokenlist[i].val == "SUB":
					arguments = 3
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))

					arglist = []					
					for j in range(i+1, i+arguments + 1):
						if tokenlist[j].tokentype == "COMMAND":
							inse_raise(2, "Cannot pass command as arg in statement " + str(i))
						arglist.append(tokenlist[j].getrealval())
					
					if type(arglist[0]) != type(arglist[1]):

						inse_raise(2, "Bad type arguments for statement " + str(i))
					
					if type(arglist[0]) == int:
						memmanager.write(tokenlist[i+3].getreadable(),arglist[0] - arglist[1])
					
					if type(arglist[0]) == str:
						memmanager.write(tokenlist[i+3].getreadable(),arglist[0].replace(arglist[1], ""))
					
					i += arguments + 1
				if tokenlist[i].val == "MUL":
					arguments = 3
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))

					arglist = []					
					for j in range(i+1, i+arguments + 1):
						if tokenlist[j].tokentype == "COMMAND":
							inse_raise(2, "Cannot pass command as arg in statement " + str(i))
						arglist.append(tokenlist[j].getrealval())
					
					if type(arglist[1]) == str:
						inse_raise(2, "Cannot multiply something BY a string in statement " + str(i))
					

					if type(arglist[0]) != type(arglist[1]):
						if type(arglist[1]) == int and type(arglist[0]) == int:
							memmanager.write(tokenlist[i+3].getreadable(),arglist[0] * arglist[1])
						else:
							# only if string is first arg while int is second arg
							if arglist[1] >= 0: # if positive
								memmanager.write(tokenlist[i+3].getreadable(),arglist[0] * arglist[1])
							else: #oh boy... if negative
								# First, split the string into commands
								preoutput = arglist[0].split(".")

								# reverse it
								preoutput.reverse()


								# string it back together with a full stop
								output = ".".join(iter(preoutput))


								memmanager.write(tokenlist[i+3].getreadable(),output * abs(arglist[1]))
					
					i += arguments + 1
				if tokenlist[i].val == "SGN":
					arguments = 2
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))

					arglist = []					
					for j in range(i+1, i+arguments + 1):
						if tokenlist[j].tokentype == "COMMAND":
							inse_raise(2, "Cannot pass command as arg in statement " + str(i))
						arglist.append(tokenlist[j].getrealval())
					
					if type(arglist[0]) != int and tokenlist[i + 2].tokentype != "POINTER":

						inse_raise(2, "Bad type arguments for statement " + str(i))
					
					if arglist[0] == 0:
						memmanager.write(tokenlist[i+2].getreadable(),0)
					elif arglist[0] > 0:

						memmanager.write(tokenlist[i+2].getreadable(),1)
					else:
						memmanager.write(tokenlist[i+2].getreadable(),-1)

					
					i += arguments + 1
						
				if tokenlist[i].val == "DIV":
					arguments = 3
					if i + arguments + 1 > len(tokenlist):

						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))
					if tokenlist[i + arguments + 1].tokentype != "END":
						inse_raise(2, "Unsuitable number of arguments for statement " + str(i))

					arglist = []					
					for j in range(i+1, i+arguments + 1):
						if tokenlist[j].tokentype == "COMMAND":
							inse_raise(2, "Cannot pass command as arg in statement " + str(i))
						arglist.append(tokenlist[j].getrealval())
					
					if type(arglist[0]) != type(arglist[1]):

						inse_raise(2, "Bad type arguments for statement " + str(i))
					
					if type(arglist[0]) == int:
						try:
							memmanager.write(tokenlist[i+3].getreadable(),arglist[0] // arglist[1])
						except ZeroDivisionError:
							
							inse_raise(2, "Dont try to divide by zero pal " + str(i))
					else:
						inse_raise(2, "Bad type arguments for statement " + str(i))
					
					i += arguments + 1
			elif tokenlist[i].tokentype == "END":
				i+= 1
			else:
				print(tokenlist[i].tokentype)
				inse_raise(2, "Statement " + str(i) + " must begin with a command")

class MemoryManager:
	def __init__(self, program) -> None:
		self.memory = [0] * 100
		self.memory[99] = program
	def read(self, address):

		return self.memory[address]
	def write(self, address, value):
		if address == 99:
			inse_raise(2, "Dont try to edit your own source code bub.")
		self.memory[address] = value
	def get_type(self,address):
		return type(self.memory[address])

if __name__ == '__main__':
	program = ""
	try:
		filename = sys.argv[1]
	except IndexError:
		inse_raise(2, "Inse does not have an interactive prompt and i will not code one")
	if not os.path.isfile(filename):
		inse_raise(2, "file not found")
	else:
		with open(filename, "r", newline="") as f:

			program = f.read().replace("\\n","\n")

	lexer = Lexer()
	interpreter = Interpreter()
	memmanager = MemoryManager(program)

	tokenlist = lexer.run(program)
	#for token in tokenlist:
		#print(str(token))
	interpreter.run(tokenlist)

#print(program)
