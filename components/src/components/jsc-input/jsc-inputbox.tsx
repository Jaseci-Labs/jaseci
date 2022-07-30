import { Component, Element, Event, EventEmitter, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

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
      <div class={clsx('form-control w-full', this.fullwidth !== 'true' && 'max-w-xs')}>
        {this.label && (
          <label class="label">
            <span class="label-text">{this.label}</span>
            {this.altLabel && <span class="label-text-alt">{this.altLabel}</span>}
          </label>
        )}
        <input
          name={this.name}
          style={{
            ...JSON.parse(this.css),
          }}
          value={this.value}
          type={this.type}
          // use onInput since it's evaluates immediately
          onInput={this.onInputChangeValue.bind(this)}
          class={clsx(
            `input input-bordered w-full`,
            this.fullwidth !== 'true' && 'max-w-xs',
            this.palette && {
              'input-primary': this.palette === 'primary',
              'input-secondary': this.palette === 'secondary',
              'input-accent': this.palette === 'accent',
              'input-success': this.palette === 'success',
              'input-info': this.palette === 'info',
              'input-warning': this.palette === 'warning',
              'input-error': this.palette === 'error',
            },
          )}
          placeholder={this.placeholder}
        ></input>
        {/* register some classes so they aren't purged by daisy-ui */}
        {false && <input class="input-xl input-primary input-secondary input-accent input-info input-success input-warning input-error input-lg input-sm input-xs"></input>}
      </div>
    );
  }
}
