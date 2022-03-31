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
  setMarkup(value) {
    this.markup = value;
    console.log(this.markup);
  }

  componentDidLoad() {
    console.log(this.markup);
  }

  render() {
    return (
      <div>
        <div innerHTML={renderComponentTree(this.markup)}></div>
      </div>
    );
  }
}
