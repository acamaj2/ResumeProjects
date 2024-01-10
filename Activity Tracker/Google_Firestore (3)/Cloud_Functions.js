//SensorStore ----------------------------------
// Import the Firestore module
const Firestore = require('@google-cloud/firestore'); 

// Connect to the Firestore database  
const db = new Firestore({ 
  projectId: '<YOUR-PROJECT-ID>', 
  keyFilename: 'key.json' 
}); 

// Cloud Function entry point 
exports.storeData = async (req, res) => { 
  // Read and validate incoming sensor data message 
  const messageData = req.body; 

  if (messageData === undefined || messageData === null) { 
    console.error('Unable to read message'); 
    res.status(400).send(); 
    return; 
  } 

  // Insert the data into the database 
  const timestamp = Date.now() 

  await db.collection('sensor-data').add({ 
    timestamp, 
    ...messageData
  }); 

  // Return a successful result 
  res.status(200).send(); 
}; 



//Retrieve Sensor Data-------------------------------------------------------------
// Import the Firestore module
const Firestore = require('@google-cloud/firestore');

// Connect to the Firestore database. 
const db = new Firestore({ 
  projectId: '<YOUR-PROJECT-ID>', 
  keyFilename: 'key.json' 
}); 

exports.getData = async (req, res) => { 
  // Permit cross-site invocation. 
  res.set('Access-Control-Allow-Origin', '*'); 

  if (req.method === 'OPTIONS') { 
    // Settings for cross-site invocation. 
    res.set('Access-Control-Allow-Methods', 'GET'); 
    res.set('Access-Control-Allow-Headers', 'Content-Type'); 
    res.set('Access-Control-Max-Age', '3600'); 
    res.status(204).send(''); 
  } else { 
    // Retrieve sensor data from the DB. 
    const coll = db.collection('sensor-data'); 
    const sensorDataSnapshot = await coll
        .orderBy('timestamp')
        .limit(10)
        .get(); 
    const sensorData = sensorDataSnapshot.docs.map(doc => doc.data()); 

    // Return the activity data as a JSON object. 
    res.json(sensorData); 
  } 
};



