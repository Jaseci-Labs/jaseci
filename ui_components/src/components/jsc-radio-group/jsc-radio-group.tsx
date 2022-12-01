import { Component, Element, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-radio-group',
  styleUrl: 'jsc-radio-group.css',
  shadow: true,
})
export class RadioGroup {
  @Prop({ reflect: true }) value: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() name: string;
  @Prop() label: string;
  @Prop() type: string = 'text';
  @Prop() events: string;
  @Prop() fullwidth: string;
  @Prop() placeholder: string;
  @Prop() palette: string;
  @Prop() operations: string;
  @Prop() options: string;
  @Element() host: HTMLElement;

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
          <div class="flex gap-2">
            {getProp(this.options)?.map(option => (
              <jsc-radio
                label={option.label}
                value={this.value === option.name ? 'true' : 'false'}
                onValueChanged={e => {
                  if (e.detail === 'on') this.value = option?.name;
                }}
                palette={this.palette as any}
              ></jsc-radio>
            ))}
          </div>
        </label>

        {false && <input class="radio-info radio-error radio-warning radio-success radio-xl radio-primary radio-secondary radio-accent radio-xs radio-sm radio-lg"></input>}
      </div>
    );
  }
}
