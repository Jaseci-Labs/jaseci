import { Component, Element, Event, EventEmitter, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-checkbox',
  styleUrl: 'jsc-checkbox.css',
  shadow: true,
})
export class Checkbox {
  @Prop({ reflect: true }) value: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() name: string;
  @Prop() label: string;
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
    this.value = String((event.target as HTMLInputElement).checked);
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
            type="checkbox"
            // use onInput since it's evaluates immediately
            onInput={this.onInputChangeValue.bind(this)}
            class={clsx(
              `checkbox w-full`,
              this.fullwidth !== 'true' && 'max-w-xs',
              this.size && {
                'checkbox-xs': this.size === 'xs',
                'checkbox-sm': this.size === 'sm',
                'checkbox-md': this.size === 'md',
                'checkbox-lg': this.size === 'lg',
              },
              this.palette && {
                'checkbox-primary': this.palette === 'primary',
                'checkbox-secondary': this.palette === 'secondary',
                'checkbox-accent': this.palette === 'accent',
              },
            )}
            placeholder={this.placeholder}
          ></input>
        </label>
        {false && (
          <input class="checkbox-primary checkbox-secondary checkbox-accent checkbox-info checkbox-error checkbox-warning checkbox-success checkbox-sm checkbox-lg checkbox-xs checkbox-xl"></input>
        )}
      </div>
    );
  }
}
