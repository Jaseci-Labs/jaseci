import { Component, h, Method, Prop } from '@stencil/core';
import { renderComponentTree } from '../../utils/utils';

@Component({
  tag: 'jsc-app',
  styleUrl: 'jsc-app.css',
  shadow: true,
})
export class App {
  @Prop({ mutable: true }) markup: JaseciComponent[];

  @Method()
  async setMarkup(value) {
    this.markup = value;
  }

  render() {
    return (
      <div>
        <div innerHTML={renderComponentTree(this.markup)}></div>
      </div>
    );
  }
}
