'''
bits 32

foo:
    push ebp
    mov ebp, esp
    mov ecx,[ebp+8]
    xor edx,edx
    cmp ecx,edx
    jz bar

    mov eax, 1

bar:
    mov eax, 2

baz:
    mov esp, ebp
    pop ebp
    ret
'''
func1 = b'\x55\x89\xe5\x8b\x4d\x08\x31\xd2\x39\xd1\x74\x05\xb8\x01\x00\x00\x00\xb8\x02\x00\x00\x00\x89\xec\x5d\xc3'

