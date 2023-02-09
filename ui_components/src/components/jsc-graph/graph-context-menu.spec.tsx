import { newSpecPage } from '@stencil/core/testing';
import { JscGraphContextMenu } from './graph-context-menu';

it('should show context menu', async () => {
  const page = await newSpecPage({
    components: [JscGraphContextMenu],
    html: `<jsc-graph-context-menu><jsc-graph-context-menu>`,
  });

  // click a node
  const contextMenuEl = page.rootInstance.contextMenuEl;

  // show context menu
  page.rootInstance.show();

  expect(contextMenuEl).not.toBeNull();
  expect(contextMenuEl.style.display).toBe('block');
});

it('should hide context menu', async () => {
  const page = await newSpecPage({
    components: [JscGraphContextMenu],
    html: `<jsc-graph-context-menu><jsc-graph-context-menu>`,
  });

  // click a node
  const contextMenuEl = page.rootInstance.contextMenuEl;

  // show context menu
  page.rootInstance.hide();

  expect(contextMenuEl).not.toBeNull();
  expect(contextMenuEl.style.display).toBe('none');
});

it('should set context menu position', async () => {
  const page = await newSpecPage({
    components: [JscGraphContextMenu],
    html: `<jsc-graph-context-menu><jsc-graph-context-menu>`,
  });

  // click a node
  const contextMenuEl = page.rootInstance.contextMenuEl;

  // show context menu
  page.rootInstance.setPos(100, 200);

  expect(contextMenuEl).not.toBeNull();
  expect(contextMenuEl.style.left).toBe('100px');
  expect(contextMenuEl.style.top).toBe('200px');
});

it('should set clicked item', async () => {
  const page = await newSpecPage({
    components: [JscGraphContextMenu],
    html: `<jsc-graph-context-menu><jsc-graph-context-menu>`,
  });

  // click a node
  const contextMenuEl = page.rootInstance.contextMenuEl;

  // show context menu
  page.rootInstance.setClickedItem({ clickedNode: { id: 'node1' } });

  expect(contextMenuEl).not.toBeNull();
  expect(page.rootInstance.clickedNode.id).toBe('node1');
});
