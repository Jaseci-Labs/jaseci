"""Jac Machine module."""

from __future__ import annotations

import inspect
import marshal
import os
import copy
import time
import sys
import tempfile
import types
import dis
import google.generativeai as genai
import threading
from collections import deque
from contextvars import ContextVar
from typing import Optional, Union

from jaclang.compiler.absyntree import Module
from jaclang.compiler.compile import compile_jac, jac_file_to_pass

from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.semtable import SemRegistry
from jaclang.runtimelib.architype import (
    Architype,
    EdgeArchitype,
    NodeArchitype,
    WalkerArchitype,
)
from jaclang.utils.log import logging
from jaclang.compiler.passes.main.schedules import py_code_gen, type_checker_sched

logger = logging.getLogger(__name__)


JACMACHINE_CONTEXT = ContextVar["JacMachine | None"]("JacMachine")


class JacMachine:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    def __init__(self, base_path: str = "") -> None:
        """Initialize the JacMachine object."""
        self.loaded_modules: dict[str, types.ModuleType] = {}
        if not base_path:
            base_path = os.getcwd()
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path)
            if not os.path.isdir(base_path)
            else os.path.abspath(base_path)
        )
        self.jac_program: Optional[JacProgram] = None
        self.gin: Optional[ShellGhost] = None

        JACMACHINE_CONTEXT.set(self)

    def attach_program(self, jac_program: "JacProgram") -> None:
        """Attach a JacProgram to the machine."""
        self.jac_program = jac_program
    
    def attach_gin(self, jac_gin: "ShellGhost") -> None:
        """Attach a JacProgram to the machine."""
        self.gin = jac_gin
            

    def get_mod_bundle(self) -> Optional[Module]:
        """Retrieve the mod_bundle from the attached JacProgram."""
        if self.jac_program:
            return self.jac_program.mod_bundle
        return None

    def get_bytecode(
        self,
        module_name: str,
        full_target: str,
        caller_dir: str,
        cachable: bool = True,
        reload: bool = False,
    ) -> Optional[types.CodeType]:
        """Retrieve bytecode from the attached JacProgram."""
        if self.jac_program:
            bytecode = self.jac_program.get_bytecode(
                module_name, full_target, caller_dir, cachable, reload=reload
            )
            if self.gin:
                self.gin.start_ghost()
            return bytecode
        return None

    def get_sem_ir(self, mod_sem_ir: SemRegistry | None) -> None:
        """Update semtable on the attached JacProgram."""
        if self.jac_program and mod_sem_ir:
            if self.jac_program.sem_ir:
                self.jac_program.sem_ir.registry.update(mod_sem_ir.registry)
            else:
                self.jac_program.sem_ir = mod_sem_ir

    def load_module(self, module_name: str, module: types.ModuleType) -> None:
        """Load a module into the machine."""
        self.loaded_modules[module_name] = module
        sys.modules[module_name] = module

    def list_modules(self) -> list[str]:
        """List all loaded modules."""
        return list(self.loaded_modules.keys())

    def list_walkers(self, module_name: str) -> list[str]:
        """List all walkers in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            walkers = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, WalkerArchitype):
                    walkers.append(name)
            return walkers
        return []

    def list_nodes(self, module_name: str) -> list[str]:
        """List all nodes in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            nodes = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, NodeArchitype):
                    nodes.append(name)
            return nodes
        return []

    def list_edges(self, module_name: str) -> list[str]:
        """List all edges in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            nodes = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, EdgeArchitype):
                    nodes.append(name)
            return nodes
        return []

    def create_architype_from_source(
        self,
        source_code: str,
        module_name: Optional[str] = None,
        base_path: Optional[str] = None,
        cachable: bool = False,
        keep_temporary_files: bool = False,
    ) -> Optional[types.ModuleType]:
        """Dynamically creates architypes (nodes, walkers, etc.) from Jac source code."""
        from jaclang.runtimelib.importer import JacImporter, ImportPathSpec

        if not base_path:
            base_path = self.base_path or os.getcwd()

        if base_path and not os.path.exists(base_path):
            os.makedirs(base_path)
        if not module_name:
            module_name = f"_dynamic_module_{len(self.loaded_modules)}"
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".jac",
            prefix=module_name + "_",
            dir=base_path,
            delete=False,
        ) as tmp_file:
            tmp_file_path = tmp_file.name
            tmp_file.write(source_code)

        try:
            importer = JacImporter(self)
            tmp_file_basename = os.path.basename(tmp_file_path)
            tmp_module_name, _ = os.path.splitext(tmp_file_basename)

            spec = ImportPathSpec(
                target=tmp_module_name,
                base_path=base_path,
                absorb=False,
                cachable=cachable,
                mdl_alias=None,
                override_name=module_name,
                lng="jac",
                items=None,
            )

            import_result = importer.run_import(spec, reload=False)
            module = import_result.ret_mod

            self.loaded_modules[module_name] = module
            return module
        except Exception as e:
            logger.error(f"Error importing dynamic module '{module_name}': {e}")
            return None
        finally:
            if not keep_temporary_files and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def update_walker(
        self, module_name: str, items: Optional[dict[str, Union[str, Optional[str]]]]
    ) -> tuple[types.ModuleType, ...]:
        """Reimport the module."""
        from .importer import JacImporter, ImportPathSpec

        if module_name in self.loaded_modules:
            try:
                old_module = self.loaded_modules[module_name]
                importer = JacImporter(self)
                spec = ImportPathSpec(
                    target=module_name,
                    base_path=self.base_path,
                    absorb=False,
                    cachable=True,
                    mdl_alias=None,
                    override_name=None,
                    lng="jac",
                    items=items,
                )
                import_result = importer.run_import(spec, reload=True)
                ret_items = []
                if items:
                    for item_name in items:
                        if hasattr(old_module, item_name):
                            new_attr = getattr(import_result.ret_mod, item_name, None)
                            if new_attr:
                                ret_items.append(new_attr)
                                setattr(
                                    old_module,
                                    item_name,
                                    new_attr,
                                )
                return (old_module,) if not items else tuple(ret_items)
            except Exception as e:
                logger.error(f"Failed to update module {module_name}: {e}")
        else:
            logger.warning(f"Module {module_name} not found in loaded modules.")
        return ()

    def spawn_node(
        self,
        node_name: str,
        attributes: Optional[dict] = None,
        module_name: str = "__main__",
    ) -> NodeArchitype:
        """Spawn a node instance of the given node_name with attributes."""
        node_class = self.get_architype(module_name, node_name)
        if isinstance(node_class, type) and issubclass(node_class, NodeArchitype):
            if attributes is None:
                attributes = {}
            node_instance = node_class(**attributes)
            return node_instance
        else:
            raise ValueError(f"Node {node_name} not found.")

    def spawn_walker(
        self,
        walker_name: str,
        attributes: Optional[dict] = None,
        module_name: str = "__main__",
    ) -> WalkerArchitype:
        """Spawn a walker instance of the given walker_name."""
        walker_class = self.get_architype(module_name, walker_name)
        if isinstance(walker_class, type) and issubclass(walker_class, WalkerArchitype):
            if attributes is None:
                attributes = {}
            walker_instance = walker_class(**attributes)
            return walker_instance
        else:
            raise ValueError(f"Walker {walker_name} not found.")

    def get_architype(
        self, module_name: str, architype_name: str
    ) -> Optional[Architype]:
        """Retrieve an architype class from a module."""
        module = self.loaded_modules.get(module_name)
        if module:
            return getattr(module, architype_name, None)
        return None

    @staticmethod
    def get(base_path: str = "") -> "JacMachine":
        """Get current jac machine."""
        if (jac_machine := JACMACHINE_CONTEXT.get(None)) is None:
            jac_machine = JacMachine(base_path)
        return jac_machine

    @staticmethod
    def detach() -> None:
        """Detach current jac machine."""
        JACMACHINE_CONTEXT.set(None)


class JacProgram:
    """Class to hold the mod_bundle bytecode and sem_ir for Jac modules."""

    def __init__(
        self,
        mod_bundle: Optional[Module],
        bytecode: Optional[dict[str, bytes]],
        sem_ir: Optional[SemRegistry],
    ) -> None:
        """Initialize the JacProgram object."""
        self.mod_bundle = mod_bundle
        self.bytecode = bytecode or {}
        self.sem_ir = sem_ir if sem_ir else SemRegistry()

    def get_bytecode(
        self,
        module_name: str,
        full_target: str,
        caller_dir: str,
        cachable: bool = True,
        reload: bool = False,
    ) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if self.mod_bundle and isinstance(self.mod_bundle, Module):
            codeobj = self.mod_bundle.mod_deps[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        gen_dir = os.path.join(caller_dir, Con.JAC_GEN_DIR)
        pyc_file_path = os.path.join(gen_dir, module_name + ".jbc")
        if cachable and os.path.exists(pyc_file_path) and not reload:
            with open(pyc_file_path, "rb") as f:
                return marshal.load(f)

        result = compile_jac(full_target, cache_result=cachable)
        if result.errors_had or not result.ir.gen.py_bytecode:
            for alrt in result.errors_had:
                logger.error(alrt.pretty_print())
            return None
        if result.ir.gen.py_bytecode is not None:
            return marshal.loads(result.ir.gen.py_bytecode)
        else:
            return None


class CFGTracker:
    def __init__(self):
        self.executed_inst_list = deque()
        self.inst_lock = threading.Lock()

    def start_tracking(self):
        """Start tracking branch coverage"""
        frame = sys._getframe()
        frame.f_trace_opcodes = True
        sys.settrace(self.trace_callback)
    def stop_tracking(self):
        """Stop tracking branch coverage"""
        sys.settrace(None)
    
    def get_exec_inst(self):
        ret = []
        
        self.inst_lock.acquire()
        while len(self.executed_inst_list) > 0:
            ret.append(self.executed_inst_list.popleft())
        self.inst_lock.release()
        
        return ret
    
    def trace_callback(self, frame: types.FrameType, event: str, arg: any) -> Optional[types.TraceFunction]:
        # if event == "call":
        frame.f_trace_opcodes = True
        # frame.f_trace_lines = False
    #     def tracefunc(frame, event, arg):
    #         if event == 'call':
    #             frame.f_trace_opcodes = True
    #         elif event == 'opcode':
    #             if frame.f_code.co_code[frame.f_lasti] == dis.opmap['MAKE_FUNCTION']:
    #                 makefunctiontracefunc(frame)
    # return tracefunc
                
        """Trace function to track executed branches"""        
        
        if ".jac" not in code.co_filename:
            return self.trace_callback
        
        if event == 'opcode':
            print(frame.f_lasti)

        if event != 'line':
            return self.trace_callback
        code = frame.f_code
        

        
        # print(frame.f_lineno, frame.f_lasti)
        
        #edge case to handle executing code not within a function
        filename = os.path.basename(code.co_filename)
        module = code.co_name if code.co_name != "<module>" else os.path.splitext(filename)[0]
        
        # bytecode = dis.Bytecode(code)
        # for instr in bytecode:
        #     if instr.starts_line:
        #         print(f"  Offset: {instr.offset}, Op: {instr.opname}, Line: {instr.starts_line}")
        #         pass
        variable_dict = {}
        if '__annotations__' in frame.f_locals:
            for var_name in frame.f_locals['__annotations__']:
                variable_dict[var_name] = frame.f_locals[var_name]
    
        self.inst_lock.acquire()
        self.executed_inst_list.append((module, frame.f_lineno, variable_dict))
        self.inst_lock.release()

        # self.variable_values[code.co_name][frame.f_lineno] = {}

                
        # print(f"{frame.f_lineno}")
        # print(f"Function Name: {code.co_name}") 
        # print(f"Filename: {code.co_filename}") 
        # print(f"First Line Number: {code.co_firstlineno}") 
        # print(f"Argument Count: {code.co_argcount}") 
        # print(f"Constants: {code.co_consts}") 
        # print(f"Local Variables: {code.co_varnames}")

        # if event != 'line':
        #     return self.trace_callback

        # code = frame.f_code
        # if code not in self.cfg_cache:
        #     self.build_cfg(code)

        # # Find current basic block
        # blocks = self.cfg_cache[code]
        # current_offset = frame.f_lasti

        # # Find the block containing this offset
        # current_block = None
        # for block in blocks.values():
        #     if block.offset <= current_offset <= block.offset + sum(inst.size for inst in block.instructions):
        #         current_block = block
        #         break

        # if current_block:
        #     current_block.hits += 1
        #     # Record taken branches
        #     for next_block in current_block.next:
        #         self.coverage_data[code].add(
        #             (current_block.offset, next_block.offset))

        return self.trace_callback

class ShellGhost:
    def __init__(self):
        self.cfgs = None
        self.cfg_cv = threading.Condition()
        self.tracker = CFGTracker()
        
        self.finished_exception_lock = threading.Lock()
        self.exception = None
        self.finished = False

    def set_cfgs(self, cfgs):
        self.cfg_cv.acquire()
        self.cfgs = cfgs
        self.cfg_cv.notify()
        self.cfg_cv.release()

    def start_ghost(self):
        self.__ghost_thread = threading.Thread(target=self.worker)
        self.__ghost_thread.start()

    def set_finished(self, exception: Exception = None):
        self.finished_exception_lock.acquire()
        self.exception = exception
        self.finished = True
        self.finished_exception_lock.release()
    
    def worker(self):
        #this is temporary while developing 
        
        # get static cfgs
        self.cfg_cv.acquire()
        while (self.cfgs == None):
            self.cfg_cv.wait()
        # print(self.cfgs)
        for module_name, cfg in self.cfgs.items():
            print(f"Name: {module_name}\n{cfg.display_instructions()}")
            pass
        self.cfg_cv.release()

        variables_by_line = []
        
        # Once cv has been notifie, self.cfgs is no longer accessed across threads

        current_executing_bb = [0]
        
        def update_cfg():
            exec_inst_list = self.tracker.get_exec_inst()
            
            for module, inst, variables in exec_inst_list:
                cfg = self.cfgs[module]                    
                

                inst_line_no_list = []
                for instruction in cfg.block_map.idx_to_block[current_executing_bb[0]].instructions:
                    pass
                if inst not in cfg.block_map.idx_to_block[current_executing_bb[0]].line_nos:
                    for next in cfg.edges[current_executing_bb[0]]:
                        if inst in cfg.block_map.idx_to_block[next].line_nos:
                            cfg.edge_counts[(current_executing_bb[0], next)] += 1
                            cfg.block_map.idx_to_block[next].exec_count += 1

                            current_executing_bb[0] = next
                            break
                
                # print("current local variable values:" f"Inst #{inst}", variables)
                variables_by_line.append((inst, variables))
                
                    
                # assert(inst in cfg.block_map.idx_to_block[current_executing_bb[0]].line_nos)
                # cfg.block_map.idx_to_block[current_executing_bb[0]].start_inst_variables_map[inst] = variables

        self.finished_exception_lock.acquire()
        while (not self.finished):
            self.finished_exception_lock.release()

            update_cfg()
            
            time.sleep(1)
            self.finished_exception_lock.acquire()
        
        update_cfg()
        # print(self.cfgs)
        # for module_name, cfg in self.cfgs.items():
        #     print(f"Name: {module_name}\n{cfg.display_instructions()}")


        
        #     for func_name, dic in curr_variables.items():
        #         print(func_name)module
                
        #         for lin_no ,v in dic.items():
        #             print("line: ", lin_no)
        #             print(v)

        #     # check the variable values ever 3 seconds
        #     self.finished_exception_lock.release()
        #     time.sleep(0.5)
        #     self.finished_exception_lock.acquire()

        # self.finished_exception_lock.release()
        # print("Getting Current Variable Values")
        # for func_name, dic in self.tracker.get_variable_values().items():
        #     print("name:", func_name)
            
        #     for lin_no ,v in dic.items():
        #         print("line: ", lin_no)
        #         print(v)    
        # # there should be no other thread trying to access finished/exception

        if self.exception:
            print("Exception occured:", self.exception)    
        self.finished_exception_lock.release()
        
        
        # genai.configure(api_key=os.getenv("GEN_AI_KEY"))
        # model = genai.GenerativeModel("gemini-1.5-flash")
        response_dict = {'cfg': self.cfgs, 'instructions': self.cfgs[module_name].display_instructions(), 'list of local variables at sequential line numbers': variables_by_line}
        prompt = []
        for k,v in response_dict.items():
            prompt.append(f"here is my {k}:\n{v}")
        prompt.append("\nCan you identify where the code could have an error?")
        # response = model.generate_content("".join(prompt))

        # print("PROMPT:\n")
        # print("".join(prompt))
        # print("RESPONSE:\n")
        # print(response.text)

        # print(self.cfgs['hot_path'].display_instructions())