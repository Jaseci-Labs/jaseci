import { checkCond } from './conditions';
import { renderComponentTree } from './utils';

export function setUpEvents(host: HTMLElement, events: string) {
  if (events) {
    host.removeAttribute('events');
    const parsedEvents: JaseciComponent['events'] = JSON.parse(events);
    linkEvents(host, parsedEvents);
  }
}

type ParseArgsConfig = { withOriginal?: boolean };

/**
 * Inject the provided args for an action into the defined args of an operation
 */
export function computeOpArgs(operationActionArgs: string[], actionArgs: (string | number)[]) {
  let argValues = {};

  operationActionArgs.map((operationArg, index) => {
    // const matchedArgs = operationArg.match(/arg[(](.*?)[)]/g);
    argValues[`arg(${operationArg})`] = actionArgs[index];
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

  checkCond(action.cond || []).run(() => {
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
        let newComponentString = JSON.stringify(newComponent);

        append(targetComponent, newComponentString);
        action?.onCompleted && runAction(action?.onCompleted);
        break;
      case 'runOperation':
        const operation = action?.operation;
        if (typeof operation !== 'string') throw new Error('Operation must be a string.');
        if (!operation.includes('.')) throw new Error('Invalid operation. Operation and component not specified.');
        const [opTargetComponentName, operationName] = operation.split('.');
        const opTargetComponent = getComponentByName(opTargetComponentName);
        const opTargetComponentOperations = opTargetComponent.getAttribute('operations');
        if (!opTargetComponentOperations) throw new Error(`No operation defined for ${opTargetComponentName}`);
        const operationDef = JSON.parse(opTargetComponentOperations)[operationName];

        operationDef.run.map(operationAction => {
          const opArgsMap = computeOpArgs(operationDef.args, action?.args);

          const newActionArgs = operationAction?.args?.map(arg => {
            let parsedArg = arg;

            Object.keys(opArgsMap).map(opArg => {
              if (typeof parsedArg == 'string' || typeof parsedArg === 'object') {
                if (typeof parsedArg == 'object') {
                  parsedArg = JSON.stringify(parsedArg);
                  if (parsedArg.includes(opArg)) {
                    parsedArg = parsedArg.replaceAll(opArg, opArgsMap[opArg]);
                    parsedArg = JSON.parse(parsedArg);
                  }
                } else {
                  if (parsedArg.includes(opArg)) {
                    parsedArg = parsedArg.replaceAll(opArg, opArgsMap[opArg]);
                    parsedArg = parsedArg;
                  }
                }
              }
            });

            return parsedArg;
          });

          operationAction.args = newActionArgs;

          runAction(operationAction);
        });

        action?.onCompleted && runAction(action?.onCompleted);
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

  targetComponent.shadowRoot.innerHTML += renderComponentTree([newComponent] as any);
}
