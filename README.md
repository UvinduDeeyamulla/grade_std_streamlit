# grade_std_streamlit
A grade standardization application
Student Marks Normalization with Grading
This Streamlit app allows you to upload a CSV or Excel file containing student marks, normalize the marks based on a selected target mean, and generate an updated dataset with adjusted marks and grades. The app also displays various visualizations, including grade distributions before and after normalization.

Features
Upload CSV or Excel files with student marks.
Display a preview of the dataset and basic statistics.
Normalize student marks to a user-specified target mean.
Adjust marks while preserving their relative positions.
Generate and display grade distributions before and after normalization.
Show pass percentages before and after normalization.
Provide visualizations of the original and adjusted marks distributions.
Download the adjusted data with grades in Excel format.
Requirements
This app requires the following Python packages:

streamlit
pandas
matplotlib
seaborn
io
To install the required packages, you can use the following:

bash
Copy
Edit
pip install streamlit pandas matplotlib seaborn
Usage
Clone or download this repository to your local machine.
Install the necessary dependencies using pip.
Run the app using the following command:
bash
Copy
Edit
streamlit run app.py
Upload your CSV or Excel file containing student marks.
Adjust the normalization settings in the sidebar, such as the desired target mean for the marks.
View the dataset preview, grade distribution, and other statistics before and after normalization.
Download the updated dataset with adjusted marks and grades as an Excel file.
File Structure
bash
Copy
Edit
/
│
├── app.py                    # Main Streamlit app file
└── requirements.txt           # List of dependencies
Contributing
Contributions to this project are welcome! If you'd like to improve the app, fix bugs, or add new features, feel free to open a pull request.

License
This project is open source and available under the MIT License.
