# inse
An esolang than can run itself inside itself (also with 0 if statements or loops) pronounced "in-say" or "insé"

Here is a 99 bottles of beer program as an example
```
# address 0 is bottles #
set /99/ &0&.

# main loop of the program #

set [
	out &0&.
	out [ bottles of beer on the wall \n].
	out &0&.
	out [ bottles of beer\n].
	out [take one down, pass it around\n].
	
	# subtraction #
	sub &0& /1/ &0&.
	
	out &0&.
	out [ bottles of beer on the wall \n \n].

	# test to see whether we are at 0 #

	# sign function will return 1 if we are not at 0, and 0 if we are (it will also turn negative if beer is negative but it should never be)#
	sgn &0& &1&.

	# multiply ourselves by the signed number, if we are 0, it will delete ourselves, it not nothing will happen #
	mul &10& &1& &10&.
	run &10&.

] &10&. # main loop is at address 10 #

run &10&.
dun.
```

## Install
```
git clone https://github.com/BurningApparatus/inse.git
cd inse
python main.py example/hello_world.inse
```

## Better Description
Inse is an esolang with no present loops or if statements. Code can be stored within "strings" or "blocks" which can be stored in memory. These strings can be run and edited through addition, subtraction and multiplication in order to change how the code is run. These interactions with the code allow for control flow. Im 90% sure its turing complete.

As you have probably noticed, the syntax is very simple, and not at all user friendly (because I'm not too great at writing interpreters). But I can argue that this is an esolang and I can make it as user unfriendly as I want.

For one, there are no variables, but you write directly to an array of memory. This is not becayse I'm lazy, but because the most popular esolangs use a stack or tape, and I wanted to innovate.
Also, commands cannot be nested. I think you can guess why at this point.

All commands must end in a full stop, otherwise you will get a confusing error message.
Did i mention that the error handling is terrible as well? May have neglected that part.

I also wrote the interpreter in 2 days so that may explain a lot (feel free to rewrite a better version)

I also really needed to put this somewhere, but the code itself is stored in address 99, so any inse program can become a quine if you add `out &99&` to the end :) 

## Documentation
Proceed with caution
### Data types
* Integer - defined between forward slashes e.g `/150/` `/13/` `/-36/` `/+4731/`
* String - defined between square brackets `[hello world]` `[set /13/ &13&]`
* Memory address/pointer - defined between ampersands `&7&` `&35&` `&99&`
Comments are defined in between # symbols (this can also be used for block comments). `# this is a comment #`

### Commands
* out - out (any type)
  * Prints the string or the int or the value in the address to the console.
* fin - fin
  * ends the current instance running on the stack. does not halt the program completely (kinda like return in other languages)
* dun - dun
  * halts the program regardless of what is currently on the stack (like sys.out() in python)
* set - set (any type) &address&
  * sets the value of the first parameter into the address in the second parameter
* inp - inp &address& /int/
  * asks for the user's input and puts it in the memory address in the first paramenter. If the second parameter is 00, read it as an integer. (If the user inputs a string, the first character of that string is read as its unicode character), if any non-zero value is in the second parameter, read as string.
* run - run (&address& or [string])
  * executes the code in the string/address.
* add - add (any) (any) &address&
  * adds the two values in the first two parameters and returns the result into the address. Integers are added and strings are concatenated. Values must contain the same type.
* sub - sub (any) (any) &address&
  * subtracts the two values in the first two parameters and returns the result into the address. Integers are subtracted and if two strings are inputed, all instances of the second string inside the first string will be deleted. Values must contain the same type.
* mul - mul (any) (any) &address&
  * multplies the two values in the first two parameters and returns the result into the address. Integers are multplied. If a string is multiplied by an positive int, the string will be duplicated that many times. If by zero, the string will be deleted. If by a negative int, the string will be reversed, then duplicated that many times. Strings and strings cannot be multplied.
* div - div (/int/ or &address&) (/int/ or &address&) &address&
  * divides the first integer by the second and returns the result to the address. Strings are not allowed
* sgn - sgn (/int/ or &address&) &address&
  * Short for "sign". Returns 1 if the integer is postive, 0 if it is 0, or -1 if it is negative. 


  




