import { Component, Prop, h } from '@stencil/core';
import { clsx } from 'clsx';

@Component({
  tag: 'graph-node-info',
  styleUrl: 'graph-node-info.css',
  shadow: true,
})
export class GraphNodeInfo {
  @Prop() selectedInfoTab: 'details' | 'context' | 'info' = 'context';
  @Prop() context: { [key: string]: any } = {};
  @Prop() details: { [key: string]: any } = {};
  @Prop() info: { [key: string]: any } = {};

  render() {
    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <div class="tabs">
            <a class={clsx(['tab tab-bordered', this.selectedInfoTab === 'context' && 'tab-active'])} onClick={() => (this.selectedInfoTab = 'context')}>
              Context
            </a>
            <a class={clsx(['tab tab-bordered', this.selectedInfoTab === 'details' && 'tab-active'])} onClick={() => (this.selectedInfoTab = 'details')}>
              Details
            </a>
            <a class={clsx(['tab tab-bordered', this.selectedInfoTab === 'info' && 'tab-active'])} onClick={() => (this.selectedInfoTab = 'info')}>
              Info
            </a>
          </div>
        </div>
        <div style={{ marginTop: '4px' }} id="details">
          {this.selectedInfoTab === 'context' && (
            <div id="context">
              {Object.keys(this.context)?.length ? (
                Object.keys(this.context).map(contextKey => (
                  <div key={contextKey}>
                    <p style={{ fontWeight: 'bold' }}>{contextKey}</p>
                    <p>
                      {Array.isArray(this.context[contextKey])
                        ? this.context[contextKey].map(item => item.toString()).join(', ')
                        : typeof this.context[contextKey] === 'boolean'
                        ? this.context[contextKey]?.toString()
                        : this.context[contextKey]}
                    </p>
                  </div>
                ))
              ) : (
                <p>No context information available</p>
              )}
            </div>
          )}

          {this.selectedInfoTab === 'info' && (
            <div id="info">
              {Object.keys(this.info)?.length ? (
                Object.keys(this.info).map(infoKey => (
                  <div key={infoKey}>
                    <p style={{ fontWeight: 'bold' }}>{infoKey}</p>
                    <p>
                      {Array.isArray(this.info[infoKey])
                        ? this.info[infoKey].map(item => item.toString()).join(', ')
                        : typeof this.info[infoKey] === 'boolean'
                        ? this.info[infoKey]?.toString()
                        : this.info[infoKey]}
                    </p>
                  </div>
                ))
              ) : (
                <p>No info available</p>
              )}
            </div>
          )}

          {this.selectedInfoTab === 'details' && (
            <div>
              {Object.keys(this.details)?.length ? (
                Object.keys(this.details).map(detailsKey => (
                  <div key={detailsKey}>
                    <p style={{ fontWeight: 'bold' }}>{detailsKey}</p>
                    <p>
                      {Array.isArray(this.details[detailsKey])
                        ? this.details[detailsKey].map(item => item.toString()).join(', ')
                        : typeof this.details[detailsKey] === 'boolean'
                        ? this.details[detailsKey]?.toString()
                        : this.details[detailsKey]}
                    </p>
                  </div>
                ))
              ) : (
                <p>No details available</p>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }
}
