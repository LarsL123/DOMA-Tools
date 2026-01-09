const fs = require("fs");
const path = require("path");

// Input and output paths
const inputFile = path.join(__dirname, "mapData.json");
const outputFile = path.join(__dirname, "mapCenters.json");
const outputArrayFile = path.join(__dirname, "mapCentersArray.js");

function calculateCenter(mapCorners) {
  if (!mapCorners || mapCorners.length !== 4) {
    return null;
  }

  // Calculate average latitude and longitude
  let totalLat = 0;
  let totalLon = 0;

  for (const corner of mapCorners) {
    totalLat += corner.lat;
    totalLon += corner.lon;
  }

  return {
    lat: totalLat / 4,
    lon: totalLon / 4
  };
}

function processMaps() {
  // Read the map data
  const mapData = JSON.parse(fs.readFileSync(inputFile, "utf8"));

  const mapCenters = {};
  const mapCentersArray = [];

  // Process each map
  for (const [mapId, data] of Object.entries(mapData)) {
    if (data && data.mapCorners) {
      const center = calculateCenter(data.mapCorners);

      if (center) {
        mapCenters[mapId] = center;

        // Also add to array with mapId
        mapCentersArray.push({
          mapId: mapId,
          lat: center.lat,
          lon: center.lon
        });
      }
    }
  }

  // Save as JSON object
  fs.writeFileSync(outputFile, JSON.stringify(mapCenters, null, 2));

  // Save as JavaScript array for easy copying
  const jsContent = `// Map Centers Array - Ready to copy
const mapCenters = ${JSON.stringify(mapCentersArray, null, 2)};

module.exports = mapCenters;
`;

  fs.writeFileSync(outputArrayFile, jsContent);

  console.log(`✅ Processing complete!`);
  console.log(`📄 JSON object saved to: ${outputFile}`);
  console.log(`📄 JavaScript array saved to: ${outputArrayFile}`);
  console.log(`📊 Total maps with centers: ${mapCentersArray.length}`);
}

// Run the processing
processMaps();
