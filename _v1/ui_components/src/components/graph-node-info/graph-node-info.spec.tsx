import { newSpecPage } from '@stencil/core/testing';
import { GraphNodeInfo } from './graph-node-info';

describe('graph-node-info', () => {
  it('renders', async () => {
    const { body, rootInstance } = await newSpecPage({
      components: [GraphNodeInfo],
      html: `<graph-node-info selectedInfoTab="details" context={{ a: 1 }} info={{ a: 2 }} details={{ a: 3 }}></graph-node-info>`,
    });

    rootInstance.selectedInfoTab = 'details';
    console.log(rootInstance.selectedInfoTab);

    const shadowRoot = body.querySelector('graph-node-info').shadowRoot;
    const tabs = shadowRoot.querySelectorAll('.tab');
    const detailsTab = tabs[2] as HTMLAnchorElement;

    const details = shadowRoot.querySelector('#context');
    console.log({ details: details.innerHTML });
    // expect(details.innerHTML).toContain('No context information available.');

    detailsTab.click();

    // console.log({ contextTab, detailsTab, infoTab });
  });
});
