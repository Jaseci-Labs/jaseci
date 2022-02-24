import { Component, h } from '@stencil/core';
import { renderComponentTree } from '../../utils/utils';

@Component({
  tag: 'jsc-app',
  styleUrl: 'jsc-app.css',
  shadow: true,
})
export class App {
  get markup() {
    return renderComponentTree([
      {
        component: 'Navbar',
        slots: {
          links: [
            { component: 'NavLink', props: { label: 'Test' } },
            {
              component: 'NavLink',
              props: { label: 'Hello' },
              slots: { links: [{ component: 'Navbar', props: { title: 'cool' } }] },
            },
          ],
        },
        props: { label: 'Jaseci App' },
      },
      {
        component: 'Container',
        props: {
          width: '100%',
          background: '#0090FF',
          padding: '10px',
          margin: '10px 0',
        },
        slots: {
          children: [
            {
              component: 'Row',
              props: {
                width: '100%',
                padding: '10px',
                background: 'white',
              },
              slots: {
                children: [
                  {
                    component: 'Container',
                    props: {
                      background: 'blue',
                      width: '50px',
                      height: '50px',
                    },
                  },
                  {
                    component: 'Container',
                    props: {
                      background: 'blue',
                      width: '50px',
                      height: '50px',
                    },
                  },
                ],
              },
            },
          ],
        },
      },
    ]);
  }

  render() {
    return (
      <div>
        {JSON.stringify(this.markup)}
        <div innerHTML={this.markup}></div>
      </div>
    );
  }
}
