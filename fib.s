        ; This an example of computing the Fibonacci sequence.
        ; To illustrate the function call process, we'll jump ahead past our
        ; function, then call it.

pushl 21 ; address of the code following the function
skip    ; There is a delay slot after each skip. Here we discard the return
disc    ; address because we don't care about returning to this address

neg     ; We count up from -n to 0 rather than down from n to 0
        ; This is the easiest way to compensate for the strange asymmetric
        ; 'sign' instruction which returns either 0 or -1

pushl 2 ; To compute the nth fibonacci number, we need to
add     ; run the process below (n-2) times, so cancel two iterations
save    ; Then put the counter in the stash so we can use the stack for math

pushl 1 ; Put 1 and 1 on the stack to start our sequence
dup

        ; Between each iteration, the stack contains F(n-1) and F(n)
        ; The stash contains the (negative) number of iterations remaining
        ; Each iteration should leave F(n) and F(n+1) on the stack.

        ; example layout:                   stack | stash

dup     ; Here we save F(n) in the stash,    3 5 5|-3     <---+
save                                           3 5|5 -3       |
add     ; calculate F(n+1) = F(n) + F(n-1),      8|5 -3       |
rstor   ; restore F(n)                         8 5|-3         |
swap    ; and swap to put F(n+1) on the top    5 8|-3         |
        ;                                                     |
rstor   ; move the counter onto the stack   5 8 -3|           |
pushl 1 ; prepare to increment            5 8 -3 1|           |
add     ; increment                         5 8 -2|           |
dup     ; copy the counter               5 8 -2 -2|           |
save    ; push the copy back onto the stash 5 8 -2|-2         |
        ;                                                     |
sign    ; has the counter reached zero?         -1|-2         |
pushl 8 ; prepare to jump 8 bytes back          -1|-2         |
mul     ; multiply our offset by the sign       -8|-2         |
skip    ; actually jump now and ...          -8 13|-2  --->---+
disc    ; discard the return address            -8|-2  ; branch delay slot

        ; if we made it here, we finished computing F(n)
swap    ; throw out F(n-1)
disc
rstor   ; throw out the counter
disc    ; now F(n) is at the top of the stack

rstor   ; prepare to return - put the return address on the stack

neg     ; negate the return address; we will be subtracting this below
pushl 2 ; offset between the two skips below
dup     ; push a zero
sign
skip    ; put IP+1 on the stack
add     ; compute base of second skip as (2 + base of first skip)
add     ; compute skip distance as (base - fn addr)
neg     ; negate the distance
skip    ; now return to our caller
disc    ; and discard our current address


align   ; align this to a byte boundary so it's callable
        ; (we can't jump to the middle of a byte)

pushl 15 ; first we stage our first argument on the stack

dup     ; no-op to separate this from the next pushl
neg     ; otherwise we'd have to spend six cycles pushl'ing three zeroes
disc

pushl 3 ; then stage the absolute address of our function

        ; Illustration of an absolute function call

        ; skip works by applying a relative offset to the instruction pointer
        ; and leaving its current value on the stack. In order to set the
        ; instruction pointer to an absolute value, we need to skip a distance
        ; of zero to find our current location. Then we can do math
        ; to determine how far forward (or back) to skip

        ; An important consideration is ensuring that the second skip
        ; instruction is exactly 4 nibbles after the first. This is
        ; why some of the arithmetic is arranged oddly.

neg     ; negate the fn address; we will be subtracting this below
pushl 2 ; offset between the two skips below
dup     ; elaborate scheme to push a zero with 33% fewer nibbles
sign    ;
skip    ; put IP+1 on the stack
add     ; compute base of second skip as (2 + base of first skip)
add     ; compute skip distance as (base - fn addr)
neg     ; negate the distance
skip    ; now call the function
save    ; and save the return address

        ; we've returned from the function; the top of the stack
        ; is our return value

neg     ; do something with the result
pushl 1 ; and more things
add     ; etc ..
