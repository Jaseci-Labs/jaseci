import { computeVar } from './events';

/**
 * Runs a function if all action conditions are passing -> resolves to true
 */
export function checkCond(cond: ActionCondition[]) {
  let passing: boolean = true;

  cond.map(condition => {
    let [val1, condName, val2] = condition.split('::');
    val1 = computeVar(val1);
    val2 = computeVar(val2);
    condName = condName.split('#').pop();

    switch (condName as ActionConditionName) {
      case 'eq':
        passing = checkEquality(val1, val2);
        break;
      case 'neq':
        passing = !checkEquality(val1, val2);
        break;
      case 'gt':
        passing = checkGreaterThan(Number(val1), Number(val2));
        break;
      default:
        passing = checkEquality(val1, val2);
        break;
    }
  });

  return {
    run(cb: () => unknown) {
      passing && cb();
    },
  };
}

export function checkEquality(val1: unknown, val2: unknown) {
  return val1 === val2;
}

export function checkGreaterThan(val1: number, val2: number) {
  return val1 > val2;
}
