import { Component, h, Prop } from '@stencil/core';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-label',
  styleUrl: 'jsc-label.css',
  shadow: true,
})
export class Label {
  @Prop() label: string;
  @Prop() name: string;
  @Prop() htmlFor: string;
  @Prop() operations: string;

  componentDidLoad() {
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <label htmlFor={this.htmlFor} class="label">
        {this.label}
      </label>
    );
  }
}
