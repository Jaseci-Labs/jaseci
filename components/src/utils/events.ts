import { checkCond } from './conditions';
import { renderComponentTree } from './utils';

export function setUpEvents(host: HTMLElement, events: string) {
  if (events) {
    host.removeAttribute('events');
    const parsedEvents: JaseciComponent['events'] = JSON.parse(events);
    linkEvents(host, parsedEvents);
  }
}

// export function setUpOperations(name: string, operations: any) {
//   operations = JSON.parse(localStorage.getItem(`op-${name}`));
// }

type ParseArgsConfig = { withOriginal?: boolean };

/**
 * Inject the provided args for an action into the defined args of an operation
 */
export function computeOpArgs(operationActionArgs: string[], actionArgs: (string | number)[]) {
  let argValues = {};

  operationActionArgs.map((operationArg, index) => {
    console.log(actionArgs[index]);
    // const matchedArgs = operationArg.match(/arg[(](.*?)[)]/g);
    argValues[`arg(${operationArg})`] = typeof actionArgs[index] === 'string' ? computeVar(actionArgs[index] as string) : actionArgs[index];
  });

  return argValues;
}

/**
 *  Determines the value of a variable
 */
export function computeVar(arg: string, result?: any) {
  let updatedArg = arg;
  const vars = arg.match(/var[(](.*?)[)]/g);

  if (typeof arg === 'string' && vars?.length > 0) {
    vars.map(variableRef => {
      let component: Element;
      let variableValue: any;
      const variableName = variableRef.split('var(')?.[1]?.split(')')[0];
      const [componentName, componentProperty] = variableName.split('.');
      if (componentName !== 'result') {
        component = getComponentByName(componentName);
        variableValue = component[componentProperty];
      }
      if (componentName === 'result') {
        variableValue = result;
      }
      updatedArg = updatedArg.replaceAll(variableRef, variableValue);
    });

    return updatedArg;
  }

  return arg;
}

// evaluates the value of an arg specified as a variable where the variable is a property name
function parseArgs(args: unknown[] = [], config?: ParseArgsConfig, result?: any) {
  const originalArgsWithNewArgs = {};
  let newArgs = [...args];

  args.map((arg, index) => {
    if (typeof arg === 'string') {
      const variableValue = computeVar(arg, result);
      newArgs = [...newArgs.slice(0, index), variableValue, ...newArgs.slice(index + 1)];
      originalArgsWithNewArgs[arg] = variableValue;
    }
  });

  return config?.withOriginal ? originalArgsWithNewArgs : newArgs;
}

function getComponentByName(componentName: string) {
  return window.document.querySelector('jsc-app').shadowRoot.querySelector(`[name='${componentName}']`);
}

/**
 * Evaluates the correct action to be attached to the event handler of the dom element
 */
function runAction(action: JaseciAction, result?: any) {
  const actionName = action.fn;
  const actionArgs = action.args;
  const parsedActionArgs = parseArgs(action.args, {}, result);

  checkCond(action.cond || []).run(async () => {
    switch (actionName) {
      case 'update':
        // use actions.args because we need a ref instead of the value for the first arg of update
        const componentPropertyRef = actionArgs[0];
        if (typeof componentPropertyRef !== 'string') throw new Error('Component property reference must be a string');
        const [componentName, propertyName] = componentPropertyRef.split('.');
        const component = getComponentByName(componentName);
        const value = parsedActionArgs[1];
        update(component, propertyName, value);
        action?.onCompleted && runAction(action?.onCompleted);
        break;
      case 'add':
        const val1 = parsedActionArgs[0];
        const val2 = parsedActionArgs[1];
        const result = Number(val1) + Number(val2);
        action?.onCompleted && runAction(action?.onCompleted, result);
        break;
      case 'append':
        const targetComponentName = actionArgs[0];
        if (typeof targetComponentName !== 'string') throw new Error('Component name must be a string');
        const targetComponent = getComponentByName(targetComponentName);
        let newComponent = actionArgs[1];
        let newComponentString = typeof newComponent === 'string' ? newComponent : JSON.stringify(newComponent);

        append(targetComponent, newComponentString);

        action?.onCompleted && runAction(action?.onCompleted);
        break;
      case 'runOperation':
        const operation = action?.operation;
        const [opComponentName, operationName] = operation.split('.');
        // get the operation component
        const opComponent = getComponentByName(opComponentName);
        // get the structure of the operation
        const componentOperations = (opComponent as HTMLElement & { operations: Record<string, JaseciOperation> }).operations;
        const operationStructure = componentOperations[operationName];

        // get the defined args of the operation
        const operationArgs = operationStructure.args;

        // get and compute args of the current action
        let currentActionArgs = parsedActionArgs as [];

        // map the args of the operation to the computed action args
        const operationArgsMap = {};

        currentActionArgs.forEach((actionArgValue, index) => {
          operationArgsMap[`arg(${operationArgs[index]})`] = actionArgValue;
        });

        // replace args with computed values
        let updatedOperationStructure = { ...operationStructure };
        let operationStructureActionsString = JSON.stringify(operationStructure.run);

        console.log({ operationArgsMap });

        Object.keys(operationArgsMap).forEach(arg => {
          console.log({ arg });
          operationStructureActionsString = operationStructureActionsString.replaceAll(arg, operationArgsMap[arg]);
          console.log(operationStructureActionsString);
        });

        updatedOperationStructure['run'] = JSON.parse(operationStructureActionsString);
        // run the operation
        updatedOperationStructure['run'].map(action => runAction(action as any));
        console.log({ updatedOperationStructure });

        break;

      case 'callEndpoint':
        const method = parsedActionArgs[0];
        const body = typeof parsedActionArgs[1] === 'string' ? parsedActionArgs[1] : JSON.stringify(parsedActionArgs[1]);
        console.log({ method, body });
        const actions = await fetch(action?.endpoint, { method, body, headers: { 'Content-Type': 'application/json' } }).then(res => res.json());
        if (!actions) throw new Error('No action returned from endpoint.');
        Array.isArray(actions) ? actions.map(action => runAction(action)) : runAction(actions);

        break;
      default:
        new Function(`${actionName}.apply(this, ${JSON.stringify(parsedActionArgs)})`)();
        action?.onCompleted && runAction(action?.onCompleted);
    }
  });
}

/**
 * Attach events to the dom element based on the JSON structure
 */
function linkEvents(host: HTMLElement, events: JaseciComponent['events']) {
  Object.keys(events).map((eventName: JaseciEventName) => {
    switch (eventName) {
      case 'onClick': {
        events['onClick'].map(action => {
          host.addEventListener('click', () => {
            runAction(action);
          });
        });

        break;
      }
      case 'onEnterKeyPress': {
        events['onEnterKeyPress'].map(action => {
          host.addEventListener('keydown', keyboardEvent => {
            if (keyboardEvent.key === 'Enter') {
              runAction(action);
            }
          });
        });
        break;
      }
      case 'onKeyPress':
        events['onKeyPress'].map(action => {
          host.addEventListener('keydown', keyboardEvent => {
            if (keyboardEvent.key.toLowerCase() === action?.key?.trim().toLowerCase()) {
              runAction(action);
            }
          });
        });
        break;
      default: {
      }
    }
  });
}

// BUILT-IN Actions
function update(element: Element, property: string, value: unknown) {
  element[property] = value;
}

function append(targetComponent: Element, newComponentString: string) {
  // extract vars
  const variables = newComponentString.match(/var[(](.*?)[)]/g);
  let parsedArgs;

  if (variables) {
    parsedArgs = parseArgs(variables, { withOriginal: true });

    Object.keys(parsedArgs).map(variable => {
      newComponentString = newComponentString.replaceAll(variable, parsedArgs[variable]);
    });
  }

  let newComponent = JSON.parse(newComponentString);
  console.log({ newComponent });

  const childComp = renderComponentTree([newComponent] as any);
  targetComponent.shadowRoot.innerHTML += childComp;
}
