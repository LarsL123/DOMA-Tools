const fs = require("fs");
const path = require("path");
const extractQuickRoute = require("./extractQuickRoute.js");

// Path to maps directory
const mapsDir = path.join(__dirname, "..", "..", "maps");
const outputFile = path.join(__dirname, "mapData.json");

function extractAllMapData() {
  const results = {};

  // Read all directories in maps folder
  const mapFolders = fs
    .readdirSync(mapsDir, { withFileTypes: true })
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);

  console.log(`Found ${mapFolders.length} map folders`);

  for (const mapId of mapFolders) {
    const mapFolder = path.join(mapsDir, mapId);

    // Look for the main image file (mapId.jpg or mapId.png)
    let imageFile = null;

    if (fs.existsSync(path.join(mapFolder, `${mapId}.jpg`))) {
      imageFile = path.join(mapFolder, `${mapId}.jpg`);
    } else if (fs.existsSync(path.join(mapFolder, `${mapId}.png`))) {
      imageFile = path.join(mapFolder, `${mapId}.png`);
    }

    if (imageFile) {
      console.log(`\n--- Processing Map ID: ${mapId} ---`);
      try {
        const data = extractQuickRoute(imageFile);

        if (data && (data.mapCorners || data.rotationDeg !== undefined)) {
          results[mapId] = {
            mapCorners: data.mapCorners,
            rotationDeg: data.rotationDeg,
          };
          console.log(`✅ Extracted data for map ${mapId}`);
        } else {
          console.log(`⚠️  No QuickRoute data found for map ${mapId}`);
          results[mapId] = null;
        }
      } catch (error) {
        console.error(`❌ Error processing map ${mapId}:`, error.message);
        results[mapId] = { error: error.message };
      }
    } else {
      console.log(`⚠️  No image file found for map ${mapId}`);
      results[mapId] = { error: "Image file not found" };
    }
  }

  // Save results to JSON file
  const jsonOutput = JSON.stringify(results, null, 2);
  fs.writeFileSync(outputFile, jsonOutput);

  console.log(`\n✅ Extraction complete!`);
  console.log(`📄 Results saved to: ${outputFile}`);
  console.log(`📊 Total maps processed: ${Object.keys(results).length}`);

  // Summary
  const successful = Object.values(results).filter(
    (r) => r && r.mapCorners
  ).length;
  const failed = Object.values(results).filter((r) => !r || r.error).length;
  console.log(`✅ Successful: ${successful}`);
  console.log(`❌ Failed/No data: ${failed}`);
}

// Run the extraction
extractAllMapData();
