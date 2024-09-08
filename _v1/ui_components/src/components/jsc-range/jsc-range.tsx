import { Component, Element, Event, EventEmitter, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-range',
  styleUrl: 'jsc-range.css',
  shadow: true,
})
export class Range {
  @Prop({ reflect: true }) value: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() name: string;
  @Prop() min: string;
  @Prop() max: string;
  @Prop() label: string;
  @Prop({ attribute: 'defaultvalue' }) defaultValue: string = '20';
  @Prop({ attribute: 'showvalue' }) showValue: string = 'true';
  @Prop() altLabel: string;
  @Prop() type: string = 'text';
  @Prop() events: string;
  @Prop() fullwidth: string;
  @Prop() placeholder: string;
  @Prop() operations: string;
  @Prop() size: 'xs' | 'sm' | 'md' | 'lg';
  @Prop() palette: 'primary' | 'secondary' | 'accent';
  @Element() host: HTMLElement;

  @Event() valueChanged: EventEmitter<string>;
  private onInputChangeValue(event: Event) {
    this.value = (event.target as HTMLInputElement).value;
    this.valueChanged.emit(this.value);
  }

  componentDidLoad() {
    if (this.defaultValue) this.value = this.defaultValue;
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
        <label class="label cursor-pointer">
          <span class="label-text pr-2">{this.label}</span>
          {this.showValue === 'true' && <span class="label-text-alt">{this.value}</span>}
        </label>
        <input
          name={this.name}
          value={this.value || this.defaultValue}
          style={{
            ...JSON.parse(this.css),
          }}
          checked={this.value === 'true'}
          type="range"
          min={this.min}
          max={this.max}
          // use onInput since it's evaluates immediately
          onInput={this.onInputChangeValue.bind(this)}
          class={clsx(
            `range w-full`,
            this.fullwidth !== 'true' && 'max-w-xs',
            this.size && {
              'range-xs': this.size === 'xs',
              'range-sm': this.size === 'sm',
              'range-md': this.size === 'md',
              'range-lg': this.size === 'lg',
            },
            this.palette && {
              'range-primary': this.palette === 'primary',
              'range-secondary': this.palette === 'secondary',
              'range-accent': this.palette === 'accent',
            },
          )}
          placeholder={this.placeholder}
        ></input>
        {false && <input class="range-xl range-primary range-secondary range-accent range-xs range-sm range-lg"></input>}
      </div>
    );
  }
}
