# SalesTaxHackathon
![us_tax_calc_demo_final_](https://github.com/user-attachments/assets/19591d47-f06b-45ab-b9f5-caad419aca53)



## Project Overview
This project aims to streamline the tax calculation process by utilizing machine learning to automate product type identification and tax calculations, thereby improving user experience and efficiency.

## Development Process
1. **Research and Design**: 
   - Identified model parameters and prioritized features.
   - Designed the user interface on Figma.
   
2. **Implementation**: 
   - Developed the UI, trained the text and tax calculation model.
   - Set up the database.
   - Established API endpoints for interaction.

## Data and Calculation Process
1. **Form Entry and Submission**: The user fills out a form which automatically identifies the product type.
2. **ML Product Type Identification**: Leveraging machine learning to classify products based on product name.
3. **ML Tax Calculation**: Automatically calculates the applicable tax based on identified product type.
4. **Data Storage**: Saves user input and calculation results to the database for future reference and logs history.

### Other Notes on Features
- Users do not need to enter the product type manually.
- Provides a visual map showing selected and top states for immersive user engagement.
- Enables users to view the distribution of calculations, archived for future reference.
- Offers a tax calculator *accessible as an API endpoint* or through a dedicated website.

## Challenges
- **Working with Multiple Languages**: Implemented functionalities using four different programming languages.
- **Map Integration Issues**: Faced challenges with the mapping functionalities.
- **UI Rework**: Significant adjustments made to connect the form to the map and redesign the form.
- **Usage of jQuery and AJAX**: Required to call endpoints without page refresh, adding complexity.

## Next Steps
- Develop a filtering system for improved user queries.
- Increase data and training of existing models
- Create models for local and within-state tax calculations.
- Implementation of an automated pipeline for data scraping, model retraining, and deployment.
