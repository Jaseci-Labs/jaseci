import { Component, h, Prop } from '@stencil/core';
import { renderComponentTree } from '../../utils/utils';

@Component({
  tag: 'jsc-app',
  styleUrl: 'jsc-app.css',
  shadow: true,
})
export class App {
  @Prop() markup: JaseciComponent[];

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
