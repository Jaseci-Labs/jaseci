import { Component, Element, h, Prop } from '@stencil/core';
import { ItemsPropValue, JustifyPropValue } from '../../types/propTypes';
import { setUpEvents } from '../../utils/events';
import { itemsValue, justifyValue } from '../../utils/propValueMappings';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-column',
  styleUrl: 'jsc-column.css',
  shadow: true,
})
export class Column {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop() justify: JustifyPropValue = 'start';
  @Prop() items: ItemsPropValue = 'start';
  @Prop() events: string;
  @Prop() operations: string;
  @Prop() name: string;

  componentDidLoad() {
    const childrenSlot = this.host.querySelector('div[slot=children]') as HTMLSlotElement;

    Object.assign((childrenSlot as HTMLElement).style, {
      'box-sizing': 'border-box',
      'justify-content': justifyValue[this.justify],
      'align-items': itemsValue[this.items],
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return <slot name="children"></slot>;
  }
}
