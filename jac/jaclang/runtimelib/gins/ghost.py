"""The Shell Ghost code for gins"""
import os
import threading
import time


from jaclang.runtimelib.gins.tracer import CFGTracker
try:
    import google.generativeai as genai
except Exception as e:
    print("google.generativeai module not present. Please install using 'pip install google.generativeai'.")

class ShellGhost:
    def __init__(self):
        self.cfgs = None
        self.cfg_cv = threading.Condition()
        self.tracker = CFGTracker()
        self.sem_ir = None
        
        self.finished_exception_lock = threading.Lock()
        self.exception = None
        self.finished = False
        self.variable_values = None

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")


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
    
    def prompt_llm(self, verbose: bool = False):
        prompt = """I have a program.
CFGS:
{cfgs},
Instructions per basic block:
{instructions}
Semantic and Type information from source code:
{sem_ir}"""
        
        cfg_string = ""
        ins_string = "" 
        for module, cfg in self.cfgs.items():
            cfg_string += f"Module: {module}\n{cfg}" 
            ins_string += f"Module: {module}\n{cfg.display_instructions()}"
        
        prompt = prompt.format(cfgs=cfg_string, instructions=ins_string, sem_ir=self.sem_ir)

        if self.variable_values != None:
            prompt += "\nCurrent variable values at the specified bytecode offset:"
            
            for module, var_map in self.variable_values.items():
                prompt += f"\nModule {module}: Offset: {var_map[0]}, Variables: {str(var_map[1])}"
        
        self.finished_exception_lock.acquire()
        
        if self.exception:
            prompt += f"\nException: {self.exception}"

        self.finished_exception_lock.release()
        
        prompt += "\nCan you identity bottlneck optimizations or where the code can error out?"
        prompt += "\n(Reason about the program using cfg, semantic and type information. Do not include python code fixes or bytecode in response.)"
        
        if verbose:
            print(prompt)
        
        response = self.model.generate_content(prompt)
        
        print(response.text)
    
    def worker(self):

        # get static cfgs
        self.cfg_cv.acquire()
        while (self.cfgs == None):
            self.cfg_cv.wait()
        # print(self.cfgs)
        # for module_name, cfg in self.cfgs.items():
        #     print(f"Name: {module_name}\n{cfg.display_instructions()}")
        self.cfg_cv.release()
        
        # Once cv has been notifie, self.cfgs is no longer accessed across threads

        
        current_executing_bbs = {}   

        def update_cfg():
            exec_insts = self.tracker.get_exec_inst()
            
            # don't prompt if there's nothing new
            if exec_insts == {}: return
            for module, offset_list in exec_insts.items():
                try: 
                    cfg = self.cfgs[module]                    

                    if module not in current_executing_bbs: # this means start at bb0, set exec count for bb0 to 1
                        current_executing_bbs[module] = 0
                        cfg.block_map.idx_to_block[0].exec_count = 1
                    
                    for offset in offset_list:                
                        if offset not in cfg.block_map.idx_to_block[current_executing_bbs[module]].bytecode_offsets:
                            for next in cfg.edges[current_executing_bbs[module]]:
                                if offset in cfg.block_map.idx_to_block[next].bytecode_offsets:
                                    cfg.edge_counts[(current_executing_bbs[module], next)] += 1
                                    cfg.block_map.idx_to_block[next].exec_count += 1

                                    current_executing_bbs[module] = next
                                    break                                    
                        assert(offset in cfg.block_map.idx_to_block[current_executing_bbs[module]].bytecode_offsets)
                except Exception as e:
                    self.set_finished(e)
                    print(e)
                    return

            self.variable_values = self.tracker.get_variable_values()

        self.finished_exception_lock.acquire()
        while (not self.finished):
            self.finished_exception_lock.release()
            
            time.sleep(5)
            print('\nUpdating cfgs')
            update_cfg()
            self.prompt_llm()
            self.finished_exception_lock.acquire()

        self.finished_exception_lock.release()
        
        # print(self.cfgs)
        # self.finished_exception_lock.acquire()
        # if self.exception:
            # print("Exception occured:", self.exception)
        # self.finished_exception_lock.release()
        print('\nUpdating cfgs at the end')
        update_cfg()
        self.prompt_llm()
        
        # response_dict = {'cfg': self.cfgs, 'instructions': self.cfgs[module_name].display_instructions(), 'list of local variables at sequential line numbers': variables_by_line}
        # prompt = []
        # for k,v in response_dict.items():
        #     prompt.append(f"here is my {k}:\n{v}")
        # prompt.append("\nCan you identify where the code could have an error?")
        # response = model.generate_content("".join(prompt))

        # print("PROMPT:\n")
        # print("".join(prompt))
        # print("RESPONSE:\n")
        # print(response.text)

        # print(self.cfgs['hot_path'].display_instructions())