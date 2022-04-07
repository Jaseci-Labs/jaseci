import { Component, Element, h, Prop } from '@stencil/core';
import { ItemsPropValue, JustifyPropValue } from '../../types/propTypes';
import { setUpEvents } from '../../utils/events';
import { itemsValue, justifyValue } from '../../utils/propValueMappings';

@Component({
  tag: 'jsc-row',
  styleUrl: 'jsc-row.css',
  shadow: true,
})
export class Row {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;
  @Prop() justify: JustifyPropValue = 'start';
  @Prop() items: ItemsPropValue = 'start';
  @Prop() operations: string;

  componentDidLoad() {
    const childrenSlot = this.host.querySelector('div[slot=children]') as HTMLSlotElement;

    Object.assign((childrenSlot as HTMLElement).style, {
      'box-sizing': 'border-box',
      'justifyContent': justifyValue[this.justify],
      'alignItems': itemsValue[this.items],
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
  }

  render() {
    return <slot name="children"></slot>;
  }
}
