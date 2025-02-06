import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Streamlit App Title
st.title("📊Student Marks Normalization with Grading")

# Sidebar File Upload and Controls
st.sidebar.header("Upload Your CSV/Excel File")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read file based on extension
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            st.stop()

        # Display Dataset Preview
        st.write("### 📜 Data Preview (Before Normalization)")
        st.dataframe(df.head())

        # Show Basic Statistics
        st.write("### 📈 Basic Statistics (Before Normalization)")
        st.write(df.describe())

        # Normalization Section
        st.write("### 🎯 Normalize Marks for All Students")

        # Select a column for normalization
        num_columns = df.select_dtypes(include=["int64", "float64"]).columns
        if not num_columns.empty:
            # Move column selection to sidebar
            st.sidebar.header("Adjustment Controls")
            marks_column = st.sidebar.selectbox("Select Marks Column", num_columns)

            # Compute Original Mean and Standard Deviation
            original_mean = df[marks_column].mean()
            original_std = df[marks_column].std()

            # Add slider for target mean in sidebar
            target_mean = st.sidebar.slider(
                "Select desired population mean",
                min_value=float(max(0, original_mean - 20)),
                max_value=float(min(100, original_mean + 20)),
                value=float(original_mean),
                step=0.5
            )

            st.write(f"📌 **Original Mean of {marks_column}:** {original_mean:.2f}")
            st.write(f"📌 **Target Mean:** {target_mean:.2f}")
            st.write(f"📌 **Standard Deviation of {marks_column}:** {original_std:.2f}")

            # Rest of the code remains the same...
            def assign_grade(score):
                if 85 <= score <= 100:
                    return "A+"
                elif 70 <= score < 85:
                    return "A"
                elif 65 <= score < 70:
                    return "A-"
                elif 60 <= score < 65:
                    return "B+"
                elif 55 <= score < 60:
                    return "B"
                elif 50 <= score < 55:
                    return "B-"
                elif 45 <= score < 50:
                    return "C+"
                elif 40 <= score < 45:
                    return "C"
                elif 35 <= score < 40:
                    return "C-"
                elif 30 <= score < 35:
                    return "D+"
                elif 25 <= score < 30:
                    return "D"
                else:
                    return "E"

            df["Grade Before Normalization"] = df[marks_column].apply(assign_grade)

            # Calculate Grade Distribution Before Normalization
            grade_counts_before = df["Grade Before Normalization"].value_counts().sort_index()
            
            # Display Grade Distribution Before Normalization
            st.write("### 📊 Grade Distribution (Before Normalization)")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Grade Counts:")
                st.write(pd.DataFrame({
                    'Grade': grade_counts_before.index,
                    'Count': grade_counts_before.values,
                    'Percentage': (grade_counts_before.values / len(df) * 100).round(2)
                }))
            
            with col2:
                plt.figure(figsize=(8, 6))
                grade_counts_before.plot(kind='bar')
                plt.title('Grade Distribution Before Normalization')
                plt.xlabel('Grade')
                plt.ylabel('Count')
                st.pyplot(plt)

            # Calculate Pass Percentage Before Normalization
            pass_grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C"]
            pass_count_before = df[df["Grade Before Normalization"].isin(pass_grades)].shape[0]
            total_students = df.shape[0]
            pass_percentage_before = (pass_count_before / total_students) * 100

            st.write(f"📊 **Pass Percentage (Before Normalization):** {pass_percentage_before:.2f}%")

            # Adjust marks to new mean while preserving relative positions
            mean_difference = target_mean - original_mean
            df["Adjusted Marks"] = df[marks_column] + mean_difference

            # Ensure marks stay within 0-100 range
            df["Adjusted Marks"] = df["Adjusted Marks"].clip(0, 100)

            # Assign Grades After Adjustment
            df["Grade After Adjustment"] = df["Adjusted Marks"].apply(assign_grade)

            # Calculate Grade Distribution After Adjustment
            grade_counts_after = df["Grade After Adjustment"].value_counts().sort_index()
            
            # Display Grade Distribution After Adjustment
            st.write("### 📊 Grade Distribution (After Adjustment)")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Grade Counts:")
                st.write(pd.DataFrame({
                    'Grade': grade_counts_after.index,
                    'Count': grade_counts_after.values,
                    'Percentage': (grade_counts_after.values / len(df) * 100).round(2)
                }))
            
            with col2:
                plt.figure(figsize=(8, 6))
                grade_counts_after.plot(kind='bar')
                plt.title('Grade Distribution After Adjustment')
                plt.xlabel('Grade')
                plt.ylabel('Count')
                st.pyplot(plt)

            # Calculate Pass Percentage After Adjustment
            pass_count_after = df[df["Grade After Adjustment"].isin(pass_grades)].shape[0]
            pass_percentage_after = (pass_count_after / total_students) * 100

            st.write(f"📊 **Pass Percentage (After Adjustment):** {pass_percentage_after:.2f}%")

            # Display the updated dataset with adjusted marks and grades
            st.write("### 📜 Updated Data with Adjusted Marks and Grades")
            st.dataframe(df[[marks_column, "Grade Before Normalization", "Adjusted Marks", "Grade After Adjustment"]].head())

            # Plot the adjusted data distribution
            st.write("### 📊 Adjusted Data Distribution")
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            sns.histplot(data=df[marks_column], kde=True, bins=20, ax=ax1)
            ax1.set_title('Original Distribution')
            ax1.set_xlabel('Marks')
            
            sns.histplot(data=df["Adjusted Marks"], kde=True, bins=20, ax=ax2)
            ax2.set_title('Adjusted Distribution')
            ax2.set_xlabel('Marks')
            
            st.pyplot(fig)

            # Compare grade distributions
            st.write("### 📊 Grade Distribution Comparison")
            comparison_df = pd.DataFrame({
                'Before Adjustment': grade_counts_before,
                'After Adjustment': grade_counts_after
            }).fillna(0)
            
            plt.figure(figsize=(10, 6))
            comparison_df.plot(kind='bar')
            plt.title('Grade Distribution Comparison')
            plt.xlabel('Grade')
            plt.ylabel('Count')
            plt.legend(title='')
            st.pyplot(plt)

            # Export Data
            st.write("### 📤 Download Processed Data")

            def convert_df_to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Adjusted Data with Grades")
                processed_data = output.getvalue()
                return processed_data

            st.download_button(
                label="📥 Download as Excel",
                data=convert_df_to_excel(df),
                file_name="adjusted_data_with_grades.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    except Exception as e:
        st.error(f"Error loading file: {e}")

else:
    st.info("Please upload a file to proceed.")