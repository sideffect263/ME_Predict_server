# ME_Predict_server

Welcome to the ME_Predict_server repository! 🎉 This project includes the backend server and machine learning algorithms used for mouse usage analysis and prediction. 🚀

## Overview

### The Machine Learning Model
The project uses a KMeans clustering model to analyze mouse movement data. The model is trained using various features extracted from the raw data to identify different usage patterns. 🧠 The data used to build the model is sourced from Kaggle.
data-source: https://www.kaggle.com/datasets/chaminduweerasinghe/stress-detection-by-keystrokeapp-mouse-changes


![image](https://github.com/sideffect263/ME_Predict_server/assets/90728515/e0559ac1-99ca-4f6b-ba24-5383c89ee162)
![image](https://github.com/sideffect263/ME_Predict_server/assets/90728515/9f4c3ee5-1b9a-4433-8350-b75f3d76c017)

#### Data Representation
X and Y axes: Represent the coordinates on the screen.
Z axis: Represents the speed of the mouse, calculated based on the change in position over time.


## Features

- **Backend Server**: Built with Node.js and Express, handling API requests and data processing. 🖥️
- **Machine Learning Models**: Implemented in Python using scikit-learn, including a KMeans clustering model. 🧠
- **Data Preprocessing**: Scalers and data transformation scripts to prepare mouse usage data for analysis. 🔄
- **RESTful API**: Endpoint for data submission and prediction retrieval. 📡

## Getting Started

#### Just Using the API
The server exposes an endpoint for interacting with the machine learning model and retrieving predictions.

POST /predict: Submit mouse usage data for prediction. The API expects x, y, and speed in the request body and returns the predicted cluster and user condition along with UI suggestions.

server: https://me-predict-server.onrender.com/

### going for production

### Prerequisites

Ensure you have the following installed:
- Node.js
- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/sideffect263/ME_Predict_server.git
    cd ME_Predict_server
    ```

2. **Install Node.js dependencies**:
    ```bash
    npm install
    ```

3. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

To run the backend server, use the following command:
```bash
node server.js
