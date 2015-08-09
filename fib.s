pushl 24 ; Compute the 24th Fibonacci number

neg     ; We count up from -n to 0 rather than down from n to 0

pushl 2 ; To compute the nth fibonacci number, we need to
add     ; run the process below (n-2) times, so cancel two iterations
save    ; Then put the counter in the stash so we can use the stack for math

pushl 1 ; Put 1 and 1 on the stack to start our sequence
dup

        ; Between each iteration, the stack contains F(n-1) and F(n)
        ; The stash contains the (negative) number of iterations remaining
        ; Each iteration should leave F(n) and F(n+1) on the stack.

        ; example layout:                   stack | stash
dup     ; Here we save F(n) in the stash,    3 5 5|-3
save                                           3 5|5 -3
add     ; calculate F(n+1) = F(n) + F(n-1),      8|5 -3
rstor   ; restore F(n)                         8 5|-3
swap    ; and swap to put F(n+1) on the top    5 8|-3

rstor   ; move the counter onto the stack   5 8 -3|
pushl 1 ; prepare to increment            5 8 -3 1|
add     ; increment                         5 8 -2|
dup     ; copy the counter               5 8 -2 -2|
save    ; push the copy back onto the stash 5 8 -2|-2

sign    ; has the counter reached zero?         -1|-2
pushl 9 ; if so, prepare to jump 8 bytes back -1 8|-2
mul     ; multiply our offset by the sign       -8|-2
dup
disc
skip    ; actually jump now and ...          -8 13|-2
disc    ; discard the return address            -8|-2  ; branch delay slot

        ; if we made it here, we finished computing F(n)
swap    ; throw out F(n-1)
disc
rstor   ; throw out the counter
disc

disc    ; now F(n) is at the top of the stack