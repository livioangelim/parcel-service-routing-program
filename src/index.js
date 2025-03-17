import './styles/global.css';
import ParcelForm from './components/ParcelForm/ParcelForm';
import RouteDisplay from './components/RouteDisplay/RouteDisplay';

document.addEventListener('DOMContentLoaded', () => {
    new ParcelForm();
    new RouteDisplay();
});
