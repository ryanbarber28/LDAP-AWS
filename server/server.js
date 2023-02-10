const fs = require('fs');
const AWS = require('aws-sdk');

const accessKeyId = 'ZVGKYFD7SX4HX02KD84X';
const secretAccessKey = 's0ABazD7PABlyU9sBVaQltay87zdnG1Q3gieiCwP';
const region = 'ca-central-1';

// Read credentials.json file
let credentials;
try {
  const data = fs.readFileSync('credentials.json');
  credentials = JSON.parse(data);
} catch (err) {
  console.log('Error reading credentials.json: ', err);
  // Set credentials to an empty object if credentials.json is not found
  credentials = {};
}

// Update AWS configuration with credentials.json
AWS.config.update({
  accessKeyId: credentials.accessKeyId || accessKeyId,
  secretAccessKey: credentials.secretAccessKey || secretAccessKey,
  region: credentials.region || region
});

const s3 = new AWS.S3({
  apiVersion: '2006-03-01'
});

s3.listBuckets(function(err, data) {
  if (err) {
    console.log('Error during authentication: ', err);
  } else {
    console.log('Authentication successful!');
    const credentials = {
      accessKeyId: accessKeyId,
      secretAccessKey: secretAccessKey,
      region: region
    };
    const credentialsJSON = JSON.stringify(credentials);
    fs.writeFile('credentials.json', credentialsJSON, (err) => {
      if (err) {
        console.log('Error writing credentials.json: ', err);
      }
    });
  }
});