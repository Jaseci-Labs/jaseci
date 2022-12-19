import { Component, Prop, h, State, Event, EventEmitter } from '@stencil/core';
import { Walker } from '../jsc-graph/jsc-graph';

@Component({
  tag: 'graph-walker-runner',
  styleUrl: 'graph-walker-runner.css',
  shadow: true,
})
export class GraphWalkerRunner {
  @Prop() walkers: Walker[];
  @Prop({ attribute: 'nodeid' }) nodeId: string;
  @Prop({ attribute: 'serverurl', mutable: true }) serverUrl: string;
  @Prop() sentinel: string;
  @State() selectedWalker: string = '';

  @State() walkerContext: [string, string | number, 'number' | 'string'][] = [['', '', 'string']];

  @Event() walkerCompleted: EventEmitter<string>;

  async runWalker(nd: string, walker_name: string, ctx: Record<string, any>, snt: string) {
    return await fetch(`${this.serverUrl}/js/walker_run`, {
      body: JSON.stringify({
        name: walker_name,
        nd,
        snt,
        ctx,
      }),
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `token ${localStorage.getItem('token')}`,
      },
    }).then(async res => {
      this.walkerCompleted.emit(this.nodeId);
      return res.json();
    });
  }

  addProperty() {
    this.walkerContext = [...this.walkerContext, ['', '', 'string']];
  }

  buildContext() {
    const context = {};

    this.walkerContext.map(item => {
      context[item[0]] = item[2] === 'string' ? item[1] : Number(item[1]);
    });

    return context;
  }

  render() {
    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', paddingTop: '4px' }}>
          <h3 class="text-lg font-bold">{this.selectedWalker ? 'Walker Context' : 'Select Walker'}</h3>
          {this.selectedWalker && (
            <button data-testId="addProperty" class="btn btn-info btn-xs ml-2" onClick={() => (this.selectedWalker = '')}>
              Change Walker
            </button>
          )}
        </div>

        {this.selectedWalker ? (
          <p data-testId="subTitle" class="py-4 font-medium">
            Add walker properties and values to the context <em>(running walker: {this.selectedWalker})</em>
          </p>
        ) : (
          <p data-testId="subTitle" class="py-4 font-medium">
            Choose a walker to run on this node
          </p>
        )}
        {this.selectedWalker ? (
          <div>
            <table class="table w-full table-compact">
              <thead>
                <tr class={'active'}>
                  <th>Name</th>
                  <th>Value</th>
                  <th>Type</th>
                </tr>
              </thead>
              <tbody>
                {this.walkerContext.map((item, itemIndex) => (
                  <tr>
                    <td>
                      <jsc-inputbox
                        size="xs"
                        value={item[0] as string}
                        onValueChanged={e => {
                          const newWalkerContext = [...this.walkerContext];
                          newWalkerContext[itemIndex][0] = e.detail;
                          this.walkerContext = newWalkerContext;
                        }}
                      ></jsc-inputbox>
                    </td>
                    <td>
                      <jsc-inputbox
                        size="xs"
                        value={item[1] as string}
                        type={item[2] === 'number' ? 'number' : 'text'}
                        onValueChanged={e => {
                          const newWalkerContext = [...this.walkerContext];
                          newWalkerContext[itemIndex][1] = e.detail;
                          this.walkerContext = newWalkerContext;
                        }}
                        onKeyDown={e => e.key === 'Enter' && this.addProperty()}
                      ></jsc-inputbox>
                    </td>
                    <td>
                      <jsc-select
                        selected="string"
                        size="xs"
                        options={[{ label: 'string' }, { label: 'number' }]}
                        onValueChanged={e => {
                          const newWalkerContext = [...this.walkerContext];
                          newWalkerContext[itemIndex][2] = e.detail as 'number' | 'string';
                          this.walkerContext = newWalkerContext;
                        }}
                      ></jsc-select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <button data-testId="addProperty" class="btn btn-info btn-xs ml-2" onClick={() => this.addProperty()}>
              Add Property
            </button>
            <div class="flex justify-end">
              <button class="btn btn-sm ml-2" onClick={() => this.runWalker(this.nodeId, this.selectedWalker, this.buildContext(), this.sentinel)}>
                Submit
              </button>
            </div>
          </div>
        ) : (
          <table class="table w-full table-compact">
            <thead>
              <tr class={'active'}>
                <th>Name</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {this.walkers.map((walker, index) => (
                <tr class={index % 2 === 0 ? undefined : 'active'}>
                  <td>{walker.name}</td>
                  <td>
                    <label class="btn btn-info btn-xs ml-2" onClick={() => (this.selectedWalker = walker.name)}>
                      Use
                    </label>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  }
}
