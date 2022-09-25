# Jaseci Change / Release Notes

## Version 1.3.5

### Updates

- New Feature: Introduced `graph node view` API
- Major Improvement: Walkers are now proper architypes in stack, all code in architypes
- Improvement: Attributes like anchored and private are not fuzed with anchored objects.
- Improvement: Incompatible/outdated IR now rejected by Jaseci stack

## Version 1.3.4

### Updates

- Improvement: Indicator for being logged in in JSCTL
- New Feature: Email action set
- Major Feature: Async walkers
- Deprecation: Stripe API soft removed.
- Improvement: Improved the deref operator `*` to be more nimble
- New Feature: Can now pluck lists of values from collections of nodes and edges.
- Major Language Feature: Introducing the `yeild` feature. See bible for details
- Improvement/Bug: Here behavior is now specified for ability calls and inheritance in intuitive way
- Major Feature: Can now specify various forms of breadth first and depth first search on `take` commands (e.g., `take:bfs`, `take:dfs`, and `take:b` and `take:d` for short)
- Improvement: Added deep copy for lists and dictionaries
- Improvement: The connect operator between 2 nodes now returns the left-hand side. (e.g., `n1 --> n2 --> n3` will create an intuitive chain of connections not `n1 --> n3 <-- n2`)
- Bug Fix: Root nodes now return valid `.type`
- Bug Fix: With exit within walker now executes after exit events in nodes

### Notes

- Behavior change for jac programs utilizing chained connection operators. Connection orders are now intuitive (e.g., `n1 --> n2 --> n3` will create an intuitive chain of connections not `n1 --> n3 <-- n2`)
- API interface update: `sentinel_register` auto_run_ctx replaces ctx to be more specific, `auto_gen_graph` is now `auto_create_graph` for same reason as well
- API interface update: `master_create` API return format updated

## Version 1.3.3

### Updates

- Improvement: Added `reversed` to set of list builtin functions
- Bug Fix: Mem leak on graph node setting fixed
- Major Feature: Jsctl graph walking tooling
- Improvement: Optimized the self generation of jaseci internal APIs
- New Feature: Added `jaseci` standard library as patch through to all jaseci core APIs
- New Features: Report payloads can be customized with `report:custom`
- Improvement: Disengage can now do disengage with report action
- Improvement: import now works recursively through chain of files
- Improvement: JSCTL shows token on login
- Major Feature: JSCTL has persistent log in sessions, and can logout
- Improvement: `*` and `&` precedence hierarch locations improved.
- Bug Fix: Indirect node field updates tag elements to be written to db
- Major Feature: Multiple inheritance support on nodes and edges!
- Improvement: Fixed and much improved `actions load local` functionality
- Bug Fix: Globals imports of imports working
- Improvement: Sentinel registering improved to include ir mode
- Improvement: `edge` semantics improved
- Major bug fix: Re registering new code was breaking architype abilities
- Improvement: Tests now only show stdout and stderr on a test by test basis in detailed mode (Much cleaner)
- Improvement: JSKit package architecture established, normalized, and standardized
- New Lang Feature: Added list built in call of `.l::max`, `.l::min`, `.l::idx_of_max`, and `.l::idx_of_min`
- Improvement: Api so super masters can `become` any master id, also jsctl can issue `master allusers`
- New Lang Feature: Can now have `can` statements in spawn graphs after `has anchor rootname`
- Improvement: `actions load module` added as capability where module strings are accepted
- New Feature: Added global root finder `net.root` to std lib and `net.min` to go with existing `net.max`
- New Feature: New global element type and `global` keyword

### Notes

- Special report actions now use `:` instead of `.` eg `report.status = 200` is now `report:status = 200`

## Version 1.3.2

### Updates

- New Feature: Introduction of new standard library option for loading actions in Jac with `std.actload_local` and `std.actload_remote`
- Improvement: Disallowing spawning of unlinked edges, i.e., `spawn --> node::generic` not allowed without `here`
- New Feature: Random library adds random text generation lorem style with `rand.word()`, `rand.sentence()`, `rand.paragraph()`, and `rand.text()`.
- New Feature: Standard input `std.input(prompt)` :-p
- Improvement: Status codes auto plucked from return payload in jsserv
- New Feature: Can now control status codes with `report.status = 201` style statements
- Improvement: No longer saves action data into graph and keeps it in architypes
- New Feature: Walkers can be called directly using `wapi/{walkername}` api
- New Feature: New `master_allusers` API available for super master users
- Improvement: Superusers now have access to all data
- Improvement: Jaseci's admin api route changed to `/js_admin/...` vs `/admin/` to not conflict with Django's internals
- Update: Django 3 upgraded to latest as well as all other dependencies.
- Fix: Believe it or not, I never fully implemented `continue`. LIKE REALLY??? Anyway, fixed now. FTLOG!
- New Feature: Added `jac dot` cli command much like `jac run` but prints dot graph
- New Feature: Created shorthand for string, list, and dict functions i.e., `.s::`, `.d::`, and `.l::` respectively
- New Feature: Added suite of dict manipulation functions
- New Feature: Added suite of list manipulation functions

### Notes

- All api calls to Jaseci admin apis using the `/admin/` route must be updated to `/js_admin/`

## Version 1.3.1

### Updates

- New Feature: File I/O Library in with json support
- New Lang Feature: `.str::load_json` added to string library
- Fix: Error output when key not in object or dict
- New Lang Feature: Can now spawn root nodes in addition to generic nodes
- Improvement: Line numbers provided for all "Internal Errors"
- Fix: Dot strings now handled as expected (stripping quotes etc)
- Improvement: General improvements to error reporting
- Improvement: Changed meta requirement for actions to be option at hook points
- Improvement: Now you can arbitrarily chain array indexs into function calls as per `std.get_report()[0]`.
- New Feature: `std.get_report` gives the what is to be reported so far
- Improvement: General polish items of JSCTL UI
- Improvement: Raised the default core logging reporting level to warning

## Version 1.3

### Updates

- Improvement: JSCTL now takes args without flags in sensible places for quality of life.
- Improvement: Better Error reporting all around
- New Feature: APIs for manipulating actions
- New Feature: Hotloading jaseci action modules
- Update: New action creation methodology and architecture
- New Feature: Decorator interface for creating jaseci action modules
- New Feature: New profiling flag added to run walker api for performance profiling
- New Feature: Direct jac file building, test, and run from in JSCTL
- New Language Feature: Tests and testing features as first order language semantics
- New Lang Feature: Asserts!
- Fix: Simplified and optimized global abilities
- New Support Feature: Started vs code for JAC extension first beta
- New Lang Feature: Multifile codebase support and import keyword and semantic added
- New Lang Feature: Try-else blocks introduced for exception handling
- New Lang Feature: Added new `&` reference and `*` dereference semantic for getting psuedo-pointers to node, edges, etc
- New Lang Feature: Massively expanded functionality with destroy and list slice management
- New Lang Feature: can now explicitly reference and dereference graph elements (nodes, edges, etc)
- New Lang Feature: Field filtering for dictionaries, particularly useful for context, info, details
- New Lang Feature: Type checking primitives, and type casting primitives
- New Lang Feature: String library finally present

### Notes

- Various flags are now args for `jsctl` i.e., `walker run -name init` is now `walker run init` as name is now the standard arg. If you wanted to specify a node the flag would be used as per `walker run init -nd {uuid}`
- Reports back from walker is now dictionary of form `{'report': list(report)}` instead of currnet `list(report)`
- `std.sort_by_col` tweaked to make last paramter a boolean for reverse (instead of string)
- Format of `walker get -mode key` api changed from {key:namespace} to {namespace:key}
- `test` is now a keyword with added test capabilities in jaseci
- Type, int, float, str, list, dict, bool, are now keywords, if you used these as variable names in legacy code, must make updates.
- The destroy built-in is totally revised `lst.destroy(idx)` on lists should be changed to `destroy lst[idx]`.
- Get_uuid standard library function is deprecated since we have string manipulation
- Internal representation of element now `jac:uuid:` format, should not be visible to coder, `&` references still produce `urn:uuid:` as strings. To dereference use new `*` dereference operators.
- Standard, output and logging now will print proper values (e.g. json values for null, true, and false)

## Version 1.2.2

### Updates

- New Language Feature: can now perform assignments arbitrarily (not just to named variables)
- New Language Feature: can spawn assign on creation of nodes and edges
- New Language Feature: can filter references to nodes and edges
- Added new built-ins for nodes and edges (context, info, and details)
- Fixed dot output
- Added reset command to jsctl to clear complete state
- Various language grammar tweaks

## Version 1.2.1

### Updates

- Both jaseci and jaseci_serv are architected to be standalone packages
- Stripe API integrated
- EMails can be templated with HTML content
- Token expiry time can be set as config through live api
- Added auto sync to global sentinel for spawned walkers
- FIX: Global sentinels cascade to all users on change
- FIX: Multi pod concurrency issue corrected

## Version 1.2.0

### Updates

- New Hierarchal user creation and management through core Jaseci
- New version labels for Jac programs
- New custom action for nodes and edges
- New Jaseci server support for new API and Jaseci architecture
- New namespaces for public walker permissions management with key access
- New object sharing across users and access control APIs
- New Jaseci object permissions architecture
- New Jac library for outbound requests
- New Globals Jac standard library and API interfaces
- New support for server-side Jac deployments and relevant APIs
- New Jac language updates
- New access language features for edge manipulation and traversal
- New code IR format and handling across Architypes and Walkers
- New dot integration redesign
- New added editor to JSCTL
- New complete API redesign and deprecation of legacy APIs
- New introduced new standard Jaseci Bible (unfinished)
- New redesigned graphs nodes and edges to support multi-graph semantic.
