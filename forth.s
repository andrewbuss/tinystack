include macros.s

; we can't yet jump to labels we haven't defined (lazy assembler author!)
; so we hardcode the address of our main Forth program after our definitions

start:
    0x50    ; address of our program
    dup     ; keep a copy on the stack for the interpreter's use
    save
    ld      ; load the address of the interpreter
    jmp     ; start executing!

forth_enter_code: ; This is the core of the interpreter
                  ; We set up the return stack then
                  ; start executing the first word

forth_native_epilogue: ; This is also the same code which runs after
                       ; each native definition
    rstor   ;
    2       ; step to the next item in the list
    add     ;

    dup     ; save this value for later use
    save    ;

    ld      ; load the address of the first word of the definition
    dup     ; and save it as well so the interpreter can use it if needed
    save    ;

    ld      ; load the address of the interpreter of the definition
    jmp     ; and run it!

; these make for prettier native fn defs

defmacro forth_native_defn $+2 rstor disc
defmacro forth_native_defn_end forth_native_epilogue jmp

align 2
forth_litword:    ; Put the next word on the stack
forth_native_defn
    rstor
    2
    add
    dup
    save
    ld
forth_native_defn_end

align 2
forth_add:        ; TOS = TOS + NOS
forth_native_defn
    add
forth_native_defn_end

align 2
forth_sub:        ; TOS = NOS - TOS
forth_native_defn
    neg
    add
forth_native_defn_end

align 2
forth_next:       ; Pop one element off the return stack
forth_native_defn
    rstor
    disc
forth_native_defn_end

align 2
forth_dup:        ; Same as native dup
forth_native_defn
    dup
forth_native_defn_end

align 2
forth_exit:       ; Exit the interpreter
forth_native_defn
    rstor
    disc
    1
    neg
    jmp

; Now we've defined a bunch of native functions
; we can start to define threaded functions which
; simply comprise lists of addresses

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
align 0x50
&forth_enter_code
    &forth_litword
    &0xfeed
    &forth_quadruple
    &forth_quadruple
    &forth_quadruple
    &forth_litword
    &0x100
    &forth_quadruple
    &forth_add
    &forth_litword
    &0x51
    &forth_sub
&forth_exit