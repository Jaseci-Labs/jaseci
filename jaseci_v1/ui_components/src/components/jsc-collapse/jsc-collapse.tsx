import { Component, Element, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-collapse',
  styleUrl: 'jsc-collapse.css',
  shadow: true,
})
export class Collapse {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() icon: 'plus' | 'arrow' = 'arrow';
  @Prop() label: string;
  @Prop() palette: 'primary' | 'secondary' | 'accent';
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
    // const childrenSlot = this.host.shadowRoot.querySelector('slot[name=children]') as HTMLSlotElement;

    // childrenSlot.assignedNodes().map(node => {
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
      <div
        tabindex="0"
        class={clsx('collapse collapse-arrow border border-base-300 bg-base-100 rounded-box', {
          'collapse-plus': this.icon === 'plus',
          'collapse-arrow': this.icon === 'arrow',
        })}
      >
        <input type="checkbox" />
        <div
          class={clsx(
            'collapse-title text-xl font-medium',
            this.palette && {
              'bg-primary text-neutral-content': this.palette === 'primary',
              'bg-secondary text-secondary-content': this.palette === 'secondary',
              'bg-accent text-primary-content': this.palette === 'accent',
            },
          )}
        >
          {this.label}
        </div>
        <div class="collapse-content">
          <div class="py-2">
            <slot name="children"></slot>
          </div>
        </div>
      </div>
    );
  }
}
