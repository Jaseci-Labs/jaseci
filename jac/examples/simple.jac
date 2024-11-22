# @decorator1
# @decorator2
::py::
def codon (func):
    print("deco")
    func()

::py::

can foo {
    print("Hello");
}