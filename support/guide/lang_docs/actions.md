# Actions

Actions enables bindings to functionality specified outside of Jac/Jaseci and behave as function
calls with returns. These are analogous to library calls in traditional languages. This external
functionality in practice takes the form of direct binding to python implementations that are
packaged up as a Jaseci action library.

> **Note**
>
> This action interface is the abstraction that allows Jaseci to do it's sophisticated serverless inter-machine optimizations, auto-scaling, auto-componentization etc.
