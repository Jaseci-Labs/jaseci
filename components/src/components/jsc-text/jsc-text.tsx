import { Component, h, Prop } from '@stencil/core';

@Component({
  tag: 'jsc-text',
  styleUrl: 'jsc-text.css',
  shadow: true,
})
export class MyComponent {
  @Prop() variant: 'simple' | 'title' = 'simple';
  @Prop() value: string;

  render() {
    return <p>{this.value}</p>;
  }
}
