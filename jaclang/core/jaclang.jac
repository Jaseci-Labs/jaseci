"""Jac's Key Elemental Abstractions"""

import:jac from primitives, Element, Object, Node, Edge, Walker;


# object Element {
#     has _jinfo: ElementMetaData = ElementMetaData();

#     can _jac_make_public_ro;
#     can _jac_make_public_rw;
#     can _jac_make_private;
#     can _jac_is_public_ro -> bool;
#     can _jac_is_public_rw -> bool;
#     can _jac_is_private -> bool;
#     can _jac_is_readable(caller_id: UUID) -> bool;
#     can _jac_is_writable(caller_id: UUID) -> bool;
#     can _jac_give_access(caller_id: UUID, read_write: bool = False);
#     can _jac_revoke_access(caller_id: UUID);
# }

# object Object:Element {
#     static has _jac_ds_entry_funcs: list[dict]=[],
#                _jac_ds_exit_funcs: list[dict]=[];

#     static can _jac_on_entry(cls: type, triggers: list[type]);
#     static can _jac_on_exit(cls: type, triggers: list[type]);
# }

# object Node:Object {
#     has _jac_edges_: dict[EdgeDir, list[Edge]]
#         = {EdgeDir.IN: [], EdgeDir.OUT: []};

#     can __call__(walk: Walker);
#     can _jac_connect_node_(nd: Node, edg: Edge) -> Node;
#     can _jac_edges_to_nodes_(dir: EdgeDir) -> list[Node];
# }

# object Edge:Object {
#     has _jac_source_: Node?,
#         _jac_target_: Node?,
#         _jac_dir_: EdgeDir?;

#     can __call__(walk: Walker);
#     can _jac_apply_dir_(dir: EdgeDir) -> Edge;
#     can _jac_attach_(src: Node, trg: Node) -> Edge;
# }

# object Walker:Object {
#     has _jac_path_: list[Node] = [],
#         _jac_next_: list[Node] = [],
#         _jac_disengaged_: bool = False;

#     can __call__(nd: Node);
#     can _jac_visit_(nds: list[Node]|list[Edge]);
#     can _jac_disengage_;
# }

# object Master:Element {
#     has root_node: Node = Node();
# }

# can make_architype(base_class: type) -> type;