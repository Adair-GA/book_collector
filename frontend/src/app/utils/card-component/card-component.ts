import {
  AfterViewInit,
  Component,
  ElementRef,
  input,
  OnInit,
  Signal,
  viewChild,
} from '@angular/core';

@Component({
  selector: 'app-card-component',
  imports: [],
  templateUrl: './card-component.html',
  styleUrl: './card-component.css',
})
export class CardComponent implements OnInit, AfterViewInit {
  bg = input<string>();
  text = input<string>();
  divRef: Signal<ElementRef<HTMLDivElement>> = viewChild.required('card');
  bounds!: DOMRect;

  ngOnInit() {
    if (!(this.bg() || this.text())) {
      throw Error('One of bg or text must be initialized');
    }
  }

  ngAfterViewInit() {
    const element = this.divRef().nativeElement;

    this.bounds = element.getBoundingClientRect();
  }

  rotateToMouse(e: MouseEvent) {
    const mouseX = e.clientX;
    const mouseY = e.clientY;
    const leftX = mouseX - this.bounds.x;
    const topY = mouseY - this.bounds.y;
    const center = {
      x: leftX - this.bounds.width / 2,
      y: topY - this.bounds.height / 2,
    };
    const distance = Math.sqrt(center.x ** 2 + center.y ** 2);

    const element = this.divRef().nativeElement;

    element.style.transform = `
      scale3d(1.07, 1.07, 1.07)
      rotate3d(
        ${center.y / 100},
        ${-center.x / 100},
        0,
        ${Math.log(distance) * 2}deg
      )
    `;
    // @ts-expect-error Funciona, pero typescript dice que no
    element.querySelector('.glow').style.backgroundImage = `
    radial-gradient(
      circle at
      ${center.x * 2 + this.bounds.width / 2}px
      ${center.y * 2 + this.bounds.height / 2}px,
      #ffffff55,
      #0000000f
    )
  `;
  }

  reset() {
    const element = this.divRef().nativeElement;

    element.style.transform = '';
  }
}
