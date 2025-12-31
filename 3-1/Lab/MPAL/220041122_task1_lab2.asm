ORG 0100h             

; input a character
MOV AH, 1
INT 21h
MOV BL, AL

; go to a new line with carriage return
MOV AH, 2
MOV DL, 0DH
INT 21h
MOV DL, 0AH
INT 21h 

;divisible by 2
AND BL, 1 
CMP BL, 0
jz  PRINT_E
jz  PRINT_O


;printing o or e 
PRINT_O: MOV AH, 2
         MOV DL, 'O'
         INT 21h 
         JMP EXIT
 

PRINT_E: MOV AH, 2
         MOV DL, 'E'
         INT 21h   
         JMP EXIT
         
EXIT: MOV AH, 04CH
      INT 21H  
      
      

