import './ParcelForm.css';
import { calculateRoute } from '../../services/api';
import handleError from '../../modules/error/errorHandler';
import config from '../../modules/config/config';

class ParcelForm {
    constructor() {
        this.form = document.getElementById('parcelForm');
        this.bindEvents();
    }

    bindEvents() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
    }

    validateWeight(weight) {
        return weight >= config.validation.weight.min &&
            weight <= config.validation.weight.max;
    }

    async handleSubmit(e) {
        e.preventDefault();

        const weight = parseFloat(document.getElementById('weight').value);

        if (!this.validateWeight(weight)) {
            alert(`Weight must be between ${config.validation.weight.min} and ${config.validation.weight.max} kg`);
            return;
        }

        const parcelData = {
            source: document.getElementById('source').value,
            destination: document.getElementById('destination').value,
            weight
        };

        try {
            const data = await calculateRoute(parcelData);
            this.dispatchRouteCalculated(data);
        } catch (error) {
            handleError(error);
        }
    }

    dispatchRouteCalculated(data) {
        const event = new CustomEvent('routeCalculated', { detail: data });
        document.dispatchEvent(event);
    }
}

export default ParcelForm;
