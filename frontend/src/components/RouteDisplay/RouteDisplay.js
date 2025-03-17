import './RouteDisplay.css';

class RouteDisplay {
    constructor() {
        this.routeElement = document.getElementById('routeDisplay');
        this.costElement = document.getElementById('costDisplay');
        this.bindEvents();
    }

    bindEvents() {
        document.addEventListener('routeCalculated', this.updateDisplay.bind(this));
    }

    updateDisplay(event) {
        const { route, cost } = event.detail;

        this.routeElement.innerHTML = `
            <h3>Route:</h3>
            <p>${route.join(' → ')}</p>
        `;

        this.costElement.innerHTML = `
            <h3>Total Cost:</h3>
            <p>$${cost.toFixed(2)}</p>
        `;
    }
}

export default RouteDisplay;
