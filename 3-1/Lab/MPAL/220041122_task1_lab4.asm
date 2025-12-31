org 100h
.DATA ; Data segment starts 

ODD_ARRAY db 1, 3, 5, 7, 9
EVEN_ARRAY db 2, 4, 6, 8


ODD_SUM db 00h
EVEN_SUM db 00h

msg1 db 'Enter the value of N(1-9):$'
msg2 db 'ODD SUM: $'
msg3 db 'EVEN SUM: $'    

  
.CODE ; Code segment starts
MAIN PROC
    mov ax, @DATA
    mov ds, ax     

    mov dx, OFFSET msg1 ; Load Effective Address of the message in DX register;
    mov ah, 09h ;display string function
    int 21h ;display message 
    
    mov ah, 01h
    int 21h 
    sub al, 48
    mov cl, al; cl = N  
    mov bh, al
    xor ch, ch
         
    xor al, al   
    mov si, OFFSET ODD_ARRAY
    

ODD_LOOP:
    mov al, [Si] 
    mul al
    add ODD_SUM, al
    inc Si
    loop ODD_LOOP        
    
        
    mov cl, bh
    xor ch, ch
    xor al, al
    mov si, OFFSET EVEN_ARRAY
    
EVEN_LOOP:
    mov al, [Si] 
    mul al
    add EVEN_SUM, al
    inc Si
    loop EVEN_LOOP


    mov dx, OFFSET msg2
    mov ah, 09h ;display string function
    int 21h ;display message 
    
    mov al, ODD_SUM
    add al, 48
    mov dl, al 
    mov ah, 02h
    int 21h  
    
        
    mov dx, OFFSET msg3
    mov ah, 09h ;display string function
    int 21h ;display message 
    
    mov al, EVEN_SUM
    add al, 48
    mov dl, al  
    mov ah, 02h
    int 21h
    
mov ah, 4Ch
int 21h
MAIN ENDP
END MAIN




