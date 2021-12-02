# Jaseci Release Notes

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
