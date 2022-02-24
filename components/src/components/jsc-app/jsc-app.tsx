import { Component, h } from '@stencil/core';
import { renderComponentTree } from '../../utils/utils';

@Component({
  tag: 'jsc-app',
  styleUrl: 'jsc-app.css',
  shadow: true,
})
export class App {
  get 'markup'() {
    return renderComponentTree([
      {
        component: 'Navbar',
        slots: {
          links: [
            { component: 'NavLink', props: { label: 'Home' } },
            { component: 'NavLink', props: { label: 'About' } },
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
                height: '300px',
                padding: '10px',
                background: 'black',
                align: 'middle',
                crossAlign: 'middle',
              },
              slots: {
                children: [
                  {
                    component: 'Container',
                    props: {
                      background: 'red',
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

            {
              component: 'Row',
              props: {
                width: '100%',
                height: '300px',
                padding: '10px',
                background: 'grey',
                align: 'start',
                crossAlign: 'middle',
              },
              slots: {
                children: [
                  {
                    component: 'Container',
                    props: {
                      background: 'red',
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
  'top';

  'render'() {
    return (
      <div>
        <div innerHTML={this.markup}></div>
      </div>
    );
  }
}
