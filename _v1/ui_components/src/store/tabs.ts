import { createStore } from '@stencil/store';

export const tabsStore = createStore<Record<string, { selected: string }>>({});

export const setSelectedTab = (tabsName: string, tabName: string) => {
  tabsStore.state = {
    ...tabsStore.state,
    [tabsName]: { selected: tabName },
  };
};

export const getSelectedTab = (tabsName: string) => {
  return tabsStore.state[tabsName].selected;
};
