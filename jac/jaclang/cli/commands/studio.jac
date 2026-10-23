comptime SPEC_STUDIO: CommandSpec = CommandSpec(
         name="studio",
         help="Open the studio: a compiler-backed terminal workspace for coding agents",
         args=[
             Arg.create(
                 "action",
                 kind=ArgKind.POSITIONAL,
                 `default="",
                 help="(none) open the workspace | model | ask | agents | sessions | mcp"
             ),
             Arg.create(
                 "args",
                 kind=ArgKind.REMAINDER,
                 `default=[],
                 help="Arguments for the action (a module or symbol, an instruction, ...)"
             ),
             Arg.create(
                 "agent",
                 `default="",
                 short="a",
                 help="Agent to drive (see `jac studio agents`)"
             ),
             Arg.create(
                 "session",
                 `default="",
                 short="s",
                 help="Session id to resume (see `jac studio sessions`)"
             ),
             Arg.create(
                 "json",
                 kind=ArgKind.FLAG,
                 typ=bool,
                 `default=False,
                 dest="as_json",
                 help="Print JSON instead of text"
             ),
             Arg.create(
                 "dir",
                 `default="",
                 short="d",
                 dest="directory",
                 help="Project directory (default: the project around the current directory)"
             ),

         ],
         examples=[
             ("jac studio", "Open the workspace on the current project"),
             (
                 "jac studio model --json",
                 "Dump the project model: modules, wires, rules and symbols"
             ),
             ("jac studio model core.jobs", "Show one module's wiring and symbols"),
             (
                 "jac studio ask core.jobs.Runner.start \"add retry with backoff\"",
                 "Hand a symbol and an instruction to an agent without the UI"
             ),
             ("jac studio agents", "List the agents the studio can drive"),
             ("jac studio sessions", "List saved sessions"),

         ],
         group="tools",
         handler_name=ct_name(studio)
     );

def studio(
    action: str = "",
    args: list[str] = [],
    agent: str = "",
    session: str = "",
    as_json: bool = False,
    directory: str = ""
) -> int;

impl studio(
    action: str = "",
    args: list[str] = [],
    agent: str = "",
    session: str = "",
    as_json: bool = False,
    directory: str = ""
) -> int {
    return run_studio(action, args, agent, session, as_json, directory);
}
