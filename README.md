# Solar Samriddhi ☀️

A Django-based solar energy calculator that helps users estimate their solar panel potential based on their rooftop area and location.

## Features

- 🏠 Property information collection
- 🏗️ Roof type selection
- 📊 Electricity bill analysis
- 🗺️ Interactive map for rooftop area selection (Leaflet.js)
- 🌍 Real-time solar radiation data (Solcast API)
- ⚡ Solar energy production calculations
- 💰 Cost savings estimation
- 🌱 CO₂ offset calculations

## Tech Stack

- **Backend:** Django 5.2
- **Frontend:** HTML, CSS, JavaScript
- **Maps:** Leaflet.js with satellite imagery
- **API:** Solcast Solar Radiation API
- **Database:** SQLite

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/solar-samriddhi.git
cd solar-samriddhi
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django requests
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Open http://127.0.0.1:8000 in your browser

## Project Structure

```
Django/
├── manage.py
├── Django/              # Main Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── DT_project/          # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   └── migrations/
├── DT_Templates/        # HTML templates
│   ├── index.html       # Landing page
│   ├── index2-8.html    # Form steps
│   └── index9.html      # Results page
└── static/
    └── css/
        └── main.css     # Styling
```

## Calculation Methodology

1. **Usable Area:** 70% of total roof area (accounts for spacing/obstructions)
2. **Panel Size:** 1.7 m² per panel (400W standard panel)
3. **Performance Ratio:** 0.75 (accounts for system losses)
4. **Energy Production:** System Capacity (kW) × Sun Hours × 0.75
5. **Savings:** Based on ₹8/kWh electricity rate
6. **CO₂ Offset:** 0.82 kg CO₂/kWh (India grid average)

## License

MIT License

## Contributing

Pull requests are welcome! For major changes, please open an issue first.
