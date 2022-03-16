import { Component, Element, Event, EventEmitter, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';

@Component({
  tag: 'jsc-inputbox',
  styleUrl: 'jsc-inputbox.css',
  shadow: true,
})
export class Input {
  @Prop({ reflect: true }) value: string;
  @Prop() placeholder: string;
  @Prop() fullwidth: string;
  @Prop() padding: string;
  @Prop() margin: string;
  @Prop() events: string;
  @Element() host: HTMLElement;

  @Event() valueChanged: EventEmitter<string>;
  private onInputChangeValue(event: Event) {
    this.value = (event.target as HTMLInputElement).value;
    this.valueChanged.emit(this.value);
  }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
  }

  render() {
    return (
      <input
        style={{
          padding: this.padding,
          margin: this.margin,
        }}
        value={this.value}
        // use onInput since it's evaluates immediately
        onInput={this.onInputChangeValue.bind(this)}
        class={`input ${this.fullwidth === 'true' ? 'fullWidth' : ''}`}
        placeholder={this.placeholder}
      ></input>
    );
  }
}
