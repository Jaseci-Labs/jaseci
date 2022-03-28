# Jaseci Change / Release Notes

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
