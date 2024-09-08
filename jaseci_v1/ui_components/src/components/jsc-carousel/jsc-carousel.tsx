import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-carousel',
  styleUrl: 'jsc-carousel.css',
  shadow: true,
})
export class Carousel {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() label: string;
  @Prop() slide: string = 'item2';
  @Prop() size: string;
  @Prop() palette: string;
  @Prop() placeholder: string;
  tooltip: HTMLElement;
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
    // childrenSlot.assignedNodes().map(node => {
    Object.assign(this.host.style, {
      'box-sizing': 'border-box',
      'overflowX': 'auto',
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <Fragment>
        <div class="carousel w-full relative">
          <div
            id="item1"
            class={clsx(
              'abolute z-10 carousel-item w-full !transition-all !ease-in !duration-500 !scale100 block !opacity-100',
              this.slide !== 'item1' && '!scale-0 z-0 !opacity-0',
            )}
          >
            <img src="https://placeimg.com/800/200/arch" class="w-full object-cover" />
          </div>
          <div
            id="item2"
            class={clsx(
              'absolute z-10 carousel-item w-full !transition-all !ease-in !duration-500 !scale-100 block !opacity-100',
              this.slide !== 'item2' && '!scale-0 z-0 !opacity-0',
            )}
          >
            <img src="https://cdn.mos.cms.futurecdn.net/tXr5UjKDsDBrYBQM9znb2c-1024-80.jpg.webp" class="w-full object-cover" />
          </div>
          <div
            id="item3"
            class={clsx(
              'carousel-item z-10 w-full !transition-all !ease-in !duration-500 scale-1000 block absolute !opacity-100',
              this.slide !== 'item3' && '!scale-0 z-0 opacity-0',
            )}
          >
            <img src="https://placeimg.com/800/200/people" class="w-full object-cover" />
          </div>
          <div
            id="item4"
            class={clsx(
              'absolute z-10 carousel-item w-full !transition-all !ease-in !duration-500 !scale-100 !opacity-100 block',
              this.slide !== 'item4' && '!scale-0 z-0 opacity-0',
            )}
          >
            <img src="https://placeimg.com/800/200/food" class="w-full object-cover" />
          </div>
        </div>
        <p class="hidden"></p>
        <div class="flex justify-center w-full py-2 gap-2">
          <a href="#item1" onClick={() => (this.slide = 'item1')} class="btn btn-xs">
            1
          </a>
          <a href="#item2" onClick={() => (this.slide = 'item2')} class="btn btn-xs">
            2
          </a>
          <a href="#item3" onClick={() => (this.slide = 'item3')} class="btn btn-xs">
            3
          </a>
          <a href="#item4" onClick={() => (this.slide = 'item4')} class="btn btn-xs">
            4
          </a>
        </div>

        {/* <div class="carousel w-full">
          <div id="slide1" class="carousel-item relative w-full">
            <img src="https://placeimg.com/800/200/arch" class="w-full" />
            <div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
              <a href="#slide4" class="btn btn-circle">
                ❮
              </a>
              <a href="#slide2" class="btn btn-circle">
                ❯
              </a>
            </div>
          </div>
          <div id="slide2" class="carousel-item relative w-full">
            <img src="https://placeimg.com/800/200/tech" class="w-full" />
            <div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
              <a href="#slide1" class="btn btn-circle">
                ❮
              </a>
              <a href="#slide3" class="btn btn-circle">
                ❯
              </a>
            </div>
          </div>
          <div id="slide3" class="carousel-item relative w-full">
            <img src="https://placeimg.com/800/200/people" class="w-full" />
            <div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
              <a href="#slide2" class="btn btn-circle">
                ❮
              </a>
              <a href="#slide4" class="btn btn-circle">
                ❯
              </a>
            </div>
          </div>
          <div id="slide4" class="carousel-item relative w-full">
            <img src="https://placeimg.com/800/200/nature" class="w-full" />
            <div class="absolute flex justify-between transform -translate-y-1/2 left-5 right-5 top-1/2">
              <a href="#slide3" class="btn btn-circle">
                ❮
              </a>
              <a href="#slide1" class="btn btn-circle">
                ❯
              </a>
            </div>
          </div>
        </div> */}
      </Fragment>
    );
  }
}
