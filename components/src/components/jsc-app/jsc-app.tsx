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
      <div>
        {JSON.stringify(
          renderComponentTree([
            {
              component: 'Navbar',
              slots: {
                links: [
                  { component: 'Button', props: { label: 'Test' } },
                  {
                    component: 'Button',
                    props: { label: 'Hello' },
                    slots: { links: [{ component: 'Navbar', props: { title: 'cool' } }] },
                  },
                ],
              },
              props: { label: 'Jaseci App' },
            },
          ]),
        )}
        <jsc-nav-bar label="Test">
          <div slot="links">
            <a>Link 1</a>
            <a>Link 2</a>
            <a>Link 3</a>
          </div>
        </jsc-nav-bar>
      </div>
    );
  }
}
