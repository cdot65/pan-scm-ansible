/**
 * termynal.js
 * A lightweight, modern and extensible animated terminal window, using
 * async/await.
 *
 * @author Ines Montani <ines@ines.io>
 * @version 0.0.1
 * @license MIT
 */

'use strict';

/** Generate a terminal widget. */
class Termynal {
    /**
     * Construct the widget's settings.
     * @param {(string|Node)=} container - Query selector or container element.
     * @param {Object=} options - Custom settings.
     * @param {string} options.prefix - Prefix to use for data attributes.
     * @param {number} options.startDelay - Delay before animation, in ms.
     * @param {number} options.typeDelay - Delay between each typed character, in ms.
     * @param {number} options.lineDelay - Delay between each line, in ms.
     * @param {number} options.progressLength - Number of characters displayed as progress bar.
     * @param {string} options.progressChar – Character to use for progress bar, defaults to █.
	 * @param {number} options.progressPercent - Max percent of progress.
     * @param {string} options.cursor – Character to use for cursor, defaults to ▋.
     * @param {Object[]} lineData - Dynamically loaded line data objects.
     * @param {boolean} options.noInit - Don't initialise the animation.
     */
    constructor(container = '#termynal', options = {}) {
        this.container = (typeof container === 'string') ? document.querySelector(container) : container;
        this.pfx = `data-${options.prefix || 'ty'}`;
        this.startDelay = options.startDelay || 600;
        this.typeDelay = options.typeDelay || 90;
        this.lineDelay = options.lineDelay || 1500;
        this.progressLength = options.progressLength || 40;
        this.progressChar = options.progressChar || '█';
		this.progressPercent = options.progressPercent || 100;
        this.cursor = options.cursor || '▋';
        this.lineData = options.lineData || [];
        this.lines = [...this.container.querySelectorAll(`[${this.pfx}]`)].concat(this.lineData);
        this.useLines = options.useLines || false;
        this.init();
    }

    /**
     * Initialise the widget, get lines, clear container and start animation.
     */
    init() {
        if (this.lines.length) this.container.setAttribute(`${this.pfx}-initialized`, '');
        else return;

        this.container.innerHTML = '';
        for (let line of this.lines) {
            line.removeAttribute(`${this.pfx}-cursor`);
            if (line.getAttribute(`${this.pfx}`) === 'input') {
                line.setAttribute(`${this.pfx}-cursor`, this.cursor);
            }
            this.container.appendChild(line);
        }

        // Add a new line
        const newLine = document.createElement('span');
        newLine.innerHTML = ' ';
        this.container.appendChild(newLine);

        this.start();
    }

    /**
     * Start the animation and rener the lines depending on their data attributes.
     */
    async start() {
        this.container.setAttribute(`${this.pfx}-initialized`, '');
        await this._wait(this.startDelay);

        for (let line of this.lines) {
            const type = line.getAttribute(this.pfx);
            const delay = line.getAttribute(`${this.pfx}-delay`) || this.lineDelay;

            if (type == 'input') {
                line.setAttribute(`${this.pfx}-cursor`, this.cursor);
                await this.type(line);
                await this._wait(delay);
            }

            else if (type == 'progress') {
                await this.progress(line);
                await this._wait(delay);
            }

            else {
                this.container.appendChild(line);
                await this._wait(delay);
            }

            line.removeAttribute(`${this.pfx}-cursor`);
        }
    }

    /**
     * Animate a typed line.
     * @param {Node} line - The line element to render.
     */
    async type(line) {
        const chars = [...line.textContent];
        const delay = line.getAttribute(`${this.pfx}-typeDelay`) || this.typeDelay;
        line.textContent = '';
        this.container.appendChild(line);

        for (let char of chars) {
            await this._wait(delay);
            line.textContent += char;
        }
    }

    /**
     * Animate a progress bar.
     * @param {Node} line - The line element to render.
     */
    async progress(line) {
        const progressLength = line.getAttribute(`${this.pfx}-progressLength`) || this.progressLength;
        const progressChar = line.getAttribute(`${this.pfx}-progressChar`) || this.progressChar;
        const chars = progressChar.repeat(progressLength);
		const progressPercent = line.getAttribute(`${this.pfx}-progressPercent`) || this.progressPercent;
        line.textContent = '';
        this.container.appendChild(line);

        for (let i = 1; i < chars.length + 1; i++) {
            await this._wait(this.typeDelay);
            const percent = Math.round(i / chars.length * 100);
            line.textContent = `${chars.slice(0, i)} ${percent}%`;
			if (percent > progressPercent) {
				break;
			}
        }
    }

    /**
     * Helper function for animation delays, called with `await`.
     * @param {number} time - Timeout, in ms.
     */
    _wait(time) {
        return new Promise(resolve => setTimeout(resolve, time));
    }
}

/**
 * Get all data-ty-* attributes from a line, and return them as JSON.
 * @param {Node} line - Line with attributes.
 */
function getLineData(line) {
    const data = {};
    const type = line.getAttribute('data-ty');
    data.type = type;
    if (type === 'input') {
        data.cursor = line.getAttribute('data-ty-cursor') || '▋';
    } else if (type === 'progress') {
        data.progressLength = line.getAttribute('data-ty-progressLength') || '40';
        data.progressChar = line.getAttribute('data-ty-progressChar') || '█';
    }
    return data;
}

/**
 * Initialise all termynal containers.
 */
document.addEventListener('DOMContentLoaded', () => {
    const termnals = [...document.querySelectorAll('[data-termynal]')];
    for (let term of termnals) {
        new Termynal(term);
    }
});