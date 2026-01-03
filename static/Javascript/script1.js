var map = L.map('map').setView([18.5204, 73.8567], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
    draw: {
        polygon: true,
        polyline: false,
        rectangle: true,
        circle: false,
        marker: false
    },
    edit: {
        featureGroup: drawnItems
    }
}).addTo(map);

map.on(L.Draw.Event.CREATED, function (event) {
    var layer = event.layer;
    drawnItems.addLayer(layer);

    // Calculate area in square feet
    var area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
    var areaInSqFeet = area * 10.7639; // Convert square meters to square feet

    // Display the area in the info box
    document.getElementById('area').textContent = 'Area: ' + areaInSqFeet.toFixed(2) + ' square feet';

    // Set the value of the hidden field
    document.getElementById('area-field').value = areaInSqFeet.toFixed(2);
});

document.getElementById('prev').addEventListener('click', function () {
    alert('Previous action');
    // Implement previous functionality
});

document.getElementById('next').addEventListener('click', function () {
    alert('Next action');
    // Implement next functionality
});
