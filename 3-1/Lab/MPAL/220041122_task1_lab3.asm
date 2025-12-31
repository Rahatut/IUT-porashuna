ORG 0100h

.DATA
input_string DB 'we are iut students', '$'
; code doesnt convert capitals to small for printing - requirement
;loop not used here, func(level) calls and recursion used  

.CODE

MAIN PROC
; print string
    LEA DX, input_string
    MOV AH, 9
    INT 21h


; new line
    MOV AH, 2
    MOV DL, 0DH
    INT 21h
    MOV DL, 0AH
    INT 21h


;read input char
    MOV AH, 1
    INT 21h
    MOV BL, AL   


; new line
    MOV AH, 2
    MOV DL, 0DH
    INT 21h
    MOV DL, 0AH
    INT 21h
    
; string for scanning
    LEA SI, input_string
    XOR DX, DX       


count_loop:
    MOV AL, [SI]
    CMP AL, '$'
    JE end_loop      

    CMP AL, BL
    JNE dont_inc
    INC DX            

dont_inc:
    INC SI
    JMP count_loop


end_loop:

    MOV AX, DX
    ADD AL, 48
    MOV DL, AL

    MOV AH, 2
    INT 21h

MOV AH, 4Ch
INT 21h
MAIN ENDP
END MAIN
