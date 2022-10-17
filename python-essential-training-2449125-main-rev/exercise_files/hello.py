
# Print "hello, world!" to the terminal
import imp


from termcolor import colored, cprint

cprint('Hello, World!', 'red')
text = colored('Hello ,World', 'green', attrs=['reverse', 'blink'])
print(text)