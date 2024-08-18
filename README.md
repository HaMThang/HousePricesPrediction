# Using Machine Learning Regression Algorithms to Predict House Prices in Vietnam

This repository contains the code and resources for a comprehensive study on house price prediction in Vietnam using machine learning techniques. The study aims to develop an accurate and reliable framework for predicting house prices, leveraging a diverse dataset sourced from alonhadat.com.vn and supplemented with data from Wikipedia.
## Abstract
Accurate house price prediction is crucial for stakeholders in the real estate market, yet it remains challenging due to the market's inherent complexity and dynamism. This study addresses this issue by developing a comprehensive machine learning framework for house price prediction in Vietnam. We leverage a robust dataset of 28,156 property listings, sourced from alonhadat.com.vn and supplemented with data from Wikipedia. Through rigorous data preprocessing, feature engineering, and a comparative analysis of state-of-the-art machine learning algorithms, including CatBoost, XGBoost, and Random Forest, we identify the most effective techniques for predicting house prices.
The results demonstrate the superiority of ensemble methods, with CatBoost achieving the highest performance on the main dataset (R² = 0.510, RMSE = 17.614). Regional analyses in Hanoi and Ho Chi Minh City reveal the adaptability of the models to local market dynamics, with XGBoost and Random Forest exhibiting the best performance, respectively. Furthermore, we employ SHAP (SHapley Additive exPlanations) to uncover the key drivers of house prices, such as area, population density, and property-specific attributes.
The findings not only contribute to the academic understanding of real estate valuation but also provide actionable insights for policymakers, investors, and other stakeholders. This study lays the groundwork for the development of automated valuation models (AVMs) and their practical implementation, exemplified by a web application (https://hathang-housepricceprediction.hf.space/). By harnessing the power of machine learning and data-driven insights, this research paves the way for more transparent, efficient, and informed decision-making in Vietnam's real estate sector.
## Repository Structure
data/: Contains the dataset used in the study, including property listings and supplementary data.


models/: Trained machine learning models and their respective configurations.

src/: Source code for data preprocessing, feature engineering, model training, and evaluation.

web_app/: Code and resources for the web application that demonstrates the practical implementation of the house price prediction framework.

README.md: Overview of the project and instructions for running the code.

requirements.txt: List of required Python packages and their versions.

## Installation
Clone the repository:
Copy
git clone https://github.com/your-username/house-price-prediction-vietnam.git

Install the required packages:
Copy
pip install -r requirements.txt


## Usage
Run the Jupyter notebooks in the notebooks/ directory to understand the data preprocessing, exploratory data analysis, feature engineering, and model development process.
Use the trained models in the models/ directory to make house price predictions on new data.
Explore the web application code in the web_app/ directory to see how the house price prediction framework can be deployed as a practical tool.

## Web Application
A live demo of the house price prediction web application is available at: https://hathang-housepricceprediction.hf.space/
Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for more information.
Contact
For any questions or inquiries, please contact [your-email@example.com].
Feel free to customize the content based on your specific project details and requirements. This README.md template provides an overview of your study, the repository structure, installation instructions, usage guidelines, information about the web application, and other relevant details for people who visit your GitHub repository


*Note: Some links leading to files need to be fixed.
