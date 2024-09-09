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
  @Prop() type: 'date' | 'datetime' = 'date';
  @Prop() label: string;
  @Prop({ mutable: true }) operations;
  @Prop({ reflect: true }) value: string;

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
    return <jsc-inputbox onValueChanged={value => (this.value = value.target['value'])} label={this.label} type={this.type === 'date' ? 'date' : 'datetime-local'}></jsc-inputbox>;
  }
}
