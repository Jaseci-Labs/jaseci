import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-date-picker',
  styleUrl: 'jsc-date-picker.css',
  shadow: true,
})
export class DatePicker {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() label: string;
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
    Object.assign(this.host.style, {
      'box-sizing': 'border-box',
      'overflowX': 'auto',
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return <jsc-inputbox label={this.label} type="date"></jsc-inputbox>;
  }
}
