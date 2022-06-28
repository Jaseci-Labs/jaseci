import { Component, Element, Event, EventEmitter, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-select',
  styleUrl: 'jsc-select.css',
  shadow: true,
})
export class Input {
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
  @Prop() options: string;
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
      <div class={clsx('form-control w-full', this.fullwidth !== 'true' && 'max-w-xs')}>
        {this.label && (
          <label class="label">
            <span class="label-text">{this.label}</span>
            {this.altLabel && <span class="label-text-alt">{this.altLabel}</span>}
          </label>
        )}
        <select
          name={this.name}
          style={{
            ...JSON.parse(this.css),
          }}
          // value={this.value}
          // type={this.type}
          // use onInput since it's evaluates immediately
          onInput={this.onInputChangeValue.bind(this)}
          class={clsx(
            `select select-bordered w-full`,
            this.fullwidth !== 'true' && 'max-w-xs',
            this.palette && {
              'select-primary': this.palette === 'primary',
              'select-secondary': this.palette === 'secondary',
              'select-accent': this.palette === 'accent',
              'select-success': this.palette === 'success',
              'select-info': this.palette === 'info',
              'select-warning': this.palette === 'warning',
              'select-error': this.palette === 'error',
            },
          )}
          // placeholder={this.placeholder}
        >
          <option disabled selected>
            {this.placeholder}
          </option>
          {getProp<{ name: string; label: string }[]>(this.options)?.map(option => (
            <option>{option.label}</option>
          ))}
        </select>
        {/* register some classes so they aren't purged by daisy-ui */}
        {false && (
          <select class="select-primary select-secondary select-accent select-info select-error select-warning select-success select-sm select-lg select-xs select-xl"></select>
        )}
      </div>
    );
  }
}
