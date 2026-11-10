// Круглый регулятор угла (крутилка).
// Тянуть мышью — поворот, колесо — шаг 5°, двойной клик — сброс в 0°.
// Угол в градусах от −180 до 180, 0° — ручка направлена вправо,
// положительный угол — против часовой стрелки.

const STYLE_ID = "knob-style";
const CSS = `
.knob {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    user-select: none;
}
.knob-dial {
    position: relative;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: #1f2128;
    cursor: grab;
    touch-action: none;
}
.knob-dial:active { cursor: grabbing; }
.knob-dial::before {
    content: "";
    position: absolute;
    inset: 9px;
    border-radius: 50%;
    background: #1a2f6e;
}
.knob-handle {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 50%;
    height: 0;
    transform-origin: 0 0;
}
.knob-handle::before {
    content: "";
    position: absolute;
    left: 0;
    top: -4px;
    width: calc(100% - 4px);
    height: 8px;
    border-radius: 4px;
    background: #dcdcdc;
}
.knob-handle::after {
    content: "";
    position: absolute;
    right: -6px;
    top: -6px;
    width: 16px;
    height: 12px;
    border-radius: 6px;
    background: #2be0a6;
}
.knob-label {
    font-size: 12px;
    color: #ccc;
    text-align: center;
    line-height: 1.3;
}
.knob-label b {
    color: #2be0a6;
}
`;

function injectStyle() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = CSS;
    document.head.appendChild(style);
}

export class Knob {
    constructor(container, { label = "", value = 0, onChange = () => {} } = {}) {
        injectStyle();
        this.onChange = onChange;

        this.root = document.createElement("div");
        this.root.className = "knob";

        this.dial = document.createElement("div");
        this.dial.className = "knob-dial";
        this.dial.title = "Тяните мышью; колесо — шаг 5°; двойной клик — 0°";

        this.handle = document.createElement("div");
        this.handle.className = "knob-handle";
        this.dial.appendChild(this.handle);

        this.text = document.createElement("div");
        this.text.className = "knob-label";

        this.label = label;
        this.root.append(this.dial, this.text);
        container.appendChild(this.root);

        this.dial.addEventListener("pointerdown", (e) => {
            this.dial.setPointerCapture(e.pointerId);
            this.fromPointer(e);
        });
        this.dial.addEventListener("pointermove", (e) => {
            if (this.dial.hasPointerCapture(e.pointerId)) this.fromPointer(e);
        });
        this.dial.addEventListener("wheel", (e) => {
            e.preventDefault();
            this.setValue(this.value + (e.deltaY < 0 ? 5 : -5));
        }, { passive: false });
        this.dial.addEventListener("dblclick", () => this.setValue(0));

        this.setValue(value, false);
    }

    fromPointer(e) {
        const r = this.dial.getBoundingClientRect();
        const dx = e.clientX - (r.left + r.width / 2);
        const dy = e.clientY - (r.top + r.height / 2);
        // Ось Y экрана направлена вниз, поэтому знак меняем
        this.setValue(Math.round(-Math.atan2(dy, dx) * 180 / Math.PI));
    }

    setValue(deg, notify = true) {
        // Приводим к диапазону (−180; 180]
        let v = ((deg + 180) % 360 + 360) % 360 - 180;
        if (v === -180) v = 180;
        this.value = v;
        this.handle.style.transform = `rotate(${-v}deg)`;
        this.text.innerHTML = `${this.label}<br><b>${v}°</b>`;
        if (notify) this.onChange(v);
    }
}
