import { Component, Element, Fragment, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-tab',
  styleUrl: 'jsc-tab.css',
  shadow: true,
})
export class Tab {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() label: string;
  @Prop() tabsEl: HTMLJscTabsElement;
  @Prop() selectedTab: string;
  @Prop({ mutable: true }) operations;

  componentDidRender() {
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
      <div>
        {this.tabsEl && (
          <Fragment>
            <div style={{ padding: '4px' }}>
              <jsc-button
                onClick={() => {
                  this.tabsEl.openTab(this.name);
                }}
                variant="link"
                style={{ paddingRight: '8px' }}
                label={this.label}
                color={this.selectedTab != this.name ? 'dark' : undefined}
              ></jsc-button>
            </div>

            <jsc-divider color={this.selectedTab === this.name ? '#0081F1' : undefined} size={this.selectedTab === this.name ? '2px' : undefined}></jsc-divider>
            {this.host.tagName == 'jsc-tabs' && (
              <div id="contents" class={clsx(this.selectedTab !== this.name && 'hidden')}>
                <slot name="contents"></slot>{' '}
              </div>
            )}
          </Fragment>
        )}
      </div>
    );
  }
}
