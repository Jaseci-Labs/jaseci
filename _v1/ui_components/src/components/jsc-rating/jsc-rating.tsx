import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';
import clsx from 'clsx';

@Component({
  tag: 'jsc-rating',
  styleUrl: 'jsc-rating.css',
  shadow: true,
})
export class Rating {
  @Prop() name: string;
  @Prop() label: string;
  @Prop() stars: string = '5';
  @Prop() value: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;
  @Prop() palette: 'primary' | 'secondary' | 'accent' | 'neutral' | 'warning' | 'error' | 'info' | 'success';
  @Prop() operations: string;
  @Element() host: HTMLElement;

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <Fragment>
        <div class="rating">
          {Array.from({ length: Number(this.stars) }, (_v, i) => i + 1).map(v => (
            <input
              type="radio"
              name="rating-1"
              class={clsx(
                'mask mask-star-2',
                this.palette && {
                  'bg-primary': this.palette === 'primary',
                  'bg-secondary': this.palette === 'secondary',
                  'bg-accent': this.palette === 'accent',
                  'bg-success': this.palette === 'success',
                  'bg-info': this.palette === 'info',
                  'bg-warning': this.palette === 'warning',
                  'bg-error': this.palette === 'error',
                },
              )}
              checked={this.value === String(v)}
              onClick={() => (this.value = String(v))}
            />
          ))}
        </div>

        {false && <div class="bg-primary bg-secondary bg-accent bg-success bg-info bg-warning bg-error"></div>}
      </Fragment>
    );
  }
}
