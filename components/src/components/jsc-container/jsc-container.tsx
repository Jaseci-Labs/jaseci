import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';

@Component({
  tag: 'jsc-container',
  styleUrl: 'jsc-container.css',
  shadow: true,
})
export class Container {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
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
    this.operations = JSON.parse(localStorage.getItem(`op-${this.name}`));
  }

  render() {
    return <slot name="children"></slot>;
  }
}
