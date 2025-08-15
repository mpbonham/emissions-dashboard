# Household Vehicle Miles Traveled (HVMT) Regression

## Project Overview

This project explores the use of regression models to estimate **Household Vehicle Miles Traveled (HVMT)** using demographic, socioeconomic, and household characteristics. The goal is to identify key drivers of vehicle travel behavior and to assess the predictive power of various machine learning models.

The models are trained using public datasets such as:
- **National Household Travel Survey (NHTS)** data
- Household demographic and vehicle usage attributes
- Common census features (e.g., household size, income, vehicle ownership)

## Methodology

### 1. Data Preparation
- Load and clean household-level datasets from 2017 and 2022
- Select relevant features, including:
  - `HHSIZE` (Household size)
  - `NUMVEH` (Number of vehicles)
  - `HHFAMINC` (Household income)
  - `URBAN` (Urban/rural indicator)
  - `HOMEOWN`, `HOMETYPE`, `HH_RACE`, `HH_HISP`
- Join with trip-level data to calculate `HH_VMT` by summing trip miles per household

### 2. Model Training
- Train the following models using 2022 data:
  - **Linear Regression**
  - **Random Forest**
  - **XGBoost Regressor**
- Evaluate performance using 2017 data for generalization testing
- Metrics used:
  - Root Mean Squared Error (RMSE)
  - Mean Absolute Error (MAE)
  - R² Score

### 3. Feature Importance and Analysis
- Use `feature_importances_` from tree-based models
- Optionally apply permutation importance or SHAP for interpretability
- Perform residual analysis and segment analysis:
  - By income group
  - Urban vs rural
  - Number of vehicles

## Key Findings

- Tree-based models (Random Forest, XGBoost) slightly outperform linear regression in accuracy
- However, **R² scores remain low**, indicating weak predictive power overall
- Vehicle ownership and household income are among the most important predictors

## Limitations

### Data Limitations
- Many relevant behavioral variables (e.g., trip purpose, time constraints) are unavailable
- Self-reported trip data may suffer from recall bias
- `HH_VMT = 0` households are common and may be underrepresented or poorly predicted

### Model Limitations
- Predictive models do not generalize well across survey years (2017 vs 2022)
- Linear regression is overly simplistic for complex travel behavior
- Tree-based models perform better but still exhibit:
  - Poor fit at extreme ends (very low or high VMT households)
  - Overfitting risk with small sample sizes or too many features

### Structural Limitations
- HVMT is influenced by factors not present in the data:
  - Urban design and zoning
  - Access to transit
  - Gas prices or vehicle efficiency
  - Remote work trends post-COVID

## Future Directions

- Integrate geographic features (distance to jobs, walk/transit scores)
- Include time-series data to track pre- and post-COVID travel shifts
- Use clustering to define household travel profiles before regression
- Test deep learning or hybrid models incorporating spatial and temporal context

## Intended Users

- Transportation modelers
- Urban planners
- Climate analysts
- Policy researchers studying emissions or travel behavior

## Contact

This project is open for collaboration to improve model accuracy and expand datasets. Reach out if you're working on sustainable transportation modeling or behavioral travel analysis.
