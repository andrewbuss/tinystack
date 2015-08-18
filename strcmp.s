dup     ; a b b
ldchar  ; a b *b
swap    ; a *b b
save    ; a *b | b
swap    ; *b a | b
dup     ; *b a a | b
ldchar  ; *b a *a | b
swap    ; *b *a a | b
save    ; *b *a | a b

