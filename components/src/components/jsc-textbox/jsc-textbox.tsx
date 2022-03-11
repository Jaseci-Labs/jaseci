import { Component, Prop, h } from '@stencil/core';

@Component({
  tag: 'jsc-textbox',
  styleUrl: 'jsc-textbox.css',
  shadow: true,
})
export class Input {
  @Prop() placeholder: string;
  @Prop() fullwidth: string;
  @Prop() padding: string;
  @Prop() margin: string;

  render() {
    return (
      <textarea
        style={{
          padding: this.padding,
          margin: this.margin,
        }}
        class={`textbox ${this.fullwidth === 'true' ? 'fullWidth' : ''}`}
        placeholder={this.placeholder}
      ></textarea>
    );
  }
}
