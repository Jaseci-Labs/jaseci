import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-breadcrumbs',
  styleUrl: 'jsc-breadcrumbs.css',
  shadow: true,
})
export class Breadcrumbs {
  @Prop() name: string;
  @Prop() label: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;
  @Prop() links: string;
  @Prop() operations: string;
  @Element() host: HTMLElement;

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <Fragment>
        <div class="text-sm breadcrumbs">
          <ul>
            {getProp(this.links).map(link => (
              <li>
                <a href={link.href} target={link.target}>
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </Fragment>
    );
  }
}
