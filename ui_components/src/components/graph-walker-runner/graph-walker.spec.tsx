import { h } from '@stencil/core';
import { mockFetch, newSpecPage } from '@stencil/core/testing';
import { GraphWalkerRunner } from './graph-walker-runner';
import { walkerList } from './mockData/walker_list';
import walker_run_result from './mockData/walker_run_result.json';

describe('graph-walker', () => {
  afterEach(() => {
    mockFetch.reset();
  });

  test('component renders', async () => {
    const page = await newSpecPage({
      components: [GraphWalkerRunner],
      template: () => <graph-walker-runner onWalkerCompleted={() => {}} walkers={walkerList} serverUrl="http://api.backend.dev" sentinel="" nodeId=""></graph-walker-runner>,
    });

    const tableRows = page.root.shadowRoot.querySelector('tbody').querySelectorAll('tr');
    const useWalker = page.root.shadowRoot.querySelector('tbody').querySelector('tr:nth-of-type(1)').querySelector('td:nth-of-type(2)').querySelector('label') as HTMLLabelElement;

    expect(useWalker.innerHTML).toBe('Use');
    expect(tableRows.length).toBe(walkerList.length);

    const subtitle = page.root.shadowRoot.querySelector("[data-testid='subTitle']");

    const inputTableRows = page.root.shadowRoot.querySelector('tbody').querySelectorAll('tr');

    expect(subtitle.innerHTML).toContain('Choose a walker to run on this node');
    expect(inputTableRows.length).toBe(19);
  });

  test('build context works', async () => {
    const walkerRunner = new GraphWalkerRunner();
    walkerRunner.walkerContext = [
      ['a', '1', 'number'],
      ['b', '2', 'number'],
      ['c', '3', 'number'],
      ['d', '4', 'string'],
    ];

    expect(walkerRunner.buildContext()).toEqual({ a: 1, b: 2, c: 3, d: '4' });
  });

  test('run walker works', async () => {
    const walkerRunner = new GraphWalkerRunner();
    walkerRunner.serverUrl = 'http://api.backend.dev';

    mockFetch.json(walker_run_result, 'http://api.backend.dev/js/walker_run');

    const response = await walkerRunner.runWalker('nd', 'test_walker', { a: 1, b: 2, c: 3, d: '4' }, 'testSentinel');

    expect(response).toStrictEqual(walker_run_result);
  });
});
