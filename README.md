# Logistics Route Optimization Service

A scalable system for optimizing delivery routes across multiple vehicle types.

## Project Architecture

```
parcel-service-routing-program/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   ├── cargo.py         # Cargo types and validation
│   │   │   ├── vehicle.py       # Vehicle abstractions (Truck, Drone)
│   │   │   └── hash_table.py    # Efficient data storage
│   │   ├── utils/
│   │   │   ├── distance.py      # Distance calculations
│   │   │   └── route_optimizer.py # Route optimization logic
│   │   ├── tests/
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── ParcelForm/      # Form handling and validation
│   │   │   │   ├── ParcelForm.js
│   │   │   │   └── ParcelForm.css
│   │   │   └── RouteDisplay/    # Route visualization
│   │   │       ├── RouteDisplay.js
│   │   │       └── RouteDisplay.css
│   │   ├── modules/             # Core functionality
│   │   │   ├── config/         # Application configuration
│   │   │   │   └── config.js   # API endpoints, validation rules
│   │   │   └── error/          # Error handling
│   │   │       └── errorHandler.js
│   │   ├── services/           # API communication
│   │   │   └── api.js         # Backend interaction
│   │   ├── styles/            # Global styles
│   │   │   ├── global.css    # Base styles
│   │   │   └── variables.css # Theme variables
│   │   └── index.js          # Application entry point
│   └── public/               # Static assets
│       ├── index.html       # Main HTML template
│       └── styles.css      # Legacy styles
└── README.md
```

## Core Components

### Vehicle System
- Abstract Vehicle base class
- Specialized implementations (Truck, Drone)
- Capacity and speed constraints
- Cargo type compatibility

### Cargo Management
- Multiple cargo categories (Standard, Express, Fragile)
- Weight-based validation
- Delivery time windows
- Status tracking

### Route Optimization
- Vehicle-specific routing
- Multi-stop journey planning
- Cost optimization
- Real-time availability checks

## API Reference

### POST /api/route
Calculate optimal delivery route.

```json
{
  "source": "string",
  "destination": "string",
  "weight": "number",
  "category": "standard|express|fragile",
  "delivery_time": "datetime" // Optional
}
```

Response:
```json
{
  "route": ["location1", "location2"],
  "cost": "number",
  "vehicle_id": "string",
  "cargo_id": "number"
}
```

## Detailed Setup

### Backend Setup
```bash
# Create and activate virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if applicable)
python src/manage.py migrate

# Start server
python src/main.py
```

### Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start

# Build for production
npm run build
```

## Data Structures

### Hash Table
- Custom implementation for O(1) lookups
- Dynamic bucket sizing
- Collision handling

### Vehicle Hierarchy
```python
Vehicle (Abstract)
├── Truck
│   └── Properties: capacity, speed
└── Drone
    └── Properties: capacity, speed, range
```

## Testing

### Backend Tests
```bash
cd backend
python -m pytest src/tests/         # Run all tests
python -m pytest src/tests/test_distance.py  # Specific test
```

### Frontend Tests
```bash
cd frontend
npm test                  # Run all tests
npm run test:coverage    # With coverage report
```

## Performance Optimizations
- Vehicle-specific route calculations
- Efficient cargo-vehicle matching
- Cached route patterns
- Load distribution across vehicle fleet

## Security Features

- Input validation
- Rate limiting
- Authentication for API endpoints
- Data sanitization

## Technologies Used

### Backend
- Python 3.8+
- Flask (Web framework)
- pytest (Testing)
- Custom data structures

### Frontend
- Modern JavaScript (ES6+)
- Custom components
- CSS Grid/Flexbox
- Fetch API

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

MIT License - See LICENSE file for details

## Support

For support, email support@parcelrouting.com or create an issue.

## Frontend Architecture

### Components
- **ParcelForm**: Handles user input and form submission
  - Form validation
  - Weight constraints checking
  - Real-time input validation
  - Error state management

- **RouteDisplay**: Visualizes delivery routes
  - Route path rendering
  - Cost calculation display
  - Vehicle assignment information
  - Status updates

### Modules
- **Config**: Centralized configuration
  - API endpoints
  - Validation rules
  - Environment settings

- **Error**: Error handling system
  - Custom error classes
  - Error message formatting
  - User-friendly error display

### Services
- **API**: Backend communication
  - Route calculation requests
  - Error handling
  - Response parsing
  - Request retry logic

### Styles
- **Global**: Base styling system
  - CSS reset
  - Typography
  - Layout utilities

- **Variables**: Theme configuration
  - Color palette
  - Spacing units
  - Breakpoints
  - Typography scale
