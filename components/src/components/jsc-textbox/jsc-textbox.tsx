import { Component, Element, Event, EventEmitter, Fragment, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

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
  @Prop() altLabel: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() operations: string;
  @Prop() events: string;
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

        <textarea
          style={{
            ...JSON.parse(this.css),
          }}
          value={this.value}
          class={clsx(
            `textarea textarea-bordered`,
            this.fullwidth !== 'true' && 'max-w-xs',
            this.palette && {
              'textarea-primary': this.palette === 'primary',
              'textarea-secondary': this.palette === 'secondary',
              'textarea-accent': this.palette === 'accent',
              'textarea-success': this.palette === 'success',
              'textarea-info': this.palette === 'info',
              'textarea-warning': this.palette === 'warning',
              'textarea-error': this.palette === 'error',
            },
          )}
          onInput={this.onInputChangeValue.bind(this)}
          placeholder={this.placeholder}
        ></textarea>
      </div>
    );
  }
}
