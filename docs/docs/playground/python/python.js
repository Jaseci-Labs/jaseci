
// ----------------------------------------------------------------------------
// Globals
// ----------------------------------------------------------------------------

var pyodide = null;
var breakpoints_buff = [];
var dbg = null;  // The debugger instance.

var sharedInts = null;


const JAC_PATH = "/tmp/main.jac";
const LOG_PATH = "/tmp/logs.log";

// ----------------------------------------------------------------------------
// Message passing protocol
// ----------------------------------------------------------------------------

onmessage = async (event) => {
  const data = event.data;
  switch (data.type) {

    case 'initialize':
      sharedInts = new Int32Array(data.sharedBuffer);

      importScripts("https://cdn.jsdelivr.net/pyodide/v0.27.0/full/pyodide.js");
      logMessage("Loading Pyodide...");
      pyodide = await loadPyodide();
      logMessage("Pyodide loaded.");
      const success = await loadPyodideAndJacLang();
      logMessage(`Pyodide and JacLang loaded: success=${success}`);
      self.postMessage({ type: 'initialized', success: success });
      break;

    case 'setBreakpoints':
      if (dbg) {
        dbg.clear_breakpoints();
        for (const bp of data.breakpoints) {
          dbg.set_breakpoint(bp);
          logMessage(`Breakpoint set at line ${bp}`);
        }
      } else {
        breakpoints_buff = data.breakpoints;
      }
      break;

    case 'startExecution':
      logMessage("Starting execution...");
      await startExecution(data.code);
      logMessage(`Execution finished`);
      self.postMessage({ type: 'execEnd' });
      break;

    default:
      console.error("Unknown message type:", data.type);
  }

};

// ----------------------------------------------------------------------------
// Utility functions
// ----------------------------------------------------------------------------

function logMessage(message) {
  console.log("[PythonThread] " + message);
}


async function readFileAsString(fileName) {
  const response = await fetch("/playground" + fileName);
  return await response.text();
};


async function readFileAsBytes(fileName) {
  const response = await fetch("/playground" + fileName);
  const buffer = await response.arrayBuffer();
  return new Uint8Array(buffer);
}


// ----------------------------------------------------------------------------
// Jaclang Initialization
// ----------------------------------------------------------------------------

async function loadPyodideAndJacLang() {
  try {
    await loadPythonResources(pyodide);
    success = await checkJaclangLoaded(pyodide);

    // Run the debugger module.
    await pyodide.runPythonAsync(
      await readFileAsString("/python/debugger.py")
    );
    return success;

  } catch (error) {
    console.error("Error loading JacLang:", error);
    return false;
  }
}


async function loadPythonResources(pyodide) {
  const data = await readFileAsBytes("/jaclang.zip");
  await pyodide.FS.writeFile("/jaclang.zip", data);
  await pyodide.runPythonAsync(
    await readFileAsString("/python/extract_jaclang.py")
  );
}


async function checkJaclangLoaded(pyodide) {
  try {
    await pyodide.runPythonAsync(`from jaclang.cli.cli import run`);
    console.log("JacLang is available.");
    return true;
  } catch (error) {
    console.error("JacLang is not available:", error);
    return false;
  }
}


// ----------------------------------------------------------------------------
// Execution
// ----------------------------------------------------------------------------


function callbackBreak(dbg, line) {

  logMessage(`before ui: line=$${line}`);
  waitingForUi = true;
  self.postMessage({ type: 'breakHit', line: line });

  continueExecution = false;
  while (!continueExecution) {
    Atomics.wait(sharedInts, 0, 0); // Block until the UI responds.
    sharedInts[0] = 0;  // Reset the shared memory.

    switch (sharedInts[1]) {
      case 1: // Clear breakpoints
        if (dbg) {
          dbg.clear_breakpoints();
          logMessage("Breakpoints cleared.");
        }
        break;

      case 2: // Set breakpoint
        const line = sharedInts[2];
        if (dbg) {
          dbg.set_breakpoint(line);
          logMessage(`Breakpoint set at line ${line}`);
        }
        break;

      case 3: // Continue execution
        dbg.do_continue();
        continueExecution = true;
        break;

      case 4: // Step over
        if (dbg) {
          dbg.do_step_over();
          logMessage("Stepped over.");
        }
        continueExecution = true;
        break;

      case 5: // Step into
        if (dbg) {
          dbg.do_step_into();
          logMessage("Stepped into.");
        }
        continueExecution = true;
        break;

      case 6: // Step out
        if (dbg) {
          dbg.do_step_out();
          logMessage("Stepped out.");
        }
        continueExecution = true;
        break;

      case 7: // Terminat execution
        if (dbg) {
          dbg.do_terminate();
          logMessage("Execution stopped.");
        }
        continueExecution = true;
        break;
    }

  }


  logMessage("after ui");
}


function callbackStdout(output) {
  self.postMessage({ type: 'stdout', output: output });
}


function callbackStderr(output) {
  self.postMessage({ type: 'stderr', output: output });
}


function callbackGraph(graph) {
  self.postMessage({ type: 'jacGraph', graph: graph });
}


async function startExecution(safeCode) {

  pyodide.globals.set('SAFE_CODE', safeCode);
  pyodide.globals.set('JAC_PATH', JAC_PATH);
  pyodide.globals.set('CB_STDOUT', callbackStdout);
  pyodide.globals.set('CB_STDERR', callbackStderr);

  dbg = pyodide.globals.get('Debugger')();
  dbg.cb_break = callbackBreak;
  dbg.cb_graph = callbackGraph;
  pyodide.globals.set('debugger', dbg);

  dbg.clear_breakpoints();
  for (const bp of breakpoints_buff) {
    dbg.set_breakpoint(bp);
    logMessage(`Breakpoint set at line ${bp}`);
  }

  // Run the main script
  logMessage("Execution started.");
  await pyodide.runPythonAsync(
    await readFileAsString("/python/main_playground.py")
  );
  logMessage("Execution finished.");
  dbg = null;

}
