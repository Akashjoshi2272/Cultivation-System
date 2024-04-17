// Initialize the map
var map = L.map('map').setView([13.3318053, 74.7058913], 9);

// Add a tile layer (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
    maxZoom: 18
}).addTo(map);

// Load the JSON file
fetch('static/js/markers.json')
    .then(response => response.json())
    .then(data => {
        // Update the markers based on the current slider values
        function updateMarkers() {
            // Read the values of the filter inputs
            var nitrogen = document.getElementById('nitrogen').value;
            var phosphorous = document.getElementById('phosphorous').value;
            var pottasium = document.getElementById('pottasium').value;

            // Remove existing markers from the map
            map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });

            // Loop through the data and add filtered markers based on condition
            data.features.forEach(marker => {
                // Filter markers based on condition
                if (
                    marker.properties["N(kg/h)"] >= nitrogen &&
                    marker.properties["P(kg/h)"] >= phosphorous &&
                    marker.properties["K(kg/h)"] >= pottasium
                ) {
                    // Create the marker and add it to the map
                    var newMarker = L.marker([marker.geometry.coordinates[1], marker.geometry.coordinates[0]]).addTo(map);
                    
                    // Attach click event to the marker
                    newMarker.on('click', function(e) {
                        // Send marker data to Flask backend
                        fetch('/process_marker_data', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(marker.properties)
                        })
                        .then(response => {
                            if (response.ok) {
                                console.log('Marker data sent successfully');
                            } else {
                                console.error('Failed to send marker data:', response.statusText);
                            }
                        })
                        .catch(error => {
                            console.error('Error sending marker data:', error);
                        });
                    });
                }
            });
        }

        // Call updateMarkers initially and whenever a slider changes
        updateMarkers();
        document.getElementById('nitrogen').addEventListener('input', updateMarkers);
        document.getElementById('phosphorous').addEventListener('input', updateMarkers);
        document.getElementById('pottasium').addEventListener('input', updateMarkers);
    });
