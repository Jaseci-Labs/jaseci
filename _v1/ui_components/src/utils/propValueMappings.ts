import { ItemsPropValue, JustifyPropValue } from '../types/propTypes';

export const justifyValue: Record<JustifyPropValue, string> = {
  start: 'flex-start',
  end: 'flex-end',
  center: 'center',
  between: 'space-between',
  around: 'space-around',
  evenly: 'space-evenly',
};

export const itemsValue: Record<ItemsPropValue, string> = {
  start: 'flex-start',
  end: 'flex-end',
  center: 'center',
};
