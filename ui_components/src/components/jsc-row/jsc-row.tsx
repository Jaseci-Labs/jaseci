import { Component, Element, h, Prop } from '@stencil/core';
import { ItemsPropValue, JustifyPropValue } from '../../types/propTypes';
import { setUpEvents } from '../../utils/events';
import { itemsValue, justifyValue } from '../../utils/propValueMappings';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-row',
  styleUrl: 'jsc-row.css',
  shadow: false,
})
export class Row {
  @Element() host: HTMLElement;
  @Prop() name: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;
  @Prop() justify: JustifyPropValue = 'start';
  @Prop() items: ItemsPropValue = 'start';
  @Prop() gap: string;
  @Prop() operations: string;

  componentDidLoad() {
    const childrenSlot = this.host.querySelector('div[slot=children]') as HTMLSlotElement;
    console.log({ childrenSlot });

    Object.assign((childrenSlot as HTMLElement).style, {
      'box-sizing': 'border-box',
      'display': 'flex',
      'justifyContent': justifyValue[this.justify],
      'alignItems': itemsValue[this.items],
      'gap': this.gap,
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return <slot name="children"></slot>;
  }
}
