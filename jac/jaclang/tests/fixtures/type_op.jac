node N {}
walker M {}
edge E {}
obj O {}

glob n = N();
glob m = M();
glob e = E();
glob o = O();

with entry {
    print(`root); # This prints the type of root which is Root
    print(`n); # This prints the type of n which is NodeArchitype
    print(`m); # This prints the type of m which is WalkerArchitype
    print(`e); # This prints the type of e which is EdgeArchitype
    print(`o); # This prints the type of o which is Architype

}
