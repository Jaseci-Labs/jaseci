import { Component, Element, Event, EventEmitter, Fragment, h, Prop, Watch } from '@stencil/core';
import { setUpEvents } from '../../utils/events';

@Component({
  tag: 'jsc-textbox',
  styleUrl: 'jsc-textbox.css',
  shadow: true,
})
export class Textbox {
  @Prop({ reflect: true }) value: string;
  @Prop() placeholder: string;
  @Prop() fullwidth: string;
  @Prop() name: string;
  @Prop() label: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;

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

        <textarea
          style={{
            ...JSON.parse(this.css),
          }}
          value={this.value}
          class={`textbox ${this.fullwidth === 'true' ? 'fullWidth' : ''}`}
          onInput={this.onInputChangeValue.bind(this)}
          placeholder={this.placeholder}
        ></textarea>
      </Fragment>
    );
  }
}
