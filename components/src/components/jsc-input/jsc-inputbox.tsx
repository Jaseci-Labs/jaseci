import { Component, Element, Event, EventEmitter, Fragment, h, Prop, Watch } from '@stencil/core';
import { setUpEvents } from '../../utils/events';

@Component({
  tag: 'jsc-inputbox',
  styleUrl: 'jsc-inputbox.css',
  shadow: true,
})
export class Input {
  @Prop({ reflect: true }) value: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() name: string;
  @Prop() label: string;
  @Prop() events: string;
  @Prop() fullwidth: string;
  @Prop() placeholder: string;
  @Element() host: HTMLElement;

  @Event() valueChanged: EventEmitter<string>;
  private onInputChangeValue(event: Event) {
    this.value = (event.target as HTMLInputElement).value;
    this.valueChanged.emit(this.value);
  }

  componentDidLoad() {
    setUpEvents(this.host, this.events);

    this.setFullWidth();
  }

  setFullWidth() {
    Object.assign(this.host.style, {
      width: this.fullwidth === 'true' ? '100%' : 'auto',
    });
  }

  @Watch('fullwidth')
  fullwidthChange() {
    this.setFullWidth();
  }

  render() {
    return (
      <Fragment>
        {this.label && <jsc-label htmlFor={this.name} label={this.label}></jsc-label>}
        <input
          name={this.name}
          style={{
            ...JSON.parse(this.css),
          }}
          value={this.value}
          // use onInput since it's evaluates immediately
          onInput={this.onInputChangeValue.bind(this)}
          class={`input ${this.fullwidth === 'true' ? 'fullWidth' : ''}`}
          placeholder={this.placeholder}
        ></input>
      </Fragment>
    );
  }
}
