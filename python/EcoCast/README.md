This is a start for a pyhton lib hierarchy.
The name of 'EcoCast' might need to be changed later.

Later I can made this module can be installed as a python lib with a CLI entrance.

For loading module it can be more pythonic.

for example,

>> import EcoCast.chip.cc2540.mcu
>> import EcoCast.compiler.gcc.mapfile

or we can just load a suite

>> import EcoCast.cc2540

To adopt this kind of structure, some general interface can be provide at the top level,
the corresponded backend need to load differently.


