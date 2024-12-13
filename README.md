# Project Title

A brief description of your project.

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.x
   - Conda
   - numpy
   - pandas
   - kagglehub
   - surprise
   - faiss_cpu
- Node.js and npm
- Git

### Installation and Setup

1. **Clone and Set Up LocalGPT Repository**
   ```bash
   git clone https://github.com/PromtEngineer/localGPT.git
   cd localGPT
   ```
   Launch the `localGPT_API` file:
   ```bash
   python localGPT_API.py
   ```

2. **Clone This Repository**
   ```bash
   git clone https://github.com/aalapsley1/IR-Project-Movie-Magic
   cd IR-Project-Movie-Magic
   ```

3. **Prepare Data**
   - Navigate to the `Recommender_System` folder:
     ```bash
     cd Recommender_System
     ```
   - Download prerequisite libraries: `pip install conda pandas kagglehub surprise faiss_cpu`
   - Run the `Data.py` script to download necessary files:
     ```bash
     python Data.py
     ```
   - Move the downloaded files to the `Recommender_System` folder. (The download location will be printed to the terminal)
      - The movie_data.csv might have an issues. If so, open the file with vscode and press "Remove Unusual Line Terminators" when prompted with "Detected unusual line terminators".

4. **Preprocess Data**
   - Return to the root repository:
     ```bash
     cd ..
     ```
   - Go to the `Website_Backend` folder:
     ```bash
     cd Website_Backend
     ```
   - Run the `preprocessing.py` file and update the static variables to point to the location of the downloaded files:
     ```bash
     python preprocessing.py
     ```
   - After creating the Faiss server, run the `prepare_metadata.py` file:
     ```bash
     python prepare_metadata.py
     ```

5. **Launch the Servers**

   - Navigate to the `Faiss_Server.py` file:
     ```bash
     cd ..
     ```
     Update the static variable paths to match your file system.
     Run this file in a unique Conda environment:
     ```bash
     conda create -n faiss_server_env python=3.x
     conda activate faiss_server_env
     python Faiss_Server.py
     ```

   - Open a new terminal and navigate to the `Recommender_System` folder:
     ```bash
     cd Recommender_System
     ```
     Run the `main.py` file in a separate Conda environment:
     ```bash
     conda create -n recommender_env python=3.x
     conda activate recommender_env
     python main.py
     ```

   - Ensure the `localGPT` Flask server is still running.

6. **Launch the Website**

   - Navigate to the `Movie_Backend/movie-magic` folder:
     ```bash
     cd ../Movie_Backend/movie-magic
     ```
   - Install dependencies:
     ```bash
     npm install
     ```
   - Build the project:
     ```bash
     npm build
     ```
   - Run the application:
     ```bash
     npm run
     ```

### Usage

Your application is now running, and you can access it via your browser. Follow any additional instructions as necessary.

### License

This project is licensed under the [LICENSE_NAME] License - see the LICENSE file for details.

