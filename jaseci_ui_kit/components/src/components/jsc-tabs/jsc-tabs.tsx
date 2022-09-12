import { Component, Element, Fragment, h, Method, Prop } from '@stencil/core';
import clsx from 'clsx';
import { nanoid } from 'nanoid';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations, renderComponentTree } from '../../utils/utils';

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
  @Prop() tabs: string;
  @Prop() tabsComps: { name: string; label: string; render: JaseciComponent[] }[];
  @Prop() content: string;
  @Prop() variant: 'boxed' | 'lifted' | 'basic' | 'bordered' = 'bordered';
  @Prop() container: HTMLElement;

  @Method()
  async openTab(tabName: string) {
    this.container.classList.add('opacity-0');
    setTimeout(() => {
      this.selectedTab = tabName;
      this.content = `${renderComponentTree(this.tabsComps?.find(tab => tab.name === this.selectedTab)?.render)}`;
      this.container.classList.remove('opacity-0');
    }, 100);
  }

  componentDidLoad() {
    // tab is given a unique name if none is provided, to keep the api layer simple
    this.tabsComps = getProp(this.tabs).map(tab => ({ ...tab, name: tab.name || nanoid() }));
    this.openTab(this.tabsComps[0].name);

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
        <div class={clsx('tabs', this.variant === 'boxed' && 'tabs-boxed')}>
          {this.tabsComps?.map(tab => (
            <Fragment>
              {tab && tab?.label && (
                <a
                  class={clsx(
                    'tab',
                    this.selectedTab === tab.name && 'tab-active',
                    this.variant && {
                      'tab-bordered': this.variant === 'bordered',
                      'tab-lifted': this.variant === 'lifted',
                    },
                  )}
                  onClick={() => this.openTab(tab.name)}
                >
                  {tab?.label}
                </a>
              )}
            </Fragment>
          ))}
        </div>

        <div class="tabs mb-2">
          <slot name="tabs"></slot>
        </div>

        <div innerHTML={this.content || `<div></div>`} ref={el => (this.container = el)} class="transition-all duration-150 opacity-0 min-h-[50px] block"></div>
      </Fragment>
    );
  }
}
