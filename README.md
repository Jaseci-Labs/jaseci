# Jaseci Release Notes

## Version 1.3

### Updates

- New Lang Feature: Massively expanded functionality with destroy and list slice management
- New Lang Feature: can now explicitly reference and dereference graph elements (nodes, edges, etc)
- New Lang Feature: Field filtering for dictionaries, particularly useful for context, info, details
- New Lang Feature: Type checking primitives, and type casting primitives
- New Lang Feature: String library finally present

### Notes

- type, int, float, str, list, dict, bool, are now keywords, if you used these as variable names in legacy code, must make updates.
- the destroy built-in is totally revised `lst.destroy(idx)` on lists should be changed to `destroy lst[idx]`.
- get_uuid standard library function is deprecated since we have string manipulation
- internal representation of element now `jac:uuid:` format
- standard, output and logging now will print proper values (e.g. json values for null, true, and false)

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
