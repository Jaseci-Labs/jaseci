import { Component, Prop, h } from '@stencil/core';

@Component({
  tag: 'jsc-row',
  styleUrl: 'jsc-row.css',
  shadow: true,
})
export class NavLink {
  @Prop() width: string;
  @Prop() height: string;
  @Prop() background: string;
  @Prop() margin: string;
  @Prop() padding: string;

  render() {
    return (
      <div
        style={{
          width: this.width,
          height: this.height,
          background: this.background,
          margin: this.margin,
          padding: this.padding,
          boxSizing: 'border-box',
          display: 'flex',
        }}
      >
        <slot name="children"></slot>
      </div>
    );
  }
}
