comptime SPEC_STUDIO: CommandSpec = CommandSpec(
         name="studio",
         help="Open the studio: a compiler-backed terminal workspace for coding agents",
         args=[
             Arg.create(
                 "action",
                 kind=ArgKind.POSITIONAL,
                 `default="",
                 help="(none) open the workspace | model | graph | roles | interface | rules | slice | blast | clusters | tour | diff | ask | agents | sessions | mcp"
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
                 "jac studio graph core",
                 "Show the wiring between a package's parts: layers, matrix, backward wires and cycles"
             ),
             (
                 "jac studio roles",
                 "Sort modules into foundations, hubs, integrators and entry points"
             ),
             (
                 "jac studio interface core",
                 "List the names that cross a package's boundary, and who uses each"
             ),
             (
                 "jac studio rules",
                 "Compare the archwire rules with the wires: unused permissions and violations"
             ),
             (
                 "jac studio slice app.main",
                 "Show everything an entry point rests on, step by step"
             ),
             (
                 "jac studio blast core.jobs.Runner",
                 "Show what depends on a module or a name"
             ),
             (
                 "jac studio clusters core",
                 "Compare the declared packages with the clusters the wiring implies"
             ),
             (
                 "jac studio tour",
                 "Write an onboarding tour of the codebase from its wiring"
             ),
             (
                 "jac studio diff main",
                 "Show how the architecture changed since a git revision"
             ),
             (
                 "jac studio ask core.jobs.Runner.start \"add retry with backoff\"",
                 "Hand a symbol and an instruction to an agent without the UI"
             ),
             ("jac studio agents", "List the agents the studio can drive"),
             ("jac studio sessions", "List saved sessions"),
             (
                 "jac studio sessions fork <id>",
                 "Copy a session to try a different direction"
             ),

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
