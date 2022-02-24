import { Component, h } from '@stencil/core';
import { renderComponentTree } from '../../utils/utils';

@Component({
  tag: 'jsc-app',
  styleUrl: 'jsc-app.css',
  shadow: true,
})
export class App {
  render() {
    return (
      <div
        innerHTML={renderComponentTree([
          {
            component: 'Navbar',
            props: { label: 'Jaseci App', links: JSON.stringify([]) },
          },
        ])}
      ></div>
    );
  }
}
