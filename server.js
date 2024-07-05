const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const app = express();
var cors = require('cors')

app.use(cors()) // Use this after the variable declaration
app.use(bodyParser.json());

function predict(x, y, speed) {
    console.log('in preidct');
    return new Promise((resolve, reject) => {
        console.log('x:', x, 'y:', y, 'speed:', speed);
      const python = spawn('python', ['predict.py', x, y, speed]);
      
      let result = '';
      let errorOutput = '';
  
      python.stdout.on('data', (data) => {
        let tempString = data.toString();
        console.log('tempString:', tempString);
        result += tempString;
      
      });
  
      python.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });
      
      python.on('close', (code) => {
        if (code !== 0) {
          console.error(`Python stderr: ${errorOutput}`);
          reject(`Python script exited with code ${code}`);
        } else {
            console.log('result:', result);
          resolve(JSON.parse(result));
        }
      });
    });
  }

function getUserCondition(cluster) {
    switch(parseInt(cluster)) {
        case 0: return 'relaxed';
        case 1: return 'anxious';
        case 2: return 'sleepy';
        case 3: return 'anxious';
        default: return 'unknown';
    }
}

app.get('/', (req, res) => {
    res.send('Hello World!');
    console.log('user connected');
}
);

app.post('/predict', async (req, res) => {
    console.log('predicting...');
    const { x, y, speed } = req.body;
    try {
        console.log('in try');
        const { cluster } = await predict(x, y, speed);
        console.log('cluster:', cluster);
        const condition = getUserCondition(cluster);

        res.json({
            cluster,
            condition,
            uiSuggestions: getUISuggestions(condition)
        });
    } catch (error) {
        console.log('error:', error);
        res.status(500).json({ error: error.toString() });
    }
});


function getUISuggestions(condition) {
    switch(condition) {
        case 'relaxed':
            return {
                fontSize: 'larger',
                spacing: 'increased',
                animation: 'minimal'
            };
        case 'sleepy':
            return {
                interactiveElements: 'increased',
                contentSuggestions: true,
                navigation: 'prominent'
            };
        case 'relaxed':
            return {
                distractions: 'minimized',
                focusArea: 'highlighted',
                notifications: 'suppressed'
            };
        case 'anxious':
            return {
                layout: 'simplified',
                helpPrompts: true,
                guidedExperience: true
            };
        default:
            return {};
    }
}


const port = process.env.PORT || 3001; // Fallback to 3000 if process.env.PORT is not defined
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});