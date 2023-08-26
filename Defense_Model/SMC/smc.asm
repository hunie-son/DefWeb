[section .text]

align 64
payload:
    ret

%define BUFFER_STEP 64

align 64
[global smc]
; rdi: bufferPtr
; rsi: bufferEndPtr
smc:
    push r10
    push r11
    push r12

    mov rax, 800
    mov r10, rdi ; r10 points to begin of buffer
    mov r11, rdi ; r11 points to current buffer position
    mov r12, rsi ; r12 points to end of buffer

.loop:
    ; Done?
    dec rax
    je .end
    
    mov rcx, 64
    mov rdi, r11
    lea rsi, [rel payload]
    
    ; Store
    rep movsb
    
    ; Call
    call r11
    
    ; Move buffer pointer
    lea r11, [r11 + BUFFER_STEP]
    cmp r11, r12
    jb .next
    mov r11, r10

.next:
    jmp .loop

.end:
    pop r12
    pop r11
    pop r10
    ret
