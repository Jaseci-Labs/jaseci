import { Component, h, Prop } from '@stencil/core';

@Component({
  tag: 'jsc-label',
  styleUrl: 'jsc-label.css',
  shadow: true,
})
export class Label {
  @Prop() label: string;
  @Prop() htmlFor: string;
  @Prop() operations: string;

  render() {
    return (
      <label htmlFor={this.htmlFor} class="label">
        {this.label}
      </label>
    );
  }
}
