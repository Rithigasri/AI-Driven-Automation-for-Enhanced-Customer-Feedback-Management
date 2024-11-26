# AI-Driven Automation for Enhanced Customer Feedback Management

## Objective:
Develop an integrated AI and automation solution to analyze customer review sentiment, flag negative feedback, and initiate follow-up actions. This proof of concept (POC) combines AI-driven sentiment analysis with automated task management and response workflows to enhance the customer experience by streamlining feedback handling and ensuring timely, personalized follow-ups for critical reviews.

## Tools Used:
- **Flask:** Backend for managing annotation processes in Label Studio.
- **Label Studio:** Tool for annotating mobile review data.
- **Zapier:** Automates workflows for data transfer to Excel, sending emails, and integration with Monday.com.
- **Gemini API:** Used to develop and train a machine learning model for generating responses to negative comments.
- **Monday.com:** Task management system for tracking and managing tasks.
- **Excel:** For structured data storage and reporting.

## Architecture Diagram:
![Updated-POC](https://github.com/user-attachments/assets/0999f8f7-2a8b-4817-bc9c-3d491c2a80f1)

## Features:
1. **Sentiment-Based Responses:**
   - **Positive Comments:** Acknowledged with gratitude.
   - **Negative Comments:** Addressed with assurances of follow-up actions.
   - **Neutral Comments:** Receives polite and professional responses.
   
2. **Dynamic Response Generation:**
   - Automatically generates responses for negative comments with minimal manual intervention.
   - Supports tone adjustments and sentiment-driven responses.

3. **Data Processing and Output:**
   - Processes customer feedback stored in CSV files.
   - Outputs the generated responses into new CSV files for easy tracking.

## System Design:

### **1. Data Collection**
- **Objective:** Gather raw mobile reviews from various platforms.
- **Tools Used:**
  - **Python Libraries:** BeautifulSoup, Scrapy
  - **Third-party Services:** Octoparse, ScrapingBee

### **2. Preprocessing and Annotation**
- **Objective:** Clean and annotate reviews for sentiment analysis.
- **Process:**
  - **Data Preprocessing:** 
    - Remove irrelevant content (e.g., special characters, HTML tags).
  - **Annotation:** 
    - Label reviews as positive, neutral, or negative.
- **Tools Used:**
  - **Label Studio:** For review annotation.
  - **Flask:** To create an API interface for easy integration with Label Studio.

### **3. Data Storage**
- **Objective:** Store the annotated dataset for further processing.
- **Process:**
  - Save the annotated data in Excel files.
  - Automate the saving process to Excel using integration tools.
- **Tools Used:**
  - **Zapier:** For automation (saving data to Excel).
  - **Excel:** For data storage.

### **4. Machine Learning Model**
- **Objective:** Train a model to analyze and respond to negative reviews.
- **Process:**
  - **Model Training:** Train the model using the annotated dataset.
  - **Response Generation:** Analyze negative comments and generate tailored responses.
- **Tools Used:**
  - **Gemini API** (or another ML service): For model training and response generation.
  - **Python:** For data manipulation and API interaction.

### **5. Email Automation**
- **Objective:** Automate the process of sending responses to negative reviews.
- **Process:**
  - Once a negative review is flagged, an initial response email is sent.
  - Email content can be customized with predefined templates for different types of negative feedback.
- **Tools Used:**
  - **Zapier:** For automation (sending emails).
  - **Email Service (e.g., Gmail):** For sending response emails.

### **6. Task Management**
- **Objective:** Create and manage follow-up tasks for negative reviews.
- **Process:**
  - Create tasks in Monday.com for follow-up actions.
  - Update task statuses (e.g., "In Progress," "Resolved").
  - Export task updates back to Excel for tracking.
- **Tools Used:**
  - **Monday.com:** For task management.
  - **Zapier:** For task and status automation.

### **7. Reporting**
- **Objective:** Generate a final report on task statuses and review cycle outcomes.
- **Process:**
  - Compile final task statuses into a report.
  - Save the report for internal review.
- **Tools Used:**
  - **Excel:** For report generation.
  - **Zapier:** For exporting task status updates.
