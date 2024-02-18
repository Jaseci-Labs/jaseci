enum Color;

with entry {
    print(Color.RED.value);
}

:enum:Color {
    RED=1,
    pencil,
    ::py::
    print('text')
    ::py::
}
