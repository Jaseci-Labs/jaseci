import { Component, Prop, h, Element } from '@stencil/core';
import { ItemsPropValue, JustifyPropValue } from '../../types/propTypes';
import { itemsValue, justifyValue } from '../../utils/propValueMappings';

@Component({
  tag: 'jsc-column',
  styleUrl: 'jsc-column.css',
  shadow: true,
})
export class Column {
  @Element() host: HTMLElement;
  @Prop() width: string;
  @Prop() height: string;
  @Prop() background: string;
  @Prop() margin: string;
  @Prop() padding: string;
  @Prop() justify: JustifyPropValue = 'start';
  @Prop() items: ItemsPropValue = 'start';

  componentDidLoad() {
    const childrenSlot = this.host.querySelector('div[slot=children]') as HTMLSlotElement;

    Object.assign((childrenSlot as HTMLElement).style, {
      'box-sizing': 'border-box',
      'width': this.width,
      'height': this.height,
      'background': this.background,
      'margin': this.margin,
      'justifyContent': justifyValue[this.justify],
      'alignItems': itemsValue[this.items],
    });
  }

  render() {
    return (
      // <div
      //   style={{
      //     width: this.width,
      //     height: this.height,
      //     background: this.background,
      //     margin: this.margin,
      //     padding: this.padding,
      //     boxSizing: 'border-box',
      //     display: 'flex',
      //     flexDirection: 'column',
      //   }}
      //   class={`align-${this.align} ${`cross-align-${this.crossAlign}`}`}
      // >
      <slot name="children"></slot>
    );
  }
}
