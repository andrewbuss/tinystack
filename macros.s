defmacro not dup nand
defmacro and nand not
defmacro or not swap not nand
defmacro ldchar ld 255 and
