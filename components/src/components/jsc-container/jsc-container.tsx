import { Component, Element, h, Prop } from '@stencil/core';

@Component({
  tag: 'jsc-container',
  styleUrl: 'jsc-container.css',
  shadow: true,
})
export class Container {
  @Element() host: HTMLElement;
  @Prop() width: string;
  @Prop() height: string;
  @Prop() background: string;
  @Prop() margin: string;
  @Prop() padding: string;
  @Prop() border: string;

  componentDidLoad() {
    // const childrenSlot = this.host.shadowRoot.querySelector('slot[name=children]') as HTMLSlotElement;

    // childrenSlot.assignedNodes().map(node => {
    Object.assign(this.host.style, {
      'width': this.width,
      'height': this.height,
      'background': this.background,
      'margin': this.margin,
      'padding': this.padding,
      'border': this.border,
      'box-sizing': 'border-box',
      'overflowX': 'auto',
    });
    // });
  }

  render() {
    return <slot name="children"></slot>;
  }
}
