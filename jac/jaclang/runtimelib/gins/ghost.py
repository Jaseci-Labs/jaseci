"""The Shell Ghost code for gins
"""

import os
import threading
import time
import logging

from jaclang.runtimelib.gins.model import Gemini
from jaclang.runtimelib.gins.tracer import CFGTracker, CfgDeque


# Helper class to maintain a fixed deque size


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

        self.model = Gemini()

        self.deque_lock = threading.Lock()
        self.__cfg_deque_dict = dict()
        self.__cfg_deque_size = 10

        self.logger = logging.getLogger()
        if self.logger.hasHandlers():
          self.logger.handlers.clear()
        logging.basicConfig(
        level=logging.INFO,             # Set the log level
        format='%(asctime)s - %(message)s', # Set the log message format
        datefmt='%Y-%m-%d %H:%M:%S',    # Set the timestamp format
          handlers=[
              logging.FileHandler("test.txt", mode='a'),  # Log to a file in append mode
          ]
        )
        

    def set_cfgs(self, cfgs):
        self.cfg_cv.acquire()
        self.cfgs = cfgs
        self.cfg_cv.notify()
        self.cfg_cv.release()

    def update_cfg_deque(self, cfg, module):
        self.deque_lock.acquire()
        if module not in self.__cfg_deque_dict:
          self.__cfg_deque_dict[module] = CfgDeque(self.__cfg_deque_size)
        self.__cfg_deque_dict[module].add_cfg(cfg)
        self.deque_lock.release()

    def get_cfg_deque_repr(self):
        return self.__cfg_deque.display_cfgs()

    def start_ghost(self):
        self.__ghost_thread = threading.Thread(target=self.worker)
        self.__ghost_thread.start()

    def set_finished(self, exception: Exception = None):
        self.finished_exception_lock.acquire()
        self.exception = exception
        self.finished = True
        self.finished_exception_lock.release()

    def prompt_direct(self):
      script = """
      import:py from math { exp }
      import:py from time { sleep }
      # Data structure representing system configuration
      glob system_config: Dict[str, Union[int, str, float]] = {
          'base_load': 1000,    # Base power load in watts
          'min_duration': 10,   # Minimum valid duration in minutes
          'mode': 'active',
          'time_step': 0,       # Track progression of simulation
          'reference_delta': 200 # Reference power delta for normalization
      };

      # Function to generate declining power readings
      with entry {
          # Create gradually converging power readings
          base: float = system_config['base_load'];
          power_readings: list[float] = [];
          time_periods: list[int] = [];
          reference_power: float = base + 200;# Reference power for normalization

          # Generate 200 readings that gradually approach base_load
          for i in range(200) {
              # Power gradually approaches base_load (1000W)
              delta: float = 200.0 * exp(-0.5 * i);# Slower decay for better visualization
              current_power: float = base + delta;
              power_readings.append(current_power);

              # Time periods increase linearly
              time_periods.append(15 + i * 2);
          }

          # Initialize results storage

          efficiency_metrics: list = [];
          total_operational_time: int = 0;

          # Process each power reading with different execution paths
          for (idx, current_power) in enumerate(power_readings) {
              if system_config['mode'] != 'active' {
                  continue;
              }

              duration: int = time_periods[idx];
              if duration < system_config['min_duration'] {
                  continue;
              }

              # Track simulation progression

              system_config['time_step'] += 1;

              power_delta: float = current_power - system_config['base_load'];

              # Introduce different execution paths based on time_step
              if system_config['time_step'] > 50 {
                  diminishing_reference: float = power_delta * 2;  # Reference point approaches zero with power_delta
                  power_utilization: float = power_delta / diminishing_reference;  # Approaches 0.5, then unstable
              } else {
                  # Original calculation path for first 10 steps
                  power_utilization: float = power_delta / system_config['reference_delta'];
              }
              period_efficiency: float = power_utilization * (duration / max(time_periods)) * 100;

              efficiency_metrics.append(period_efficiency);
              total_operational_time += duration;

              # Print current state
              print(
                  f"Step {system_config['time_step']}: Power={current_power}W, " + f"Delta from base={current_power - system_config['base_load']}W"
              );
          }

          # Calculate final metrics if no error occurred

          average_efficiency: float = sum(efficiency_metrics) / len(efficiency_metrics) if efficiency_metrics else 0;
          operational_hours: float = total_operational_time / 60;
          print(
              f"System Analysis Complete - Efficiency: {average_efficiency}%"
          );

      }

      """
      prompt = f"""
      I have the following script:
      {script}

      Can you identity bottlneck optimizations or where the code can error out?"
      Reason about the program using the provided information, reason about the program itself and what improvements could be made.
      """

      response = self.model.generate(prompt)

      print("\nGin Analysis(With static info):\n", response)

    def prompt_llm(self, verbose: bool = False):
        prompt = """I have a program.
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

        prompt = prompt.format(
            cfgs=cfg_string, instructions=ins_string, sem_ir=self.sem_ir.pp()
        )

        if self.variable_values != None:
            prompt += "\nCurrent variable values at the specified bytecode offset:"

            for module, var_map in self.variable_values.items():
                prompt += f"\nModule {module}: Offset: {var_map[0]}, Variables: {str(var_map[1])}"

        self.finished_exception_lock.acquire()

        if self.exception:
            prompt += f"\nException: {self.exception}"

        self.finished_exception_lock.release()

        # prompt += "\nCan you identity bottlneck optimizations or where the code can error out?"
        # prompt += "\n(Reason about the program using cfg, semantic and type information. Instead of saying what BB could be improved, reason about the program itself and what improvements could be made.)"
        # prompt += "\n If variable values are available, reason about at what point did a variable cause an issue"
        prompt += "\n Please use the following information fill in predicted_edges[freq] for each BB edge with something completely random"
        if verbose:
            print(prompt)

        response = self.model.generate(prompt)

        print("\nGin Analysis:\n", response)
        return response

    def prompt_llm_with_history(self, verbose: bool = False):
        prompt = """I have a program.
        Up to last {history_size} CFGs recorded:
        {cfgs},
        Instructions per basic block:
        {instructions}
        Semantic and Type information from source code:
        {sem_ir}"""

        cfg_string = ""
        ins_string = ""
        for module, cfg in self.cfgs.items():
            cfg_history = "None at this time"
            if module in self.__cfg_deque_dict:
              cfg_history = self.__cfg_deque_dict[module].get_cfg_repr()
            cfg_string += f"Module: {module}\n{cfg_history}"
            ins_string += f"Module: {module}\n{cfg.display_instructions()}"

        prompt = prompt.format(
            history_size=self.__cfg_deque_size,
            cfgs=cfg_string, 
            instructions=ins_string, 
            sem_ir=self.sem_ir.pp()
        )

        if self.variable_values != None:
            prompt += "\nCurrent variable values at the specified bytecode offset:"

            for module, var_map in self.variable_values.items():
                prompt += f"\nModule {module}: Offset: {var_map[0]}, Variables: {str(var_map[1])}"

        self.finished_exception_lock.acquire()

        if self.exception:
            prompt += f"\nException: {self.exception}"

        self.finished_exception_lock.release()

        prompt += "\nCan you identity bottlneck optimizations or where the code can error out?"
        prompt += "\n(Reason about the program using cfg history, semantic and type information. Users will not have access to BB information, so try to reason about the logic and frequencies of blocks instead.)"
        prompt += "\n Additionally, look for any cases where the hot path of the code appears to change at some point in the program"
        prompt += "\n If variable values are available, can you provide tracing information to help find the root cause of any issues?"

        if verbose:
            print(prompt)

        response = self.model.generate(prompt)


        return response
    def prompt_for_runtime(self, verbose: bool = False):
        prompt = """I have a program.
        Up to last {history_size} CFGs recorded:
        {cfgs},
        Instructions per basic block:
        {instructions}
        Semantic and Type information from source code:
        {sem_ir}"""

        cfg_string = ""
        ins_string = ""
        for module, cfg in self.cfgs.items():
            cfg_history = "None at this time"
            if module in self.__cfg_deque_dict:
              cfg_history = self.__cfg_deque_dict[module].get_cfg_repr()
            cfg_string += f"Module: {module}\n{cfg_history}"
            ins_string += f"Module: {module}\n{cfg.display_instructions()}"

        prompt = prompt.format(
            history_size=self.__cfg_deque_size,
            cfgs=cfg_string, 
            instructions=ins_string, 
            sem_ir=self.sem_ir.pp()
        )

        if self.variable_values != None:
            prompt += "\nCurrent variable values at the specified bytecode offset:"

            for module, var_map in self.variable_values.items():
                prompt += f"\nModule {module}: Offset: {var_map[0]}, Variables: {str(var_map[1])}"

        prompt+="\n given this information, what is the program behavior? Please express this in short bullets"
        response = self.model.generate(prompt)
        return response
    def worker(self):
        # get static cfgs
        self.cfg_cv.acquire()
        if self.cfgs == None:
            print("waiting")
            self.cfg_cv.wait()
        # for module_name, cfg in self.cfgs.items():
        #     print(f"Name: {module_name}")
        self.cfg_cv.release()

        # Once cv has been notifie, self.cfgs is no longer accessed across threads
        current_executing_bbs = {}

        def update_cfg():
            exec_insts = self.tracker.get_exec_inst()

            # don't prompt if there's nothing new
            if exec_insts == {}:
                return

            for module, offset_list in exec_insts.items():
                try:
                    cfg = self.cfgs[module]

                    if (
                        module not in current_executing_bbs
                    ):  # this means start at bb0, set exec count for bb0 to 1
                        current_executing_bbs[module] = 0
                        cfg.block_map.idx_to_block[0].exec_count = 1

                    for offset in offset_list:
                        if (
                            offset
                            not in cfg.block_map.idx_to_block[
                                current_executing_bbs[module]
                            ].bytecode_offsets
                        ):
                            for next_bb in cfg.edges[current_executing_bbs[module]]:
                                if (
                                    offset
                                    in cfg.block_map.idx_to_block[
                                        next_bb
                                    ].bytecode_offsets
                                ):
                                    cfg.edge_counts[
                                        (current_executing_bbs[module], next_bb)
                                    ] += 1
                                    # do some deque op
                                    cfg.block_map.idx_to_block[next_bb].exec_count += 1
                                    current_executing_bbs[module] = next_bb
                                    break
                        assert (
                            offset
                            in cfg.block_map.idx_to_block[
                                current_executing_bbs[module]
                            ].bytecode_offsets
                        )
                except Exception as e:
                    self.set_finished(e)
                    print(e)
                    return

            self.variable_values = self.tracker.get_variable_values()
            self.update_cfg_deque(cfg.get_cfg_repr(), module)
            self.logger.info(cfg.to_json())
            print(f"CURRENT INPUTS: {self.tracker.get_inputs()}")

        self.finished_exception_lock.acquire()
        while not self.finished:
            self.finished_exception_lock.release()

            time.sleep(3)
            print("\nUpdating cfgs")
            update_cfg()
            # self.logger.info(self.prompt_llm())
            # print(f"history size: {len(self.__cfg_deque_dict['hot_path'])}")
            self.finished_exception_lock.acquire()
            # time.sleep(1)

        self.finished_exception_lock.release()

        print("\nUpdating cfgs at the end")
        update_cfg()
        print(self.prompt_for_runtime())
        # print(self.__cfg_deque_dict['hot_path'].get_cfg_repr())
        # self.logger.info(self.prompt_llm())
        
