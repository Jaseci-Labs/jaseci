import from jaclang.cli.command { Arg, ArgKind, CommandSpec }
import from jaclang.comptime { name as ct_name }


comptime SPEC_KERNEL: CommandSpec = CommandSpec(
         name="kernel",
         help="Build or inspect the native compiler kernel of a source checkout",
         hidden=True,
         args=[
             Arg.create(
                 "action",
                 kind=ArgKind.POSITIONAL,
                 `default="status",
                 help="Action: status (default), build"
             ),
             Arg.create(
                 "force",
                 typ=bool,
                 `default=False,
                 help="With build: relink even when the kernel matches the sources",
                 short="f"
             ),

         ],
         examples=[
             (
                 "jac kernel status",
                 "Which kernel this checkout runs and, when it runs from bytecode, "
                 "which compiler sources moved since the kernel was built"
             ),
             (
                 "jac kernel build",
                 "Build the kernel for the checkout's sources; unchanged units are reused"
             ),
             (
                 "JAC_DEV_EXACT=1 jac kernel build --force",
                 "Rebuild every kernel unit with the compiler as edited"
             ),

         ],
         group="tools",
         handler_name=ct_name(kernel)
     );

def kernel(action: str = "status", force: bool = False) -> int;
