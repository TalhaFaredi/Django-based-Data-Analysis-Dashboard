# CAPS - Cricket Analysis and Prediction System  

CAPS (Cricket Analysis and Prediction System) is an AI-powered Django-based platform designed to offer deep insights into cricket matches, team performances, and player statistics. It incorporates advanced machine learning models to analyze critical game moments and provide predictions, creating a one-stop solution for cricket enthusiasts, analysts, and players.

---

## Features  

### **Cricket Data Analysis**  
1. **All Teams Performance Analysis**:  
   Analyze the overall performance of all cricket teams with historical and real-time data.  
2. **Team vs Team Analysis**:  
   Compare performance metrics between two selected teams.  
3. **Team vs Team at Venue**:  
   Gain insights into how teams perform against each other at specific venues.  

### **AI-Powered Models**  
1. **Runout Detection**:  
   A **Convolutional Neural Network (CNN)** model is used to classify cricket match images into `runout` and `not runout`.  
2. **Match Prediction**:  
   A **Decision Tree** model predicts match outcomes based on historical and real-time data.  

### **Interactive Interface**  
- Django-powered dynamic dashboards for team and match analysis.  
- Easy-to-use forms for data input and model predictions.  

---

## Technology Stack  

### **Backend**  
- Django (Python)  
- SQLite  

### **Frontend**  
- HTML, CSS, Bootstrap, JavaScript  

### **Machine Learning Models**  
- **CNN**: For runout image classification.  
- **Decision Tree**: For match outcome predictions.  

### **Visualization**  
- Matplotlib, Seaborn  

---

## Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/CAPS.git  
   cd CAPS  
   ```  

2. Create and activate a virtual environment:  
   ```bash  
   python -m venv env  
   source env/bin/activate  # On Windows: .\env\Scripts\activate  
   ```  

3. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. Run database migrations:  
   ```bash  
   python manage.py makemigrations  
   python manage.py migrate  
   ```  

5. Train the models (optional):  
   - Place the dataset for runout detection in the `datasets/runout/` folder.  
   - Run the CNN training script:  
     ```bash  
     python models/cnn_train.py  
     ```  
   - Prepare the dataset for match predictions in `datasets/predictions/`.  
   - Run the Decision Tree training script:  
     ```bash  
     python models/dt_train.py  
     ```  

6. Start the Django development server:  
   ```bash  
   python manage.py runserver  
   ```  

7. Open the application in your browser:  
   ```
   http://127.0.0.1:8000  
   ```  

---

## Usage  

### Dashboard Features  
- **Team Analysis**: Select a team to view detailed performance metrics.  
- **Match Comparison**: Compare teams and venues to identify key patterns.  
- **Prediction**: Upload match data for predictive analysis.  
- **Runout Detection**: Upload cricket images to classify them as `runout` or `not runout`.  

---

## Folder Structure  

```plaintext  
CAPS/  
├── analysis/           # Django app for data analysis  
├── models/             # Machine learning models  
├── datasets/           # Training datasets  
├── static/             # CSS, JavaScript, images  
├── templates/          # HTML templates  
├── manage.py           # Django management script  
├── requirements.txt    # Dependencies  
├── README.md           # Project documentation  
```  

---

## Future Plans  

- Integrate more advanced models for player performance prediction.  
- Extend analysis to include player-specific performance comparisons.  
- Add live match tracking and real-time predictions.  
- Mobile and API support for broader accessibility.  

---

## Contributing  

Contributions are welcome! Fork the repository and submit a pull request with your enhancements.  

---
## User Interface 
![image](https://github.com/user-attachments/assets/42229fb2-969a-4e9c-b49d-f48d860c9a1d)
![image](https://github.com/user-attachments/assets/49d8e4cc-af84-439c-8578-19416749ddbe)
![image](https://github.com/user-attachments/assets/2488231c-e00e-4eb5-86e8-99f7e02eaf9a)
![image](https://github.com/user-attachments/assets/f0c55c87-ed7b-4afd-8e50-1305f48e76a9)





## License  

This project is licensed under the [MIT License](LICENSE).  

---

## Contact  

For questions or collaboration opportunities, contact:  

- **Author**: Talha Fareedi  
- **Email**: talhafareedi092@gmail.com  

**CAPS** - Elevate Cricket Analysis with AI! 🏏  
