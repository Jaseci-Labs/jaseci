import { Component, Element, Fragment, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { getTheme } from '../../store/configStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-button',
  styleUrl: 'jsc-button.css',
  shadow: true,
})
export class Button {
  @Element() host: HTMLElement;
  @Prop() label: string;
  @Prop() events: string;
  @Prop() name: string;
  @Prop() variant: 'default' | 'link' = 'default';
  @Prop() color: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() operations: string;
  @Prop() palette: 'primary' | 'secondary' | 'accent' | 'ghost' | 'link' | 'info' | 'success' | 'warning' | 'error' | 'ghost';
  @Prop() size: 'sm' | 'md' | 'lg' | 'xs' = 'md';

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  @Watch('color')
  setColor(newColor: string, _oldValue: string) {
    Object.assign(this.host.style, {
      '--button-color': `var(--${newColor}3)`,
      '--button-bg-color': `var(--${newColor}3)`,
    });
  }

  render() {
    return (
      <Fragment>
        {/* register some classes so they aren't purged by daisy-ui */}
        {false && <button class="btn-primary btn-seconary btn-info btn-accent btn-ghost btn-link btn-info btn-success btn-warning btn-error btn-xs"></button>}

        <button
          data-theme={getTheme()}
          name={this.name}
          style={JSON.parse(this.css as any)}
          class={clsx([
            `btn`,
            this.palette && `btn-${this.palette}`,
            this.variant === 'link' && ['btn-link'],
            this.size && {
              'btn-sm': this.size === 'sm',
              'btn-lg': this.size === 'lg',
              'btn-md': this.size === 'md',
              'btn-xs': this.size === 'xs',
            },
          ])}
        >
          {this.label}
        </button>
      </Fragment>
    );
  }
}
