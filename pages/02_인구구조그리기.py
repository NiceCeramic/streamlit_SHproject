import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# Load data
data_path = 'age2411.csv'  # Ensure this file is in the same directory or update the path
data = pd.read_csv(data_path)

# Clean data: Extract only the necessary columns
population_data = data.copy()
population_data['행정구역'] = population_data['행정구역'].str.split('(').str[0]  # Simplify 지역명

# Streamlit app
def main():
    st.title("우리 동네 인구 구조 알아보기")

    # User input for region
    region = st.text_input("지역명을 입력하세요 (예: 서울특별시 종로구):")

    if region:
        # Filter data for the selected region
        filtered_data = population_data[population_data['행정구역'].str.contains(region)]

        if not filtered_data.empty:
            # Prepare data for plotting
            age_columns = [col for col in filtered_data.columns if '2024년11월_계_' in col and '총인구수' not in col]
            age_data = filtered_data.iloc[0][age_columns]

            # Convert to numeric if necessary
            age_data = pd.to_numeric(age_data, errors='coerce')

            # Check if age_data is valid
            if age_data.isnull().all():
                st.error("선택한 지역에 대한 유효한 연령 데이터가 없습니다.")
                return

            # Extract age range
            age_labels = [col.replace('2024년11월_계_', '').replace('세', '') for col in age_columns]

            # Debugging output for validation
            st.write("### Debugging Info")
            st.write("Age Data:", age_data)
            st.write("Age Labels:", age_labels)

            # Plot
            plt.figure(figsize=(10, 6))
            plt.bar(age_labels, age_data, color='skyblue')
            plt.title(f"{region}의 인구 구조", fontsize=16)
            plt.xlabel("나이", fontsize=12)
            plt.ylabel("인구수", fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Display plot
            st.pyplot(plt)

            # Add additional insights
            max_age_label = age_labels[age_data.idxmax()]
            min_age_label = age_labels[age_data.idxmin()]
            st.write(f"### {region}의 인구 구조")
            st.write("- 가장 많은 연령대: ", max_age_label)
            st.write("- 가장 적은 연령대: ", min_age_label)
        else:
            st.error("입력한 지역명을 찾을 수 없습니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
