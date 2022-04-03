"""
Sentinel class for Jaseci

Each sentinel has an id, name, timestamp and it's set of walkers.
"""
from jaseci.element.element import element
from jaseci.utils.utils import logger
from jaseci.utils.id_list import id_list
from jaseci.jac.ir.jac_code import jac_code, jac_ir_to_ast
from jaseci.jac.interpreter.sentinel_interp import sentinel_interp
from jaseci.actor.walker import walker
from jaseci.actor.architype import architype


class sentinel(element, jac_code, sentinel_interp):
    """
    Sentinel class for Jaseci

    is_active is used to signify whether sentinel is ready to run walkers, i.e,
    register_code succeeded
    """

    def __init__(self, *args, **kwargs):
        self.version = None
        self.arch_ids = id_list(self)
        self.walker_ids = id_list(self)
        self.testcases = []
        element.__init__(self, *args, **kwargs)
        jac_code.__init__(self, code_ir=None)
        sentinel_interp.__init__(self)
        self.load_arch_defaults()

    def load_arch_defaults(self):
        self.arch_ids.add_obj(architype(m_id=self._m_id, h=self._h,
                                        name='root', kind='node'))
        self.arch_ids.add_obj(architype(m_id=self._m_id, h=self._h,
                                        name='generic', kind='node'))
        self.arch_ids.add_obj(architype(m_id=self._m_id, h=self._h,
                                        name='generic', kind='edge'))

    def reset(self):
        """Resets state of sentinel and unregister's code"""
        self.arch_ids.destroy_all()
        self.load_arch_defaults()
        self.walker_ids.destroy_all()
        jac_code.reset(self)
        sentinel_interp.reset(self)

    def refresh(self):
        super().refresh()
        self.ir_load()

    def register_code(self, text, dir='./'):
        """
        Registers a program (set of walkers and architypes) written in Jac
        """
        self.reset()
        self.register(text, dir)
        if(self.is_active):
            self.ir_load()
        return self.is_active

    def ir_load(self):
        """
        Load walkers and architypes from IR
        """

        self.run_start(self._jac_ast)

        if(self.runtime_errors):
            logger.error(
                str(f'{self.name}: Runtime problem processing sentinel!')
            )
            self.is_active = False
        elif(not self.walker_ids and not self.arch_ids):
            logger.error(
                str(f'{self.name}: No walkers nor architypes created!')
            )
            self.is_active = False
        return self.is_active

    def register_walker(self, code):
        """Adds a walker based on jac code"""
        tree = self.parse_jac(code, start_rule='walker')
        if(not tree):
            return None
        return self.load_walker(tree)

    def register_architype(self, code):
        """Adds a walker based on jac code"""
        tree = self.parse_jac(code, start_rule='architype')
        if(not tree):
            return None
        return self.load_architype(tree)

    def spawn_walker(self, name, caller=None):
        """
        Spawns a new walker from registered walkers and adds to
        live walkers
        """
        src_walk = self.walker_ids.get_obj_by_name(name)
        if (not src_walk):
            logger.error(
                str(f'{self.name}: Unable to spawn walker {name}!')
            )
            return None
        new_walk = src_walk.duplicate()
        if(caller):
            new_walk.set_master(caller._m_id)
        new_walk._jac_ast = src_walk._jac_ast
        if(new_walk._jac_ast is None):
            new_walk.refresh()
        return new_walk

    def spawn_architype(self, name, kind=None, caller=None):
        """
        Spawns a new architype from registered architypes and adds to
        live walkers
        """
        src_arch = self.arch_ids.get_obj_by_name(name, kind=kind,
                                                 silent=True)
        if (not src_arch):
            return None

        if(caller and caller._m_id != src_arch._m_id):
            new_arch = src_arch.duplicate()
            new_arch.set_master(caller._m_id)
            new_arch._jac_ast = src_arch._jac_ast
            if(new_arch._jac_ast is None):
                new_arch.refresh()
            return new_arch
        else:
            return src_arch

    def run_architype(self, name, kind=None, caller=None):
        """
        Spawn, run, then destroy architype if m_id's are different
        """
        if(caller is None):
            caller = self
        arch = self.spawn_architype(name, kind, caller)
        if(arch is None):
            logger.error(
                str(
                    f'{self.name}: Unable to spawn architype '
                    f'{[name, kind]}!')
            )
            return None
        if(arch.jid in self.arch_ids):
            return arch.run()
        else:
            ret = arch.run()
            arch.destroy()
            return ret

    def check_in_arch_context(self, key_name, object):
        """
        Validates a key is present in currently loaded architype of
        a particular instance (helper for expanding node has variables)
        """
        src_arch = self.run_architype(object.name, kind=object.kind)
        return key_name in src_arch.context

    def run_tests(self, detailed=False, silent=False):
        """
        Testcase schema
        testcase = {'title': kid[1].token_text(),
            'graph_ref': None, 'graph_block': None,
            'walker_ref': None, 'spawn_ctx': None,
            'assert_block': None, 'walker_block': None,
            'passed': None}
        """
        from pprint import pformat
        from time import time
        TY = '\033[33m'
        TG = '\033[32m'
        TR = '\033[31m'
        EC = '\033[m'
        num_failed = 0
        for i in self.testcases:
            destroy_set = []
            title = i['title']
            if(i['graph_ref']):
                gph = self.run_architype(
                    i['graph_ref'], kind='graph', caller=self)
            else:
                gph = architype(m_id=self._m_id, h=self._h,
                                parent_id=self.id,
                                code_ir=jac_ir_to_ast(i['graph_block']))
                destroy_set.append(gph)
                gph = gph.run()
            if(i['walker_ref']):
                wlk = self.spawn_walker(i['walker_ref'], caller=self)
            else:
                wlk = walker(m_id=self._m_id, h=self._h,
                             parent_id=self.id,
                             code_ir=jac_ir_to_ast(i['walker_block']))
                destroy_set.append(wlk)
            wlk.prime(gph)
            if(i['spawn_ctx']):
                self.run_spawn_ctx(jac_ir_to_ast(i['spawn_ctx']), wlk)
            stime = time()
            try:
                if(not silent):
                    print(f"Testing {title}: ", end='')
                wlk.run()
                if(i['assert_block']):
                    wlk._loop_ctrl = None
                    wlk.scope_and_run(jac_ir_to_ast(
                        i['assert_block']), run_func=wlk.run_code_block)
                i['passed'] = True
                if(not silent):
                    print(f"[{TG}PASSED{EC} in {TY}{time()-stime:.2f}s{EC}]")
                if(detailed and not silent):
                    print("REPORT: " + pformat(wlk.report))
            except Exception as e:
                i['passed'] = False
                num_failed += 1
                if(not silent):
                    print(f"[{TR}FAILED{EC} in {TY}{time()-stime:.2f}s{EC}]")
                    print(f"{e}")
            for i in destroy_set:  # FIXME: destroy set not complete
                i.destroy()
        num_tests = len(self.testcases)
        summary = {'tests': num_tests, 'passed': num_tests-num_failed,
                   'failed': num_failed,
                   'success': num_tests and not num_failed}
        if(detailed):
            details = []
            for i in self.testcases:
                details.append({'test': i['title'], 'passed': i['passed']})
            summary['details'] = details
        return summary

    def destroy(self):
        """
        Destroys self from memory and persistent storage
        """
        for i in self.arch_ids.obj_list() + \
                self.walker_ids.obj_list():
            i.destroy()
        super().destroy()
