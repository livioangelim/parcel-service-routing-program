# Parcel Service Routing Program

A full-stack application for optimizing parcel delivery routes.

## Project Structure

```
parcel-service-routing-program/
├── backend/
│   ├── src/
│   │   ├── controllers/
│   │   ├── models/
│   │   │   ├── cargo.py
│   │   │   ├── hash_table.py
│   │   │   ├── package.py
│   │   │   ├── truck.py
│   │   │   └── vehicle.py
│   │   ├── routes/
│   │   ├── tests/
│   │   │   └── test_distance.py
│   │   └── utils/
│   │       ├── distance.py
│   │       └── route_optimizer.py
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ParcelForm/
│   │   │   │   └── ParcelForm.css
│   │   │   └── RouteDisplay/
│   │   │       └── RouteDisplay.css
│   │   ├── config/
│   │   ├── error/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── App.tsx
│   │   ├── index.js
│   │   └── index.tsx
│   ├── public/
│   ├── .babelrc
│   ├── .env
│   ├── package.json
│   └── webpack.config.js
├── csv/
│   ├── addresses.csv
│   ├── distances.csv
│   └── packages.csv
├── .gitignore
├── docker-compose.yml
├── list-files.ps1
├── Procfile
└── setup.ps1
```

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- PowerShell 5.1 or higher

## Development Setup

1. Clone the repository
2. Run the setup script:
```powershell
.\setup.ps1
```

3. The setup script will:
   - Create Python virtual environment
   - Install Python dependencies
   - Install Node.js dependencies
   - Configure development environment

## Project Organization

- `backend/`: Python Flask application
  - `src/`: Application source code
  - `controllers/`: Request handlers
  - `models/`: Data models and business logic
  - `routes/`: API endpoint definitions
  - `utils/`: Helper functions and utilities

- `frontend/`: React TypeScript application
  - `src/`: Application source code
  - `components/`: React components
  - `config/`: Configuration files
  - `services/`: API service layers
  - `styles/`: Global styles and variables

- `csv/`: Data files for addresses and distances

## Development Scripts

- `setup.ps1`: Initialize development environment
- `list-files.ps1`: Generate project structure documentation

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
