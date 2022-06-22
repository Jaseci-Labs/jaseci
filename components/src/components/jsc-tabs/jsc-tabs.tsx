import { Component, Element, Fragment, h, Method, Prop } from '@stencil/core';
import { setSelectedTab, tabsStore } from '../../store/tabs';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-tabs',
  styleUrl: 'jsc-tabs.css',
  shadow: true,
})
export class Tabs {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() selectedTab: string;
  @Prop({ mutable: true }) operations;
  @Prop() content: string;

  @Method()
  async openTab(tabName: string) {
    const tabs = this.host.querySelectorAll('jsc-tab') as NodeListOf<HTMLJscTabElement>;
    this.selectedTab = tabName;

    tabs.forEach(tab => {
      tab.selectedTab = tabName;
      if (tab.name === tabName) {
        this.content = tab.querySelector('div[slot=contents]').innerHTML;
      }
    });
  }

  componentDidLoad() {
    const tabs = this.host.querySelectorAll('jsc-tab') as NodeListOf<HTMLJscTabElement>;
    this.selectedTab = tabs[0].name;
    this.openTab(this.selectedTab);

    tabs.forEach(tab => {
      tab.tabsEl = this.host as HTMLJscTabsElement;
      tab.selectedTab = this.selectedTab;
    });

    Object.assign(this.host.style, {
      'box-sizing': 'border-box',
      'overflowX': 'auto',
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <Fragment>
        <div>
          <jsc-row>
            <div style={{ margin: '24px 0' }}>
              <slot name="tabs"></slot>
            </div>
          </jsc-row>
        </div>

        <div innerHTML={this.content}></div>
      </Fragment>
    );
  }
}
