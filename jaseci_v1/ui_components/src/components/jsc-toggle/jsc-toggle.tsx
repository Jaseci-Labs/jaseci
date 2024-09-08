import { Component, Element, Event, EventEmitter, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-toggle',
  styleUrl: 'jsc-toggle.css',
  shadow: true,
})
export class Toggle {
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
  @Prop() size: 'xs' | 'sm' | 'md' | 'lg';
  @Prop() palette: 'primary' | 'secondary' | 'accent' | 'info' | 'success' | 'warning' | 'error';
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
        <label class="label cursor-pointer">
          <span class="label-text pr-2">{this.label}</span>
          <input
            name={this.name}
            style={{
              ...JSON.parse(this.css),
            }}
            checked={this.value === 'true'}
            type="checkbox"
            // use onInput since it's evaluates immediately
            onInput={this.onInputChangeValue.bind(this)}
            class={clsx(
              `toggle w-full`,
              this.fullwidth !== 'true' && 'max-w-xs',
              this.size && {
                'toggle-xs': this.size === 'xs',
                'toggle-sm': this.size === 'sm',
                'toggle-md': this.size === 'md',
                'toggle-lg': this.size === 'lg',
              },
              this.palette && {
                'toggle-primary': this.palette === 'primary',
                'toggle-secondary': this.palette === 'secondary',
                'toggle-accent': this.palette === 'accent',
                'toggle-success': this.palette === 'success',
                'toggle-info': this.palette === 'info',
                'toggle-warning': this.palette === 'warning',
                'toggle-error': this.palette === 'error',
              },
            )}
            placeholder={this.placeholder}
          ></input>
        </label>
        {false && (
          <input class="toggle-primary toggle-secondary toggle-accent toggle-info toggle-error toggle-warning toggle-success toggle-sm toggle-lg toggle-xs toggle-xl"></input>
        )}
      </div>
    );
  }
}
