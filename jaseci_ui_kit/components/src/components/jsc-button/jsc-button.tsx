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
  @Prop() active: string;
  @Prop() tooltip: string;
  @Prop({ attribute: 'fullwidth' }) fullWidth: string;
  @Prop({ attribute: 'tooltipposition' }) tooltipPosition: string;
  @Prop({ attribute: 'tooltippalette' }) tooltipPalette: string;
  @Prop() noRadius: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() operations: string;
  @Prop() palette: 'primary' | 'secondary' | 'accent' | 'link' | 'info' | 'success' | 'warning' | 'error' | 'ghost';
  @Prop() size: 'sm' | 'md' | 'lg' | 'xs' = 'md';

  renderButton = () => (
    <button
      data-theme={getTheme()}
      name={this.name}
      style={JSON.parse(this.css as any)}
      class={clsx([
        `btn`,
        'w-full',
        this.palette && `btn-${this.palette}`,
        this.variant === 'link' && ['btn-link'],
        this.active === 'true' && ['btn-active'],
        this.noRadius === 'true' && ['rounded-none'],
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
  );

  componentDidLoad() {
    this.host.style.display = this.fullWidth === 'true' ? 'block' : 'inline-block';
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
        {this.tooltip ? (
          <div
            class={clsx(
              'tooltip',
              this.tooltipPalette && {
                'tooltip-primary': this.tooltipPalette === 'primary',
                'tooltip-secondary': this.tooltipPalette === 'secondary',
                'tooltip-accent': this.tooltipPalette === 'accent',
                'tooltip-info': this.tooltipPalette === 'info',
                'tooltip-success': this.tooltipPalette === 'success',
                'tooltip-warning': this.tooltipPalette === 'warning',
                'tooltip-error': this.tooltipPalette === 'error',
              },
              this.tooltipPosition && {
                'tooltip-bottom': this.tooltipPosition === 'bottom',
                'tooltip-left': this.tooltipPosition === 'left',
                'tooltip-right': this.tooltipPosition === 'right',
              },
            )}
            data-tip={this.tooltip}
          >
            {this.renderButton()}
          </div>
        ) : (
          <Fragment>{this.renderButton()}</Fragment>
        )}

        {/* register some classes so they aren't purged by daisy-ui */}
        {false && <button class="btn-seconary btn-primary btn-accent btn-info btn-info btn-success btn-warning btn-error btn-ghost btn-link btn-xs w-full"></button>}
      </Fragment>
    );
  }
}
