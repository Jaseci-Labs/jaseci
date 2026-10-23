# Jac Studio

`jac studio` is a terminal workspace for working on a Jac codebase with coding agents. It is built into the `jac` binary and backed by the compiler: the project is loaded into a graph of packages, modules, archetypes, abilities and impls joined by the wiring in `archwire.jac`, and every view and every piece of context an agent receives comes from that graph.

There is no text editor. You point at compiler-level things (a module, an archetype, an ability, a wire), put them in the context tray, and tell an agent what to do with them. Agents make the edits, and the compiler checks each edit before it reaches disk.

```bash
jac studio                      # open the workspace on the project around the current directory
jac studio -d path/to/project   # open another project
jac studio -a claude            # choose the agent for this session
jac studio -s 20261023-0012     # resume a saved session (a unique prefix is enough)
```

## The workspace

| Pane | What it shows |
|------|---------------|
| Navigator | Packages, modules, archetypes, abilities and fields. A `●` marks symbols changed in this session. |
| Code | The selected file, read-only, with semantic highlighting, hover, diagnostics and inferred types inline. |
| Wiring | For the focused module: the modules that feed it, the module itself with the rules that govern it, and the modules it feeds, with the names each wire carries. A wire that breaks a rule is marked `⚠` with the reason. |
| Map | The architecture map: the wiring between packages, one level of the package hierarchy at a time. See [The architecture map](#the-architecture-map). |
| Agent | The transcript: messages, collapsible tool calls, the agent's plan and command output. |
| Context | The tray: everything you selected for the next request. |
| Prompt | Your instruction. Slash verbs act on the tray. |

The centre pane switches between code and wiring with `Ctrl+T` (or `w` in the navigator or code view), and to the architecture map with `m`.

## Keys

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Move focus between panes |
| `Ctrl+P` | Go to any module or symbol (`Tab` in the list adds it to the context) |
| `m` | Architecture map of the package around the selection |
| `Ctrl+X` | Command palette |
| `Ctrl+L` | Jump to the prompt |
| `F1` | All keys |
| `Ctrl+C` | Cancel the agent's turn; press twice to quit |
| `Ctrl+Q` | Quit |
| `Alt+←` / `Alt+→` | Move the edge of the focused pane |

In the navigator and code view, `Space` (or `a`) adds the item under the cursor to the context. In the code view, `Enter` or `d` goes to the definition, `r` lists references, `i` jumps between a declaration and its impl, `e` moves to the next diagnostic, and `t` shows or hides inferred types. In the wiring view, `←` and `→` move between the columns, `Enter` follows a wire, `Space` adds a wire or symbol to the context, and `A` adds a whole column.

In the transcript, `↑` and `↓` select an entry. `Enter` expands a tool call, or on the plan opens the code its steps are linked to. `o` opens the files a tool call touched.

## The architecture map

`m` in the navigator or code view opens the map on the package that holds the selected item, with the item selected. Each level groups the modules under one package by their next name segment, so a level shows sub-packages and modules side by side, and adds up the wires between them. Groups are ordered providers first: a group comes before the groups it feeds wherever the wiring allows it.

The map has three views of the same level; `v` cycles them and `1`, `2`, `3` pick one.

| View | Shows |
|------|-------|
| Matrix | Every pair of groups. The row feeds the column, and each number is a count of wires. Numbers right of the diagonal follow the provider order; a number left of it is a backward wire, where a later group feeds an earlier one. Backward counts are yellow and counts that include a rule violation are red. `↻` marks groups that sit in a cycle. |
| Layers | Groups stacked by depth: layer 0 is fed by nothing at this level, and every forward wire goes to a higher layer. Selecting a group lights up what feeds it, what it feeds, and the rest of its cycle. |
| Issues | What keeps the level from being cleanly layered: wires that break a rule, backward wires (largest first), and cycles. |

Under each view, the selected group shows its module count, layer, cycle, governing rules, and the groups it feeds and is fed by with wire counts (`↺` marks a backward one). A selected matrix cell shows the dependency: its wire count, a sample wire, and whether the two groups depend on each other.

| Key | Action |
|-----|--------|
| Arrows | Move. In the matrix, `d` jumps to the diagonal and `t` swaps the row and column |
| `Enter` | Open a package (its level), show a module in the wiring view, or list the wires behind a number |
| `Backspace` / `u` | Up one level |
| `Space` | Add the selection to the context: a module, a package's map, or the wires behind a dependency |
| `A` | Add the whole level to the context |
| `w` | Show the selected module in the wiring view |

A package's map in the context reaches the agent as the level in text: its groups by layer, the matrix, the backward wires and the cycles. A dependency reaches it as the list of wires with the names each carries. The map follows `archwire.jac`: change a wire and the level is recomputed.

## Telling an agent what to do

Select what the request is about, then type it in the prompt. `@` in the prompt adds something to the context without leaving the keyboard. Each item in the tray is sent to the agent as a typed block: the declaration together with its impl body, its signature, what uses it and what it uses, the wires that carry it, and the rules that govern its module.

Slash verbs turn the tray into a request:

| Verb | Asks the agent to |
|------|-------------------|
| `/explain` | Explain the selected code and how it is wired |
| `/tests` | Write tests that follow the project's conventions |
| `/refactor` | Refactor without changing behaviour, keeping the wiring valid |
| `/review` | Report bugs and risky assumptions without editing |
| `/doc` | Add or improve docstrings and `sem` strings |
| `/fix` | Fix the problems in the selected code |
| `/move` | Move the selected code to another module and rewire `archwire.jac` |

Add your own verbs under `[studio.verbs]` in `jac.toml`.

## Compiler-checked edits

When an agent writes a file, the write is held while the compiler checks the new text in an overlay. The approval sheet shows:

- whether the edit compiles, and how long the check took;
- each symbol it adds, changes or removes;
- new errors and warnings, and existing diagnostics it fixes;
- architecture changes (wires or rules added, removed or changed);
- the diff.

| Key | Action |
|-----|--------|
| `a` | Accept the edit |
| `1`-`9` | Toggle one symbol change; `a` then applies only the selected ones |
| `A` | Approve an architecture change and accept the edit |
| `r` | Reject |
| `f` | Reject and send the compiler's findings back to the agent |

An edit that changes the architecture cannot be accepted with `a`; it always needs `A`. When you accept part of an edit, the studio writes the kept changes and tells the agent which changes were dropped.

Reads, searches, the jac and studio MCP tools, and edits are allowed without asking, because every write is reviewed here. Other tool calls, such as shell commands, ask first. `[studio] auto_allow` adds tool kinds or title fragments to the allowed set.

## Agents

```bash
jac studio agents
```

The studio drives any agent that speaks the [Agent Client Protocol](https://agentclientprotocol.com): Claude Code and Codex through their ACP adapters, Gemini CLI, or any command you configure. Every agent is started with two MCP servers: `jac mcp` for the compiler tools, and the studio's own server, which gives the agent these tools:

| Tool | Returns or does |
|------|-----------------|
| `studio_selection` | The context tray, the file and symbol under the cursor, and the module in the wiring view |
| `studio_focus` | Shows a module, symbol or file location to the user, with an optional note |
| `studio_wiring` | A module's providers, consumers and governing rules |
| `studio_rules` | Every rule and the modules it covers |
| `studio_graph` | One level of the architecture map: groups by layer, wire counts between them, backward wires and cycles |
| `studio_symbol` | A declaration with its impl, users, uses and the walkers that visit it |
| `studio_search` | Fuzzy search over modules and symbols |
| `studio_link_plan` | Links each step of the agent's plan to the code it touches |

The built-in agent, `jac`, runs on byLLM inside the studio. It needs byLLM's model client: add `[byllm]` to `jac.toml` and run `jac install`. Choose its model with `[studio] model`, or byLLM's `default_model`.

## Headless use

```bash
jac studio model                       # summary of the project model
jac studio model geo.shape --json      # one module, as JSON
jac studio model geo.shape.Circle      # a symbol: members, impls, users, uses, walkers
jac studio graph                       # the architecture map of the project, as text
jac studio graph core --json           # one package's level, as JSON
jac studio ask geo.shape.Circle "add a perimeter method" -a claude --yes
jac studio sessions                    # saved sessions
jac studio sessions fork <id>          # copy a session to take it in another direction
```

`jac studio ask` hands a symbol or module and an instruction to an agent without the UI. With `--yes` it approves permission requests and writes, so use it only where that is safe.

## Sessions

The transcript, the context tray and every decision you made are saved on a root graph in the project's `.jac/studio` store when you quit. `jac studio -s <id>` reopens a session in the same state, and `jac studio sessions fork <id>` copies one so you can try a different direction.

## Configuration

```toml
[studio]
default_agent = "claude"           # agent used when -a is not given
model = "anthropic/claude-sonnet-5-5"   # model for the built-in agent
gate = "ask"                       # ask | auto | strict | off
auto_allow = ["execute"]           # more tool kinds or title fragments to allow

[studio.verbs]
perf = "Find the hot paths in the selected code and make them faster."

[studio.agents.mine]
command = "my-agent"
args = ["--acp"]
env = { MY_AGENT_MODE = "acp" }
```

| `gate` | Behaviour |
|--------|-----------|
| `ask` | Every edit waits for you, with the compiler's verdict (default) |
| `auto` | Clean edits are accepted and broken ones are sent back with the compiler's findings; architecture changes still wait for you |
| `strict` | Broken edits are sent back; clean ones wait for you |
| `off` | Edits wait for you without a compiler check |

Settings in `~/.jac/studio.toml` (or the file named by `JAC_STUDIO_CONFIG`) apply to every project; the project's `jac.toml` takes precedence.

## Performance

The workspace opens before the project is indexed: the navigator shows the module tree at once, and symbols fill in from a background index. On the jaclang compiler itself (about 5,800 modules), the first frame appears in under 7 seconds. Code intelligence is per file, so hover, definitions and diagnostics for the open file do not wait for the full index.
