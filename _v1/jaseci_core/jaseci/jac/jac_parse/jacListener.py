# Generated from jac.g4 by ANTLR 4.9.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .jacParser import jacParser
else:
    from jacParser import jacParser


# This class defines a complete listener for a parse tree produced by jacParser.
class jacListener(ParseTreeListener):
    # Enter a parse tree produced by jacParser#start.
    def enterStart(self, ctx: jacParser.StartContext):
        pass

    # Exit a parse tree produced by jacParser#start.
    def exitStart(self, ctx: jacParser.StartContext):
        pass

    # Enter a parse tree produced by jacParser#ver_label.
    def enterVer_label(self, ctx: jacParser.Ver_labelContext):
        pass

    # Exit a parse tree produced by jacParser#ver_label.
    def exitVer_label(self, ctx: jacParser.Ver_labelContext):
        pass

    # Enter a parse tree produced by jacParser#import_module.
    def enterImport_module(self, ctx: jacParser.Import_moduleContext):
        pass

    # Exit a parse tree produced by jacParser#import_module.
    def exitImport_module(self, ctx: jacParser.Import_moduleContext):
        pass

    # Enter a parse tree produced by jacParser#import_items.
    def enterImport_items(self, ctx: jacParser.Import_itemsContext):
        pass

    # Exit a parse tree produced by jacParser#import_items.
    def exitImport_items(self, ctx: jacParser.Import_itemsContext):
        pass

    # Enter a parse tree produced by jacParser#import_names.
    def enterImport_names(self, ctx: jacParser.Import_namesContext):
        pass

    # Exit a parse tree produced by jacParser#import_names.
    def exitImport_names(self, ctx: jacParser.Import_namesContext):
        pass

    # Enter a parse tree produced by jacParser#element.
    def enterElement(self, ctx: jacParser.ElementContext):
        pass

    # Exit a parse tree produced by jacParser#element.
    def exitElement(self, ctx: jacParser.ElementContext):
        pass

    # Enter a parse tree produced by jacParser#global_var.
    def enterGlobal_var(self, ctx: jacParser.Global_varContext):
        pass

    # Exit a parse tree produced by jacParser#global_var.
    def exitGlobal_var(self, ctx: jacParser.Global_varContext):
        pass

    # Enter a parse tree produced by jacParser#architype.
    def enterArchitype(self, ctx: jacParser.ArchitypeContext):
        pass

    # Exit a parse tree produced by jacParser#architype.
    def exitArchitype(self, ctx: jacParser.ArchitypeContext):
        pass

    # Enter a parse tree produced by jacParser#walker_block.
    def enterWalker_block(self, ctx: jacParser.Walker_blockContext):
        pass

    # Exit a parse tree produced by jacParser#walker_block.
    def exitWalker_block(self, ctx: jacParser.Walker_blockContext):
        pass

    # Enter a parse tree produced by jacParser#test.
    def enterTest(self, ctx: jacParser.TestContext):
        pass

    # Exit a parse tree produced by jacParser#test.
    def exitTest(self, ctx: jacParser.TestContext):
        pass

    # Enter a parse tree produced by jacParser#namespaces.
    def enterNamespaces(self, ctx: jacParser.NamespacesContext):
        pass

    # Exit a parse tree produced by jacParser#namespaces.
    def exitNamespaces(self, ctx: jacParser.NamespacesContext):
        pass

    # Enter a parse tree produced by jacParser#walk_entry_block.
    def enterWalk_entry_block(self, ctx: jacParser.Walk_entry_blockContext):
        pass

    # Exit a parse tree produced by jacParser#walk_entry_block.
    def exitWalk_entry_block(self, ctx: jacParser.Walk_entry_blockContext):
        pass

    # Enter a parse tree produced by jacParser#walk_exit_block.
    def enterWalk_exit_block(self, ctx: jacParser.Walk_exit_blockContext):
        pass

    # Exit a parse tree produced by jacParser#walk_exit_block.
    def exitWalk_exit_block(self, ctx: jacParser.Walk_exit_blockContext):
        pass

    # Enter a parse tree produced by jacParser#walk_activity_block.
    def enterWalk_activity_block(self, ctx: jacParser.Walk_activity_blockContext):
        pass

    # Exit a parse tree produced by jacParser#walk_activity_block.
    def exitWalk_activity_block(self, ctx: jacParser.Walk_activity_blockContext):
        pass

    # Enter a parse tree produced by jacParser#attr_block.
    def enterAttr_block(self, ctx: jacParser.Attr_blockContext):
        pass

    # Exit a parse tree produced by jacParser#attr_block.
    def exitAttr_block(self, ctx: jacParser.Attr_blockContext):
        pass

    # Enter a parse tree produced by jacParser#attr_stmt.
    def enterAttr_stmt(self, ctx: jacParser.Attr_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#attr_stmt.
    def exitAttr_stmt(self, ctx: jacParser.Attr_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#struct_block.
    def enterStruct_block(self, ctx: jacParser.Struct_blockContext):
        pass

    # Exit a parse tree produced by jacParser#struct_block.
    def exitStruct_block(self, ctx: jacParser.Struct_blockContext):
        pass

    # Enter a parse tree produced by jacParser#can_block.
    def enterCan_block(self, ctx: jacParser.Can_blockContext):
        pass

    # Exit a parse tree produced by jacParser#can_block.
    def exitCan_block(self, ctx: jacParser.Can_blockContext):
        pass

    # Enter a parse tree produced by jacParser#graph_block.
    def enterGraph_block(self, ctx: jacParser.Graph_blockContext):
        pass

    # Exit a parse tree produced by jacParser#graph_block.
    def exitGraph_block(self, ctx: jacParser.Graph_blockContext):
        pass

    # Enter a parse tree produced by jacParser#has_root.
    def enterHas_root(self, ctx: jacParser.Has_rootContext):
        pass

    # Exit a parse tree produced by jacParser#has_root.
    def exitHas_root(self, ctx: jacParser.Has_rootContext):
        pass

    # Enter a parse tree produced by jacParser#has_stmt.
    def enterHas_stmt(self, ctx: jacParser.Has_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#has_stmt.
    def exitHas_stmt(self, ctx: jacParser.Has_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#has_assign.
    def enterHas_assign(self, ctx: jacParser.Has_assignContext):
        pass

    # Exit a parse tree produced by jacParser#has_assign.
    def exitHas_assign(self, ctx: jacParser.Has_assignContext):
        pass

    # Enter a parse tree produced by jacParser#can_stmt.
    def enterCan_stmt(self, ctx: jacParser.Can_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#can_stmt.
    def exitCan_stmt(self, ctx: jacParser.Can_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#event_clause.
    def enterEvent_clause(self, ctx: jacParser.Event_clauseContext):
        pass

    # Exit a parse tree produced by jacParser#event_clause.
    def exitEvent_clause(self, ctx: jacParser.Event_clauseContext):
        pass

    # Enter a parse tree produced by jacParser#preset_in_out.
    def enterPreset_in_out(self, ctx: jacParser.Preset_in_outContext):
        pass

    # Exit a parse tree produced by jacParser#preset_in_out.
    def exitPreset_in_out(self, ctx: jacParser.Preset_in_outContext):
        pass

    # Enter a parse tree produced by jacParser#dotted_name.
    def enterDotted_name(self, ctx: jacParser.Dotted_nameContext):
        pass

    # Exit a parse tree produced by jacParser#dotted_name.
    def exitDotted_name(self, ctx: jacParser.Dotted_nameContext):
        pass

    # Enter a parse tree produced by jacParser#name_list.
    def enterName_list(self, ctx: jacParser.Name_listContext):
        pass

    # Exit a parse tree produced by jacParser#name_list.
    def exitName_list(self, ctx: jacParser.Name_listContext):
        pass

    # Enter a parse tree produced by jacParser#param_list.
    def enterParam_list(self, ctx: jacParser.Param_listContext):
        pass

    # Exit a parse tree produced by jacParser#param_list.
    def exitParam_list(self, ctx: jacParser.Param_listContext):
        pass

    # Enter a parse tree produced by jacParser#expr_list.
    def enterExpr_list(self, ctx: jacParser.Expr_listContext):
        pass

    # Exit a parse tree produced by jacParser#expr_list.
    def exitExpr_list(self, ctx: jacParser.Expr_listContext):
        pass

    # Enter a parse tree produced by jacParser#kw_expr_list.
    def enterKw_expr_list(self, ctx: jacParser.Kw_expr_listContext):
        pass

    # Exit a parse tree produced by jacParser#kw_expr_list.
    def exitKw_expr_list(self, ctx: jacParser.Kw_expr_listContext):
        pass

    # Enter a parse tree produced by jacParser#code_block.
    def enterCode_block(self, ctx: jacParser.Code_blockContext):
        pass

    # Exit a parse tree produced by jacParser#code_block.
    def exitCode_block(self, ctx: jacParser.Code_blockContext):
        pass

    # Enter a parse tree produced by jacParser#node_ctx_block.
    def enterNode_ctx_block(self, ctx: jacParser.Node_ctx_blockContext):
        pass

    # Exit a parse tree produced by jacParser#node_ctx_block.
    def exitNode_ctx_block(self, ctx: jacParser.Node_ctx_blockContext):
        pass

    # Enter a parse tree produced by jacParser#statement.
    def enterStatement(self, ctx: jacParser.StatementContext):
        pass

    # Exit a parse tree produced by jacParser#statement.
    def exitStatement(self, ctx: jacParser.StatementContext):
        pass

    # Enter a parse tree produced by jacParser#if_stmt.
    def enterIf_stmt(self, ctx: jacParser.If_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#if_stmt.
    def exitIf_stmt(self, ctx: jacParser.If_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#try_stmt.
    def enterTry_stmt(self, ctx: jacParser.Try_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#try_stmt.
    def exitTry_stmt(self, ctx: jacParser.Try_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#else_from_try.
    def enterElse_from_try(self, ctx: jacParser.Else_from_tryContext):
        pass

    # Exit a parse tree produced by jacParser#else_from_try.
    def exitElse_from_try(self, ctx: jacParser.Else_from_tryContext):
        pass

    # Enter a parse tree produced by jacParser#elif_stmt.
    def enterElif_stmt(self, ctx: jacParser.Elif_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#elif_stmt.
    def exitElif_stmt(self, ctx: jacParser.Elif_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#else_stmt.
    def enterElse_stmt(self, ctx: jacParser.Else_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#else_stmt.
    def exitElse_stmt(self, ctx: jacParser.Else_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#for_stmt.
    def enterFor_stmt(self, ctx: jacParser.For_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#for_stmt.
    def exitFor_stmt(self, ctx: jacParser.For_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#while_stmt.
    def enterWhile_stmt(self, ctx: jacParser.While_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#while_stmt.
    def exitWhile_stmt(self, ctx: jacParser.While_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#ctrl_stmt.
    def enterCtrl_stmt(self, ctx: jacParser.Ctrl_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#ctrl_stmt.
    def exitCtrl_stmt(self, ctx: jacParser.Ctrl_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#assert_stmt.
    def enterAssert_stmt(self, ctx: jacParser.Assert_stmtContext):
        pass

    # Exit a parse tree produced by jacParser#assert_stmt.
    def exitAssert_stmt(self, ctx: jacParser.Assert_stmtContext):
        pass

    # Enter a parse tree produced by jacParser#destroy_action.
    def enterDestroy_action(self, ctx: jacParser.Destroy_actionContext):
        pass

    # Exit a parse tree produced by jacParser#destroy_action.
    def exitDestroy_action(self, ctx: jacParser.Destroy_actionContext):
        pass

    # Enter a parse tree produced by jacParser#report_action.
    def enterReport_action(self, ctx: jacParser.Report_actionContext):
        pass

    # Exit a parse tree produced by jacParser#report_action.
    def exitReport_action(self, ctx: jacParser.Report_actionContext):
        pass

    # Enter a parse tree produced by jacParser#walker_action.
    def enterWalker_action(self, ctx: jacParser.Walker_actionContext):
        pass

    # Exit a parse tree produced by jacParser#walker_action.
    def exitWalker_action(self, ctx: jacParser.Walker_actionContext):
        pass

    # Enter a parse tree produced by jacParser#ignore_action.
    def enterIgnore_action(self, ctx: jacParser.Ignore_actionContext):
        pass

    # Exit a parse tree produced by jacParser#ignore_action.
    def exitIgnore_action(self, ctx: jacParser.Ignore_actionContext):
        pass

    # Enter a parse tree produced by jacParser#take_action.
    def enterTake_action(self, ctx: jacParser.Take_actionContext):
        pass

    # Exit a parse tree produced by jacParser#take_action.
    def exitTake_action(self, ctx: jacParser.Take_actionContext):
        pass

    # Enter a parse tree produced by jacParser#disengage_action.
    def enterDisengage_action(self, ctx: jacParser.Disengage_actionContext):
        pass

    # Exit a parse tree produced by jacParser#disengage_action.
    def exitDisengage_action(self, ctx: jacParser.Disengage_actionContext):
        pass

    # Enter a parse tree produced by jacParser#yield_action.
    def enterYield_action(self, ctx: jacParser.Yield_actionContext):
        pass

    # Exit a parse tree produced by jacParser#yield_action.
    def exitYield_action(self, ctx: jacParser.Yield_actionContext):
        pass

    # Enter a parse tree produced by jacParser#expression.
    def enterExpression(self, ctx: jacParser.ExpressionContext):
        pass

    # Exit a parse tree produced by jacParser#expression.
    def exitExpression(self, ctx: jacParser.ExpressionContext):
        pass

    # Enter a parse tree produced by jacParser#assignment.
    def enterAssignment(self, ctx: jacParser.AssignmentContext):
        pass

    # Exit a parse tree produced by jacParser#assignment.
    def exitAssignment(self, ctx: jacParser.AssignmentContext):
        pass

    # Enter a parse tree produced by jacParser#copy_assign.
    def enterCopy_assign(self, ctx: jacParser.Copy_assignContext):
        pass

    # Exit a parse tree produced by jacParser#copy_assign.
    def exitCopy_assign(self, ctx: jacParser.Copy_assignContext):
        pass

    # Enter a parse tree produced by jacParser#inc_assign.
    def enterInc_assign(self, ctx: jacParser.Inc_assignContext):
        pass

    # Exit a parse tree produced by jacParser#inc_assign.
    def exitInc_assign(self, ctx: jacParser.Inc_assignContext):
        pass

    # Enter a parse tree produced by jacParser#connect.
    def enterConnect(self, ctx: jacParser.ConnectContext):
        pass

    # Exit a parse tree produced by jacParser#connect.
    def exitConnect(self, ctx: jacParser.ConnectContext):
        pass

    # Enter a parse tree produced by jacParser#logical.
    def enterLogical(self, ctx: jacParser.LogicalContext):
        pass

    # Exit a parse tree produced by jacParser#logical.
    def exitLogical(self, ctx: jacParser.LogicalContext):
        pass

    # Enter a parse tree produced by jacParser#compare.
    def enterCompare(self, ctx: jacParser.CompareContext):
        pass

    # Exit a parse tree produced by jacParser#compare.
    def exitCompare(self, ctx: jacParser.CompareContext):
        pass

    # Enter a parse tree produced by jacParser#cmp_op.
    def enterCmp_op(self, ctx: jacParser.Cmp_opContext):
        pass

    # Exit a parse tree produced by jacParser#cmp_op.
    def exitCmp_op(self, ctx: jacParser.Cmp_opContext):
        pass

    # Enter a parse tree produced by jacParser#nin.
    def enterNin(self, ctx: jacParser.NinContext):
        pass

    # Exit a parse tree produced by jacParser#nin.
    def exitNin(self, ctx: jacParser.NinContext):
        pass

    # Enter a parse tree produced by jacParser#arithmetic.
    def enterArithmetic(self, ctx: jacParser.ArithmeticContext):
        pass

    # Exit a parse tree produced by jacParser#arithmetic.
    def exitArithmetic(self, ctx: jacParser.ArithmeticContext):
        pass

    # Enter a parse tree produced by jacParser#term.
    def enterTerm(self, ctx: jacParser.TermContext):
        pass

    # Exit a parse tree produced by jacParser#term.
    def exitTerm(self, ctx: jacParser.TermContext):
        pass

    # Enter a parse tree produced by jacParser#factor.
    def enterFactor(self, ctx: jacParser.FactorContext):
        pass

    # Exit a parse tree produced by jacParser#factor.
    def exitFactor(self, ctx: jacParser.FactorContext):
        pass

    # Enter a parse tree produced by jacParser#power.
    def enterPower(self, ctx: jacParser.PowerContext):
        pass

    # Exit a parse tree produced by jacParser#power.
    def exitPower(self, ctx: jacParser.PowerContext):
        pass

    # Enter a parse tree produced by jacParser#global_ref.
    def enterGlobal_ref(self, ctx: jacParser.Global_refContext):
        pass

    # Exit a parse tree produced by jacParser#global_ref.
    def exitGlobal_ref(self, ctx: jacParser.Global_refContext):
        pass

    # Enter a parse tree produced by jacParser#atom.
    def enterAtom(self, ctx: jacParser.AtomContext):
        pass

    # Exit a parse tree produced by jacParser#atom.
    def exitAtom(self, ctx: jacParser.AtomContext):
        pass

    # Enter a parse tree produced by jacParser#atom_trailer.
    def enterAtom_trailer(self, ctx: jacParser.Atom_trailerContext):
        pass

    # Exit a parse tree produced by jacParser#atom_trailer.
    def exitAtom_trailer(self, ctx: jacParser.Atom_trailerContext):
        pass

    # Enter a parse tree produced by jacParser#ability_call.
    def enterAbility_call(self, ctx: jacParser.Ability_callContext):
        pass

    # Exit a parse tree produced by jacParser#ability_call.
    def exitAbility_call(self, ctx: jacParser.Ability_callContext):
        pass

    # Enter a parse tree produced by jacParser#ability_op.
    def enterAbility_op(self, ctx: jacParser.Ability_opContext):
        pass

    # Exit a parse tree produced by jacParser#ability_op.
    def exitAbility_op(self, ctx: jacParser.Ability_opContext):
        pass

    # Enter a parse tree produced by jacParser#ref.
    def enterRef(self, ctx: jacParser.RefContext):
        pass

    # Exit a parse tree produced by jacParser#ref.
    def exitRef(self, ctx: jacParser.RefContext):
        pass

    # Enter a parse tree produced by jacParser#deref.
    def enterDeref(self, ctx: jacParser.DerefContext):
        pass

    # Exit a parse tree produced by jacParser#deref.
    def exitDeref(self, ctx: jacParser.DerefContext):
        pass

    # Enter a parse tree produced by jacParser#built_in.
    def enterBuilt_in(self, ctx: jacParser.Built_inContext):
        pass

    # Exit a parse tree produced by jacParser#built_in.
    def exitBuilt_in(self, ctx: jacParser.Built_inContext):
        pass

    # Enter a parse tree produced by jacParser#cast_built_in.
    def enterCast_built_in(self, ctx: jacParser.Cast_built_inContext):
        pass

    # Exit a parse tree produced by jacParser#cast_built_in.
    def exitCast_built_in(self, ctx: jacParser.Cast_built_inContext):
        pass

    # Enter a parse tree produced by jacParser#obj_built_in.
    def enterObj_built_in(self, ctx: jacParser.Obj_built_inContext):
        pass

    # Exit a parse tree produced by jacParser#obj_built_in.
    def exitObj_built_in(self, ctx: jacParser.Obj_built_inContext):
        pass

    # Enter a parse tree produced by jacParser#dict_built_in.
    def enterDict_built_in(self, ctx: jacParser.Dict_built_inContext):
        pass

    # Exit a parse tree produced by jacParser#dict_built_in.
    def exitDict_built_in(self, ctx: jacParser.Dict_built_inContext):
        pass

    # Enter a parse tree produced by jacParser#list_built_in.
    def enterList_built_in(self, ctx: jacParser.List_built_inContext):
        pass

    # Exit a parse tree produced by jacParser#list_built_in.
    def exitList_built_in(self, ctx: jacParser.List_built_inContext):
        pass

    # Enter a parse tree produced by jacParser#string_built_in.
    def enterString_built_in(self, ctx: jacParser.String_built_inContext):
        pass

    # Exit a parse tree produced by jacParser#string_built_in.
    def exitString_built_in(self, ctx: jacParser.String_built_inContext):
        pass

    # Enter a parse tree produced by jacParser#node_edge_ref.
    def enterNode_edge_ref(self, ctx: jacParser.Node_edge_refContext):
        pass

    # Exit a parse tree produced by jacParser#node_edge_ref.
    def exitNode_edge_ref(self, ctx: jacParser.Node_edge_refContext):
        pass

    # Enter a parse tree produced by jacParser#node_ref.
    def enterNode_ref(self, ctx: jacParser.Node_refContext):
        pass

    # Exit a parse tree produced by jacParser#node_ref.
    def exitNode_ref(self, ctx: jacParser.Node_refContext):
        pass

    # Enter a parse tree produced by jacParser#walker_ref.
    def enterWalker_ref(self, ctx: jacParser.Walker_refContext):
        pass

    # Exit a parse tree produced by jacParser#walker_ref.
    def exitWalker_ref(self, ctx: jacParser.Walker_refContext):
        pass

    # Enter a parse tree produced by jacParser#graph_ref.
    def enterGraph_ref(self, ctx: jacParser.Graph_refContext):
        pass

    # Exit a parse tree produced by jacParser#graph_ref.
    def exitGraph_ref(self, ctx: jacParser.Graph_refContext):
        pass

    # Enter a parse tree produced by jacParser#type_ref.
    def enterType_ref(self, ctx: jacParser.Type_refContext):
        pass

    # Exit a parse tree produced by jacParser#type_ref.
    def exitType_ref(self, ctx: jacParser.Type_refContext):
        pass

    # Enter a parse tree produced by jacParser#edge_ref.
    def enterEdge_ref(self, ctx: jacParser.Edge_refContext):
        pass

    # Exit a parse tree produced by jacParser#edge_ref.
    def exitEdge_ref(self, ctx: jacParser.Edge_refContext):
        pass

    # Enter a parse tree produced by jacParser#edge_to.
    def enterEdge_to(self, ctx: jacParser.Edge_toContext):
        pass

    # Exit a parse tree produced by jacParser#edge_to.
    def exitEdge_to(self, ctx: jacParser.Edge_toContext):
        pass

    # Enter a parse tree produced by jacParser#edge_from.
    def enterEdge_from(self, ctx: jacParser.Edge_fromContext):
        pass

    # Exit a parse tree produced by jacParser#edge_from.
    def exitEdge_from(self, ctx: jacParser.Edge_fromContext):
        pass

    # Enter a parse tree produced by jacParser#edge_any.
    def enterEdge_any(self, ctx: jacParser.Edge_anyContext):
        pass

    # Exit a parse tree produced by jacParser#edge_any.
    def exitEdge_any(self, ctx: jacParser.Edge_anyContext):
        pass

    # Enter a parse tree produced by jacParser#connect_op.
    def enterConnect_op(self, ctx: jacParser.Connect_opContext):
        pass

    # Exit a parse tree produced by jacParser#connect_op.
    def exitConnect_op(self, ctx: jacParser.Connect_opContext):
        pass

    # Enter a parse tree produced by jacParser#connect_to.
    def enterConnect_to(self, ctx: jacParser.Connect_toContext):
        pass

    # Exit a parse tree produced by jacParser#connect_to.
    def exitConnect_to(self, ctx: jacParser.Connect_toContext):
        pass

    # Enter a parse tree produced by jacParser#connect_from.
    def enterConnect_from(self, ctx: jacParser.Connect_fromContext):
        pass

    # Exit a parse tree produced by jacParser#connect_from.
    def exitConnect_from(self, ctx: jacParser.Connect_fromContext):
        pass

    # Enter a parse tree produced by jacParser#connect_any.
    def enterConnect_any(self, ctx: jacParser.Connect_anyContext):
        pass

    # Exit a parse tree produced by jacParser#connect_any.
    def exitConnect_any(self, ctx: jacParser.Connect_anyContext):
        pass

    # Enter a parse tree produced by jacParser#list_val.
    def enterList_val(self, ctx: jacParser.List_valContext):
        pass

    # Exit a parse tree produced by jacParser#list_val.
    def exitList_val(self, ctx: jacParser.List_valContext):
        pass

    # Enter a parse tree produced by jacParser#index_slice.
    def enterIndex_slice(self, ctx: jacParser.Index_sliceContext):
        pass

    # Exit a parse tree produced by jacParser#index_slice.
    def exitIndex_slice(self, ctx: jacParser.Index_sliceContext):
        pass

    # Enter a parse tree produced by jacParser#dict_val.
    def enterDict_val(self, ctx: jacParser.Dict_valContext):
        pass

    # Exit a parse tree produced by jacParser#dict_val.
    def exitDict_val(self, ctx: jacParser.Dict_valContext):
        pass

    # Enter a parse tree produced by jacParser#kv_pair.
    def enterKv_pair(self, ctx: jacParser.Kv_pairContext):
        pass

    # Exit a parse tree produced by jacParser#kv_pair.
    def exitKv_pair(self, ctx: jacParser.Kv_pairContext):
        pass

    # Enter a parse tree produced by jacParser#spawn.
    def enterSpawn(self, ctx: jacParser.SpawnContext):
        pass

    # Exit a parse tree produced by jacParser#spawn.
    def exitSpawn(self, ctx: jacParser.SpawnContext):
        pass

    # Enter a parse tree produced by jacParser#spawn_object.
    def enterSpawn_object(self, ctx: jacParser.Spawn_objectContext):
        pass

    # Exit a parse tree produced by jacParser#spawn_object.
    def exitSpawn_object(self, ctx: jacParser.Spawn_objectContext):
        pass

    # Enter a parse tree produced by jacParser#spawn_edge.
    def enterSpawn_edge(self, ctx: jacParser.Spawn_edgeContext):
        pass

    # Exit a parse tree produced by jacParser#spawn_edge.
    def exitSpawn_edge(self, ctx: jacParser.Spawn_edgeContext):
        pass

    # Enter a parse tree produced by jacParser#node_spawn.
    def enterNode_spawn(self, ctx: jacParser.Node_spawnContext):
        pass

    # Exit a parse tree produced by jacParser#node_spawn.
    def exitNode_spawn(self, ctx: jacParser.Node_spawnContext):
        pass

    # Enter a parse tree produced by jacParser#graph_spawn.
    def enterGraph_spawn(self, ctx: jacParser.Graph_spawnContext):
        pass

    # Exit a parse tree produced by jacParser#graph_spawn.
    def exitGraph_spawn(self, ctx: jacParser.Graph_spawnContext):
        pass

    # Enter a parse tree produced by jacParser#walker_spawn.
    def enterWalker_spawn(self, ctx: jacParser.Walker_spawnContext):
        pass

    # Exit a parse tree produced by jacParser#walker_spawn.
    def exitWalker_spawn(self, ctx: jacParser.Walker_spawnContext):
        pass

    # Enter a parse tree produced by jacParser#type_spawn.
    def enterType_spawn(self, ctx: jacParser.Type_spawnContext):
        pass

    # Exit a parse tree produced by jacParser#type_spawn.
    def exitType_spawn(self, ctx: jacParser.Type_spawnContext):
        pass

    # Enter a parse tree produced by jacParser#spawn_ctx.
    def enterSpawn_ctx(self, ctx: jacParser.Spawn_ctxContext):
        pass

    # Exit a parse tree produced by jacParser#spawn_ctx.
    def exitSpawn_ctx(self, ctx: jacParser.Spawn_ctxContext):
        pass

    # Enter a parse tree produced by jacParser#filter_ctx.
    def enterFilter_ctx(self, ctx: jacParser.Filter_ctxContext):
        pass

    # Exit a parse tree produced by jacParser#filter_ctx.
    def exitFilter_ctx(self, ctx: jacParser.Filter_ctxContext):
        pass

    # Enter a parse tree produced by jacParser#spawn_assign.
    def enterSpawn_assign(self, ctx: jacParser.Spawn_assignContext):
        pass

    # Exit a parse tree produced by jacParser#spawn_assign.
    def exitSpawn_assign(self, ctx: jacParser.Spawn_assignContext):
        pass

    # Enter a parse tree produced by jacParser#filter_compare.
    def enterFilter_compare(self, ctx: jacParser.Filter_compareContext):
        pass

    # Exit a parse tree produced by jacParser#filter_compare.
    def exitFilter_compare(self, ctx: jacParser.Filter_compareContext):
        pass

    # Enter a parse tree produced by jacParser#any_type.
    def enterAny_type(self, ctx: jacParser.Any_typeContext):
        pass

    # Exit a parse tree produced by jacParser#any_type.
    def exitAny_type(self, ctx: jacParser.Any_typeContext):
        pass

    # Enter a parse tree produced by jacParser#multistring.
    def enterMultistring(self, ctx: jacParser.MultistringContext):
        pass

    # Exit a parse tree produced by jacParser#multistring.
    def exitMultistring(self, ctx: jacParser.MultistringContext):
        pass


del jacParser
