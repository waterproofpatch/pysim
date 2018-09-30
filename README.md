# PySim
Rudimentary language executed by an interpreter written in Python. The language specification is simple and not intended to be practical for 'real-world' use, but rather an example of how a user-defined langguage can be interpted.

There is no compilation step - tokens are extracted as they are in the human-readable format from a text file and a simple execution engine updates internal 'program state' based on these tokens.

## Installation:
```
make install
```

## Usage:
```
python3 pysim/sim.py --program ../programs/prog1.s
```

## Documentation:
Build the documentation:
```
make doc
open doc/build/html/index.html
```

#### Language Specification:
The following verbs are supported:
* add
    * `add $1, $2 // add contents of register 2 to register 1, place result in register 1`
    * `add $1, #1234 // add literal 1234 to register 1, place result in register 1`
* sub
    * `sub $1, $2 // subtract contents of register 2 from register 1, place result in register 1`
    * `sub $1, #1234 // subtract literal 1234 from register 1, place result in register 1`
* put
    * `put $1, #4 // put a literal into register 1`
    * `put $1, $2 // put contents of register 2 into register 1`

See the example program in programs/prog1.s.

