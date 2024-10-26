# DineWise

## About
DineWise is an innovative meal-planning web application that revolutionizes the way users approach their daily meals. By leveraging the power of Gemini AI and integrating it with users' e-commerce order history, our application creates personalized meal plans tailored to each individual's preferences and available ingredients.

Many people struggle with meal planning, often leading to food waste, unhealthy eating habits, or repetitive meals. Meal Planner addresses these pain points by:
1. Automatically scanning users' e-commerce order emails to identify purchased groceries
2. Creating customized meal plans based on available ingredients
3. Offering cuisine preferences and ingredient customization options
4. Utilizing scheduler sync to ensure all user orders are accounted for

Our solution not only saves time but also reduces food waste and encourages diverse, healthy eating habits. Users can easily customize their meal plans by adding or removing ingredients based on their preferences. Additionally, DineWise allows users to select their preferred cuisines, such as Chinese, Indian, or Italian, ensuring a varied and exciting meal experience.


## System Overview
DineWise employs a modern N-tier architecture, utilizing React.js for the frontend, FastAPI for the backend, and MongoDB for data persistence. The system integrates with Gmail API for email authorization and Google's Gemini AI for intelligent meal recommendations.

## Key Features
* Secure user authentication with Gmail API integration
* Automated grocery data extraction from emails
* AI-powered meal recommendations using Gemini AI
* Weekly automated meal planning
* User preference management
* Interactive meal plan review and adjustment

## Technical Architecture
**Frontend Tier:** React.js application hosted on a dedicated frontend server

**Backend Tier:** FastAPI server handling business logic and third-party integrations

**Data Tier:** MongoDB database managing user data, preferences, and meal plans

**External Services:** Integration with Gmail API and Gemini AI

This architecture ensures scalability, maintainability, and a seamless user experience while maintaining robust security measures for handling personal data.
* Users review generated meal plans
* Options to approve or request adjustments
* Final meal plan confirmation
* Extracts grocery information from emails
* Processes user preferences
* Generates personalized meal recommendations
* Manual Path: Users can initiate meal planning on demand
* Automated Path: System generates weekly meal plans every Monday at 7 AM EST
* Secure login process
* Gmail authorization for email access


