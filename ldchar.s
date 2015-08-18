dup     ; c c
ld      ; c *c
swap    ; *c c
8       ; *c c 8
swap    ; *c 8 c
1       ; *c 8 c 1
and     ; *c 8 rotate?
rol     ; *c rotate_dist
rol     ; *c<<rotate_dist
255
and     ; (*c << rotate_dist) & 0xff