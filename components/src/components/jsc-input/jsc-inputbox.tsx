import { Component, Prop, h } from '@stencil/core';

@Component({
  tag: 'jsc-inputbox',
  styleUrl: 'jsc-inputbox.css',
  shadow: true,
})
export class Input {
  @Prop() placeholder: string;
  @Prop() fullwidth: string;
  @Prop() padding: string;
  @Prop() margin: string;

  render() {
    return (
      <input
        style={{
          padding: this.padding,
          margin: this.margin,
        }}
        class={`input ${this.fullwidth === 'true' ? 'fullWidth' : ''}`}
        placeholder={this.placeholder}
      ></input>
    );
  }
}
