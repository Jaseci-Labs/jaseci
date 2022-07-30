import { Component, Element, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-divider',
  styleUrl: 'jsc-divider.css',
  shadow: true,
})
export class Divider {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() label?: string;
  @Prop() orientation?: string;
  @Prop() color?: string = 'rgb(206, 212, 218)';
  @Prop() size?: string = '1px';
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
    return <div class={clsx('divider', this.orientation === 'vertical' && 'divider-horizontal')}>{this.label}</div>;
  }
}
