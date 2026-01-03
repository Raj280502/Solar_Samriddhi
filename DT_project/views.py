from django.shortcuts import render, redirect
from DT_project.models import *
from django.conf import settings
import requests
from requests.exceptions import RequestException
import json
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, "index.html")


def index2(request):
    if request.method == "POST":
        property = request.POST.get('property')
        address = request.POST.get('address')
        
        new_property = Residential_Info(property=property, address=address)
        new_property.save()
        return redirect('/index3/')
       
    return render(request, "index2.html")
 

def index3(request):
    if request.method == "POST":
        rooftop = request.POST.get('rooftop')
    
        if rooftop:
            selected_roof = RoofType(rooftop=rooftop)
            selected_roof.save()
            return redirect('/index4/')
    
    return render(request, "index3.html")


def index4(request):
    if request.method == 'POST':
        stories = request.POST.get('stories')
        
        if stories:
            sel_storey = Storey(stories=stories)
            sel_storey.save()
            return redirect('/index5/')
    return render(request, "index4.html")


def index5(request):
    if request.method == 'POST':
        Bill = request.POST.get('Bill')
        
        if Bill:
            electricity = Electricity(Bill=Bill)
            electricity.save()
            return redirect('/index6/')
    
    return render(request, "index5.html")


def index6(request):
    return render(request, "index6.html")


def index7(request):
    return render(request, "index7.html")


def index8(request):
    """
    Fetch solar radiation data from Solcast API and redirect to results page.
    """
    specific_data = None
    context = {}
    
    # Handle GET request - pre-fill form with data from map selection
    if request.method == 'GET':
        area = request.GET.get('area')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        
        if area:
            context['area'] = area
        if latitude:
            context['latitude'] = latitude
        if longitude:
            context['longitude'] = longitude
    
    # Handle POST request - fetch solar data from API
    if request.method == 'POST':
        try:
            latitude = request.POST.get('latitude')
            panel_area = request.POST.get('panel_area')
            longitude = request.POST.get('longitude')
            hours = request.POST.get('hours')
            area = request.POST.get('area')

            # Check if values are provided
            if not latitude or not longitude or not hours:
                raise ValueError("Latitude, longitude, and hours are required.")

            # Solcast API URL
            api_url = 'https://api.solcast.com.au/world_radiation/estimated_actuals'
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'hours': hours,
                'api_key': 'dkVZL9ZX-bCSbr3pWwpkEnU-7cA34Yfd'
            }
            
            # Set headers to request JSON response format
            headers = {
                'Accept': 'application/json',
            }

            response = requests.get(api_url, params=params, headers=headers)

            # Ensure that the response is valid JSON
            if response.status_code == 200:
                try:
                    weather_data = response.json()
                    estimated_actuals = weather_data.get('estimated_actuals', [])
                    if estimated_actuals:
                        ghi = estimated_actuals[0].get('ghi', 'N/A')
                        return redirect(
                            f"{reverse('index9')}?area={area}&ghi={ghi}&latitude={latitude}"
                            f"&longitude={longitude}&hours={hours}&panel_area={panel_area}"
                        )
                except json.JSONDecodeError:
                    specific_data = f"Invalid JSON received from API"
            else:
                specific_data = f"Error fetching data: {response.status_code}"

        except requests.RequestException as e:
            specific_data = f"API request failed: {str(e)}"
        except ValueError as ve:
            specific_data = f"Input error: {str(ve)}"
        except Exception as e:
            specific_data = f"An unexpected error occurred: {str(e)}"

    context['specific_data'] = specific_data
    return render(request, 'index8.html', context)


def index9(request):
    """
    Calculate and display solar energy potential results.
    
    Calculation methodology:
    1. Determine usable roof area (70% of total due to spacing/obstructions)
    2. Calculate number of panels that fit (standard panel: 1.7 m²)
    3. Calculate system capacity (panels × 400W per panel)
    4. Calculate daily production using: Capacity × Sun Hours × Performance Ratio (0.75)
    5. Estimate savings based on ₹8/kWh electricity rate
    6. Calculate CO2 offset (0.82 kg CO2/kWh for India's grid)
    """
    if request.method == 'GET':
        try:
            # Retrieve parameters from query string
            ghi = request.GET.get('ghi')
            area = request.GET.get('area')
            latitude = request.GET.get('latitude')
            longitude = request.GET.get('longitude')
            hours = request.GET.get('hours')

            # Validate required inputs
            if not ghi or not area:
                raise ValueError("GHI and area are required for the calculation.")

            # Convert inputs to proper types
            ghi_value = float(ghi)  # W/m² from Solcast API
            rooftop_area_m2 = float(area)
            sunlight_hours = float(hours) if hours else 5  # Default 5 hours
            
            # ============================================
            # SOLAR PANEL SPECIFICATIONS
            # ============================================
            # Standard residential solar panel specs:
            panel_length = 1.7  # meters
            panel_width = 1.0   # meters
            panel_area_m2 = panel_length * panel_width  # ~1.7 m² per panel
            
            panel_wattage = 400  # Watts (standard modern panel: 350-450W)
            
            # Account for spacing, obstructions, and installation clearance
            # Typically only 60-80% of roof area is usable
            usable_area_ratio = 0.70
            usable_area = rooftop_area_m2 * usable_area_ratio
            
            # ============================================
            # CALCULATIONS
            # ============================================
            # Number of panels that can fit
            num_panels = int(usable_area // panel_area_m2)
            
            # Ensure at least 1 panel if area is small but valid
            if num_panels == 0 and rooftop_area_m2 >= panel_area_m2:
                num_panels = 1
            
            # System capacity in kW
            system_capacity_kw = (num_panels * panel_wattage) / 1000
            
            # Daily energy production (kWh/day)
            # Formula: System Capacity (kW) × Peak Sun Hours × Performance Ratio
            # Performance ratio (0.75) accounts for:
            # - Inverter efficiency (~95%)
            # - Wiring losses (~2%)
            # - Temperature losses (~10%)
            # - Dust/soiling (~3%)
            # - Other system losses
            performance_ratio = 0.75
            daily_production_kwh = system_capacity_kw * sunlight_hours * performance_ratio
            
            # Monthly and yearly estimates
            monthly_production_kwh = daily_production_kwh * 30
            yearly_production_kwh = daily_production_kwh * 365
            
            # Cost savings estimate (assuming ₹8 per kWh average)
            electricity_rate = 8  # ₹ per kWh
            monthly_savings = monthly_production_kwh * electricity_rate
            yearly_savings = yearly_production_kwh * electricity_rate
            
            # CO2 offset (0.82 kg CO2 per kWh for India's grid)
            co2_offset_yearly = yearly_production_kwh * 0.82  # kg CO2
            
            context = {
                'num_panels': num_panels,
                'total_electricity_production': round(daily_production_kwh, 2),
                'monthly_production': round(monthly_production_kwh, 1),
                'yearly_production': round(yearly_production_kwh, 1),
                'system_capacity': round(system_capacity_kw, 2),
                'monthly_savings': round(monthly_savings, 0),
                'yearly_savings': round(yearly_savings, 0),
                'co2_offset': round(co2_offset_yearly, 1),
                'latitude': latitude,
                'longitude': longitude,
                'hours': hours,
                'area': area,
                'usable_area': round(usable_area, 1),
                'ghi': ghi_value,
            }
            return render(request, 'index9.html', context)

        except ValueError as ve:
            return render(request, 'index9.html', {'error': str(ve)})
        except Exception as e:
            return render(request, 'index9.html', {'error': str(e)})
    else:
        return render(request, 'index9.html', {'error': 'No data received.'})
