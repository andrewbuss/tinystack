include macros.s
0x1000
dup
save
ld
jmp

align 0x8
forth_enter_code:
forth_native_epilogue:
rstor
2
add
dup
save
ld
dup
save
ld
jmp

align 0x20

align 2
forth_litword:
$+2
rstor
disc
rstor
2
add
dup
save
ld
forth_native_epilogue
jmp

align 2
forth_add:
$+2
rstor
disc
add
forth_native_epilogue
jmp

align 2
forth_sub:
$+2
rstor
disc
neg
add
forth_native_epilogue
jmp

align 2
forth_next:
$+2
rstor
disc
rstor
disc
forth_native_epilogue
jmp

align 2
forth_dup:
$+2
rstor
disc
dup
forth_native_epilogue
jmp

align 2
forth_exit:
$+2
rstor
disc
rstor
disc
1
neg
jmp

align 2
forth_double:
&forth_enter_code
&forth_dup
&forth_add
&forth_next

align 2
forth_quadruple:
&forth_enter_code
&forth_double
&forth_double
&forth_next

; Main program
; Here we convert feed to beef!
align 0x1000
&forth_enter_code
&forth_litword
&0xfeed
&forth_quadruple
&forth_quadruple
&forth_quadruple
&forth_litword
&0x3af
&forth_add
&forth_exit