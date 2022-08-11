import { Component, Element, Event, EventEmitter, Fragment, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-radio',
  styleUrl: 'jsc-radio.css',
  shadow: true,
})
export class Radio {
  @Prop({ reflect: true }) value: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() name: string;
  @Prop() label: string;
  @Prop() altLabel: string;
  @Prop() type: string = 'text';
  @Prop() events: string;
  @Prop() fullwidth: string;
  @Prop() placeholder: string;
  @Prop() operations: string;
  @Prop() palette: 'primary' | 'secondary' | 'accent' | 'ghost' | 'link' | 'info' | 'success' | 'warning' | 'error';
  @Element() host: HTMLElement;

  @Event() valueChanged: EventEmitter<string>;
  private onInputChangeValue(event: Event) {
    this.value = (event.target as HTMLInputElement).value;
    this.valueChanged.emit(this.value);
  }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
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
      <div class={clsx('form-control')}>
        <label class="label">
          <span class="label-text pr-2">{this.label}</span>
          <input
            name={this.name}
            style={{
              ...JSON.parse(this.css),
            }}
            checked={this.value === 'true'}
            type="radio"
            // use onInput since it's evaluates immediately
            onInput={this.onInputChangeValue.bind(this)}
            class={clsx(
              `radio w-full`,
              this.fullwidth !== 'true' && 'max-w-xs',
              this.palette && {
                'radio-primary': this.palette === 'primary',
                'radio-secondary': this.palette === 'secondary',
                'radio-accent': this.palette === 'accent',
                'radio-success': this.palette === 'success',
                'radio-info': this.palette === 'info',
                'radio-warning': this.palette === 'warning',
                'radio-error': this.palette === 'error',
              },
            )}
            placeholder={this.placeholder}
          ></input>
        </label>
        {false && <input class="radio-info radio-error radio-warning radio-success radio-xl radio-primary radio-secondary radio-accent radio-xs radio-sm radio-lg"></input>}
      </div>
    );
  }
}
