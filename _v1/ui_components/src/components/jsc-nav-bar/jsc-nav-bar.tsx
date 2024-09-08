import { Component, Element, Fragment, h, Prop, Watch } from '@stencil/core';
import { getTheme } from '../../store/configStore';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-nav-bar',
  styleUrl: 'jsc-nav-bar.css',
  shadow: true,
})
export class NavBar {
  /**
   * The title of the app bar.
   */
  @Prop({ mutable: true }) label: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() name: string;
  @Prop() events: string;
  @Prop() operations: string;
  @Prop() links: string;
  @Element() host: HTMLElement;

  @Watch('label')
  validateLabel(newLabel: string) {
    if (typeof newLabel !== 'number') {
      throw new Error('Label must be a string.');
    }
  }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <Fragment>
        <div data-theme={getTheme()} class="navbar bg-neutral text-neutral-content">
          <div class="flex-1 px-8">
            <a class="btn btn-ghost normal-case text-xl">{this.label}</a>
          </div>
          <div class="flex-none px-8">
            <ul class="menu menu-horizontal p-0">
              {getProp(this.links).map(link => (
                <li {...(link.links ? { tabindex: '0' } : {})}>
                  <a href={link.href || '#'} target={link.target}>
                    {link.label}
                    {link.links && (
                      <svg class="fill-current" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                        <path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" />
                      </svg>
                    )}
                  </a>

                  {link.links && (
                    <ul class="p-2 bg-base-100 text-base-content">
                      {link.links.map(sublink => (
                        <li>
                          <a href={sublink.href || '#'} target={sublink.target}>
                            {sublink.label}
                          </a>
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Fragment>
    );
  }
}
