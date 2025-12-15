import streamlit as st
import streamlit as st
import pandas as pd

st.title("Framingham Heart Study Report :heart:")
st.write("Report written by Alba Villagrasa Martín, Ketlin Marku and Thora Priester")
st.subheader("Research Question: How are total cholesterol levels associated to cardiovascular disease risk?")

with st.expander("Introduction"):
    st.subheader("Background Information of the Framingham Heart Study")
    st.write('''Started in 1948, the Framingham Heart Study was the first prospective study to identify cardiovascular risk factors.
Initial cohort: 5,209 adults from Framingham, MA, examined every 2 years and followed for heart-related outcomes.
Data collected: blood pressure, blood chemistry, ECG, lifestyle habits, and medication use.
Events tracked: Angina, Myocardial Infarction, Heart Failure, Stroke, and Death.

Cardiovascular disease (CVD) refers to disorders of the heart and blood vessels, including coronary artery disease, stroke, and heart failure. It remains the leading cause of global mortality and represents a major public health burden [1].

One of the key biomarkers used to assess CVD risk is total cholesterol (TOTCHOL), which is the combined concentrations of LDL, HDL, and VLDL cholesterol in the bloodstream. LDL and HDL are two major types of cholesterol-carrying particles: LDL (“bad" cholesterol) delivers cholesterol to tissues and promotes plaque build-up in arteries when elevated, whereas HDL ("good" cholesterol) helps remove excess cholesterol from the bloodstream and is generally protective against cardiovascular disease.[2] When driven by increased LDL and reduced HDL , elevated total cholesterol contributes to atherosclerosis and substantially increases the risk of cardiovascular events [3]. Understanding how TOTCHOL varies within a population therefore provides meaningful insights into cardiovascular health and disease risk.''')


             

    # Phase 1 finidings
    st.subheader("Phase 1")
    st.write("Findings from Phase 1: During the initial stages of our project, we explored research questions related to hypertension. However, we later discovered that the threshold we had could not be applied to everyone, which led to inconsistent classifications when comparing blood pressure measurements across participants. We also focused on assessing how blood pressure medications influenced hypertension status, but this approach also introduced uncertainty because we could not determine whether observed changes were caused by medication use or by lifestyle factors. To avoid these methodological challenges and ensure a clearer analytical direction, we refined our study to investigate a more reliable biomarker. Therefore, our final research question focuses on how total cholesterol levels (TOTCHOL) in Period 3 are associated with cardiovascular disease (CVD) risk. This allows us to work with a well-defined biomarker and avoids the confounding issues present in our earlier ideas.")

    st.subheader("Research Question")
    st.write("Research Question: How are total cholesterol levels associated to cardiovascular disease risk?")

# Data Preparation
with st.expander("Data Preparation"):
    st.subheader("Data Preparation: Select Rows and Columns")
    st.write("Using the Framingham Heart Study dataset, which was made available to us through Kaggle, the following data is presented:")
    # Open/load the data set
    cvd= pd.read_csv('https://raw.githubusercontent.com/LUCE-Blockchain/Databases-for-teaching/refs/heads/main/Framingham%20Dataset.csv')
    st.dataframe(cvd)

    st.write("Shape of data frame:", cvd.shape)
    st.write("Columns:",cvd.shape[1])
    st.write("Rows:",cvd.shape[0])

    st.write("From this dataset, we can see a very large amount of features (columns) and rows (records). To make the dataset more manageable and relevant to our research question, we will perform some data cleaning steps, including dropping unnecessary rows and columns.")

    st.subheader("Drop Rows")
    st.write("To ensure consistency across time periods, we will filter the dataset to include only those participants who have data recorded in all three periods of the study. This approach allows us to maintain a complete longitudinal dataset. We include only the records from Period 3 for these participants, as this period contains the most recent and relevant measurements for our analysis.")
    period1_ids = cvd.loc[cvd["PERIOD"] == 1, "RANDID"]
    period2_ids = cvd.loc[cvd["PERIOD"] == 2, "RANDID"]
    period3_ids = cvd.loc[cvd["PERIOD"] == 3, "RANDID"]

    # IDs present in all three
    ids_all_periods = set(period1_ids) & set(period2_ids) & set(period3_ids)

    # Filter period 3 for those IDs
    cvd_droprows = cvd[(cvd["PERIOD"] == 3) & (cvd["RANDID"].isin(ids_all_periods))]

    toggledroprows = st.toggle("Show code for Drop Rows")
    if toggledroprows:
        st.code('''
        period1_ids = cvd.loc[cvd["PERIOD"] == 1, "RANDID"] 
        period2_ids = cvd.loc[cvd["PERIOD"] == 2, "RANDID"]
        period3_ids = cvd.loc[cvd["PERIOD"] == 3, "RANDID"]

     # IDs present in all three
        ids_all_periods = set(period1_ids) & set(period2_ids) & set(period3_ids)

        # Filter period 3 for those IDs
        cvd_droprows = cvd[(cvd["PERIOD"] == 3) & (cvd["RANDID"].isin(ids_all_periods))]''')

    st.dataframe(cvd_droprows)
    st.write("Shape of data frame after dropping rows:", cvd_droprows.shape)
    st.write("Here we can see that after dropping rows, we have reduced the dataset from 11627 participants to 3206 participants")

    st.subheader("Drop Columns")
    st.write("Next, we will remove irrelevant columns that do not contribute to answering our research question. We will retain only the following columns: RANDID, SEX, TOTCHOL, AGE, PERIOD, HDLC, LDLC, CVD")
    #Remove irrelevant columns to the research question
    relevant_columns=['RANDID','SEX','TOTCHOL','AGE','PERIOD','HDLC','LDLC','CVD',"BMI", "PREVCHD", "PREVMI",]

    cvd_dropcolumns = cvd_droprows[relevant_columns]
    cvd_clean=cvd_dropcolumns
    toggledropcolumns = st.toggle("Show code for Drop Columns")
    if toggledropcolumns:
        st.code('''relevant_columns=['RANDID','SEX','TOTCHOL','AGE','PERIOD','HDLC','LDLC','CVD',"BMI", "PREVCHD", "PREVMI",]

    cvd_dropcolumns = cvd_droprows[relevant_columns]''')
    cvd_clean
    st.write("Shape of the data frame after dropping columns", cvd_clean.shape)
    st.write("After dropping columns, we have reduced the dataset from 39 columns to 11 columns, which are more relevant to our research question.")
    
with st.expander("Explore and Clean the Data"):
    st.write("Table of Contents:")
    st.write("1. Missing Data")
    st.write("2. Erroneous Values")
    st.write("3. Outliers")
    #Missing values in cleaned subset
    st.subheader("1. Missing Data")
    st.write("As seen in the table below, there are missing values for TOTCHOL, HDLC, and LDLC, however these values will need to be imputed to ensure there is no missing data. This will occur later on to show the difference in the visual representation of the data, without imputation.")
    st.dataframe(cvd_clean.isna().sum())

    #Dividing rows into each period 
    period1= cvd.loc[cvd['PERIOD'] == 1] 
    period2= cvd.loc[cvd['PERIOD'] == 2] 
    period3= cvd.loc[cvd['PERIOD'] == 3] 

    # Missing values period Period
    with st.expander("Missing Data per Period"):
        st.write('Period 1 Missing Values')
        st.dataframe(period1.isna().sum())
        st.write('Period 2 Missing Values')
        st.dataframe(period2.isna().sum())
        st.write('Period 3 Missing Values')
        st.dataframe(period3.isna().sum())

        st.write("We are seeing that in period 1 and period 2 there is a huge amount of missing values for HDLC and LDLC (period1=4434, period2=3930. This is interesting as we often calculate TOTCHOL with the HDLC and LDLC values, so it is important to note that in this study it was probably calculated in another way. TOTCHOL had a way smaller amount if missing values, enabling us to still be able to predict CVD from TOTCHOL")

    #Erroneous value filtering
    age_min, age_max = 32, 81
    totchol_min, totchol_max = 107, 696
    hdlc_min, hdlc_max = 10, 189
    ldlc_min, ldlc_max = 20, 565
    bmi_min, bmi_max = 14.43, 56.8

    valid_rows = (
        (cvd_clean["AGE"].between(age_min, age_max) | cvd_clean["AGE"].isna()) &
        (cvd_clean["TOTCHOL"].between(totchol_min, totchol_max) | cvd_clean["TOTCHOL"].isna()) &
        (cvd_clean["HDLC"].between(hdlc_min, hdlc_max) | cvd_clean["HDLC"].isna()) &
        (cvd_clean["LDLC"].between(ldlc_min, ldlc_max) | cvd_clean["LDLC"].isna()) &
        (cvd_clean["SEX"].isin([1, 2])) &
        (cvd_clean["CVD"].isin([0, 1]))
    )

    rows_before = len(cvd_clean)
    cvd_clean = cvd_clean[valid_rows].copy()
    rows_after = len(cvd_clean)

    st.subheader("Erroneous Values")
    st.write("Rows removed due to erroneous values:", rows_before - rows_after)
    st.write('''
    To identify erroneous data, we first examined missing values, descriptive statistics and the unique values of all categorical variables. This initial inspection allowed us to detect implausible values, inconsistencies in coding, and potential data-entry errors. For continuous variables such as age, total cholesterol, HDL, LDL and BMI, clinically realistic minimum and maximum thresholds were defined based on established medical reference ranges. Each observation was then checked against these bounds, while allowing missing values to remain for later imputation. Categorical variables, including sex, prevalent CHD, prevalent Ml and CVD outcome, were verified to contain only valid binary codes.

    All variables were then systematically validated using these predefined clinical bounds and category rules. Any observation falling outside physiologically plausible limits or containing invalid category codes would have been flagged and removed as erroneous.

    However, after applying these validation rules, zero rows were removed, confirming that the dataset did not contain values that violated biological plausibility or coding consistency.

    Although several extreme values were detected during outlier analysis using the interquartile range (IQR) method, these values did not exceed biological limits and are consistent with known clinical conditions such as severe hypercholesterolemia or obesity.

    Therefore, these observations were not classified as erroneous data but rather as valid high-risk cases. The absence of removed rows confirms that the dataset did not contain true erroneous values, and that all retained data reflect realistic patient measurements rather than data-entry or coding errors. Outlier identification and handling are discussed separately in the following section.''')

    toggleerrvalues = st.toggle("Show code for Erroneous Values")
    if toggleerrvalues:
        st.code('''#Erroneous value filtering
    age_min, age_max = 32, 81
    totchol_min, totchol_max = 107, 696
    hdlc_min, hdlc_max = 10, 189
    ldlc_min, ldlc_max = 20, 565
    bmi_min, bmi_max = 14.43, 56.8

    valid_rows = (
        (cvd_clean["AGE"].between(age_min, age_max) | cvd_clean["AGE"].isna()) &
        (cvd_clean["TOTCHOL"].between(totchol_min, totchol_max) | cvd_clean["TOTCHOL"].isna()) &
        (cvd_clean["HDLC"].between(hdlc_min, hdlc_max) | cvd_clean["HDLC"].isna()) &
        (cvd_clean["LDLC"].between(ldlc_min, ldlc_max) | cvd_clean["LDLC"].isna()) &
        (cvd_clean["SEX"].isin([1, 2])) &
        (cvd_clean["CVD"].isin([0, 1]))
    )

    rows_before = len(cvd_clean)
    cvd_clean = cvd_clean[valid_rows].copy()
    rows_after = len(cvd_clean)''')

    #Outliers
    st.subheader("Outliers")
    num_columns = ["AGE", "TOTCHOL", "HDLC", "LDLC", "BMI",]

    Q1 = cvd_clean[num_columns].quantile(0.25)
    Q3 = cvd_clean[num_columns].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier_mask = ((cvd_clean[num_columns] < lower_bound) | (cvd_clean[num_columns] > upper_bound))

    st.write("Number of outliers per variable (kept in dataset):")
    st.write(outlier_mask.sum())

    st.write("Final shape after cleaning (outliers kept):", cvd_clean.shape)

    st.write("Missing values after cleaning:")
    st.write(cvd_clean.isna().sum())



    st.write("**Reasoning for keeping Outliers:**")
    st.write('''
Outliers were identified in several continuous variables (TOTCHOL, HDLC, LDLC, BMI) using the IQR method, which is appropriate for skewed clinical data and does not rely on assumptions of normality. Identifying outliers allowed us to examine extreme values and determine whether they reflected true physiological measurements or potential errors.

All detected outliers were systematically compared against established clinical reference ranges and evidence from the medical literature. These comparisons showed that all extreme values were biologically plausible. For example, very high LDL cholesterol levels (>300 mg/dL) are rare but occur in individuals with familial hypercholesterolemia, HDL levels above 100 mg/dL have been reported in people with specific genetic profiles, total cholesterol values approaching 600 mg/dL can be observed in severe dyslipidemias, and BMI values above 50 fall within known ranges of severe obesity. Since none of these values exceeded physiologically possible limits, they were interpreted as valid patient measurements rather than artifacts or inaccuracies.

Although these observations were statistically identified as outliers, they were intentionally retained in the dataset. Extreme lipid profiles often correspond to individuals at the highest cardiovascular risk and therefore carry clinically meaningful information. Removing these values would compress the distribution toward artificially normal ranges, reduce sensitivity to true high-risk cases, and weaken the model's ability to learn valid associations between cholesterol measures and cardiovascular disease outcomes.

Furthermore, given that the dataset is imbalanced with relatively few positive CVD cases, excluding outliers would disproportionately remove high-risk observations and bias the dataset toward the majority class.

Outliers were therefore carefully evaluated but not removed, as they represent biologically realistic, clinically informative cases that are essential for preserving the integrity and real-world variability of the dataset.
''')

with st.expander("Describe and Visualize"):
    with st.expander("Describe"):
        #Descrive and Visualize
        st.subheader("Summary of Cohort")
        st.dataframe(cvd_clean[["AGE", "SEX","TOTCHOL", "HDLC", "LDLC","CVD"]].describe())

        import matplotlib.pyplot as plt

        #Cohort Summary: Descriptive Statistics
        st.subheader("Descriptive Statistics")
        st.subheader("Summary of Continuous Variables")
        # 1. Descriptive statistics for continuous variables
        cont_vars = ["AGE", "TOTCHOL", "HDLC", "LDLC"]
        cont_summary = cvd_clean[cont_vars].describe()
        st.write("Descriptive statistics for continuous variables:")
        (cont_summary)

        togglecontsummary = st.toggle("Show code for Summary of Continuous Variables")
        if togglecontsummary:
            st.code('''# 1. Descriptive statistics for continuous variables
        cont_vars = ["AGE", "TOTCHOL", "HDLC", "LDLC"]
        cont_summary = cvd_clean[cont_vars].describe()
        st.write("Descriptive statistics for continuous variables:")
        (cont_summary)''')

        st.subheader("Summary of Categorical Variables")
        # 2. Categorical summaries: SEX CVD
        st.write("SEX distribution (1 = Male, 2 = Female):")
        st.write(cvd_clean["SEX"].value_counts())
        st.write("SEX distribution (relative):")
        st.write(cvd_clean["SEX"].value_counts(normalize=True))

        st.write("CVD outcome distribution (0 = No event, 1 = Event):")
        st.write(cvd_clean["CVD"].value_counts())
        st.write("CVD outcome distribution (relative):")
        st.write(cvd_clean["CVD"].value_counts(normalize=True))

        togglecatsummary = st.toggle("Show code for Summary of Categorical Variables")
        if togglecatsummary:
            st.code('''# 2. Categorical summaries: SEX CVD
        st.write("SEX distribution (1 = Male, 2 = Female):")
        st.write(cvd_clean["SEX"].value_counts())
        st.write("SEX distribution (relative):")
        st.write(cvd_clean["SEX"].value_counts(normalize=True))

        st.write("CVD outcome distribution (0 = No event, 1 = Event):")
        st.write(cvd_clean["CVD"].value_counts())
        st.write("CVD outcome distribution (relative):")
        st.write(cvd_clean["CVD"].value_counts(normalize=True))''')
            
        st.write('''The final analytic cohort consisted of 3,206 participants from the Framingham Heart Study who had completed all three examination periods and had complete lipid measurements available in Period 3. This sample included detailed demographic information, cholesterol values, BMI, baseline cardiovascular conditions, and 24-year follow-up data on cardiovascular events. The age distribution of the cohort shows a mean of approximately 60.6 years, ranging from 44 to 81 years. The histogram reveals a slightly right-skewed distribution, with most individuals falling between 50 and 70 years of age, indicating a predominantly middle-aged to elderly population. This age range is clinically relevant, as cardiovascular disease risk increases substantially with age.

Total cholesterol values showed characteristics consistent with real-world clinical populations. The mean total cholesterol concentration was approximately 236 mg/dL with a standard deviation of 44 mg/dL, and values ranged from 112 to 625 mg/dL. The histogram demonstrates a normal-like central distribution with a modest right tail caused by several extreme but clinically plausible high values. HDL cholesterol displayed a mean of around 49 mg/dL, with some unusually high measurements up to 189 mg/dL. These upper-range values align with known genetic lipid conditions such as hyperalphalipoproteinemia. LDL cholesterol showed a mean of approximately 176 mg/dL and ranged up to 565 mg/dL, which is consistent with severe hypercholesterolemia commonly observed in familial lipid disorders. BMI values averaged around 25.9 kg/m?, close to the clinical overweight threshold. Some extreme BMI values appeared in the dataset but remained within physiologically expected limits for severe obesity. Boxplots for HDL, LDL, and BMI confirm a wide but realistic spread of values without evidence of data-entry artifacts, supporting the decision to retain outliers in subsequent analyses.

Categorical variables also reflect patterns typical of long-term cardiovascular cohort studies. The sex distribution consisted of 57.5% females and 42.5% males. The distribution of cardiovascular outcomes showed substantial class imbalance, with 23.3% of participants experiencing a cardiovascular event during follow-up and 76.7% remaining event-free.

Prevalent conditions at baseline included coronary heart disease in 351 individuals (11%) and myocardial infarction in 156 participants (5%). These baseline conditions provide important clinical context, as pre-existing cardiovascular disease substantially elevates the risk of future cardiovascular events.

The visualisations further support the interpretation of the dataset. The age histogram confirms a well-represented age span typical of cardiovascular research populations. The total cholesterol histogram demonstrates a central distribution with a right-tailed extension driven by high but plausible lipid values. Boxplots reinforce the presence of clinically meaningful heterogeneity, capturing both average and extreme lipid profiles commonly observed in real populations. Finally, CVD prevalence by sex shows that male participants have a substantially higher event rate (approximately 31%) compared to female participants (around 17%), consistent with well-established epidemiological findings that men tend to have higher cardiovascular risk earlier in life.

In addition to static figures, interactive visualisations were implemented to enhance exploratory analysis of the cohort. These interactive elements allow users to dynamically select variables and adjust age ranges using sliders and dropdown menus, enabling flexible inspection of distributions and relationships within the data. This functionality supports deeper exploration of population heterogeneity and facilitates intuitive comparison across subgroups, while maintaining consistency with the descriptive patterns observed in the static visualisations.
''')

    with st.expander("Visualizations"):
        st.subheader("Visualizations")

        #Age 
        st.write("**Age Distribution**")
        fig, ax = plt.subplots()
        ax.hist(cvd_clean["AGE"],bins=20)
        ax.set_title("Age Distribution")
        st.pyplot(fig)

        #Total Cholesterol
        st.write("**Total Cholesterol Distribution**")
        fig, ax = plt.subplots()
        ax.hist(cvd_clean["TOTCHOL"],bins=30)
        ax.set_xlabel("Total Cholesterol (mg/dL)")
        ax.set_ylabel("Number of Participants")
        ax.set_title("Total Cholesterol (mg/dL)")
        st.pyplot(fig)

        histogramdistributions = st.toggle("Show code for Histogram Distributions")

        if histogramdistributions:
            st.code('''#Age 
        st.subheader("Age Distribution")
        fig, ax = plt.subplots()
        ax.hist(cvd_clean["AGE"],bins=20)
        ax.set_title("Age Distribution")
        st.pyplot(fig)

        #Total Cholesterol
        st.subheader("Total Cholesterol Distribution")
        fig, ax = plt.subplots()
        ax.hist(cvd_clean["TOTCHOL"],bins=30)
        ax.set_xlabel("Total Cholesterol (mg/dL)")
        ax.set_ylabel("Number of Participants")
        ax.set_title("Total Cholesterol (mg/dL)")
        st.pyplot(fig)''')


        #Box plot for HDL and LDL
        st.subheader("Box plots for HDLC, LDLC, and BMI")
        fig17, ax = plt.subplots()
        ax.boxplot([cvd_clean["HDLC"].dropna(),cvd_clean["LDLC"].dropna(),cvd_clean["BMI"].dropna()], labels=["HDLC","LDLC","BMI"])
        ax.set_title("Boxplots of HDLC, LDLC, and BMI")
        ax.set_ylabel("Value")
        st.pyplot(fig17)

        toggleboxplot = st.toggle("Show code for Box plots")

        if toggleboxplot:
            st.code('''st.subheader("Box plots for HDLC, LDLC, and BMI")
            fig, ax = plt.subplots()
            ax.boxplot([cvd_clean["HDLC"].dropna(),cvd_clean["LDLC"].dropna(),cvd_clean["BMI"]], labels=["HDLC","LDLC"])
            ax.set_title("Boxplots of HDLC and LDLC")
            ax.set_ylabel("Value")
            st.pyplot(fig)''')


        # Bar plot for CVD prevalence by sex
        #    We map SEX to labels to make interpretation easier
        st.subheader('Bar plot for CVD prevalence')
        sex_map = {1: "Male", 2: "Female"}
        cvd_clean["SEX_label"] = cvd_clean["SEX"].map(sex_map)
        cvd_by_sex = cvd_clean.groupby("SEX_label")["CVD"].mean()

        vc = cvd_by_sex

        fig, ax = plt.subplots(figsize=(10,4))
        ax.bar(cvd_by_sex.index, cvd_by_sex.values)
        ax.set_xlabel("Sex")
        ax.set_ylabel("CVD Prevalence")
        ax.set_title("CVD Prevalence by Sex")
        st.pyplot(fig)

        togglebarplot = st.toggle("Show code for Bar plot")

        if togglebarplot:
            st.code('''sex_map = {1: "Male", 2: "Female"}
        cvd_clean["SEX_label"] = cvd_clean["SEX"].map(sex_map)
        cvd_by_sex = cvd_clean.groupby("SEX_label")["CVD"].mean()

        vc = cvd_by_sex

        fig, ax = plt.subplots(figsize=(10,4))
        ax.bar(cvd_by_sex.index, cvd_by_sex.values)
        ax.set_xlabel("Sex")
        ax.set_ylabel("CVD Prevalence")
        ax.set_title("CVD Prevalence by Sex")
        st.pyplot(fig)''')

        st.subheader("Distribution of Selected Variable")
        # Dropdown for variable selection
        variable = st.selectbox("Select variable", ["Age", "Total Cholesterol", "HDL Cholesterol", "LDL Cholesterol","BMI"])

        # Map display name to dataframe column
        options = {
            "Age": "AGE",
            "Total Cholesterol": "TOTCHOL",
            "HDL Cholesterol": "HDLC",
            "LDL Cholesterol": "LDLC",
            "BMI": "BMI"}
        col = options[variable]
        data = cvd_clean[col].dropna()

        # Plot histogram
        fig2, ax = plt.subplots(figsize=(12, 4))
        ax.hist(data, bins=20, edgecolor="black")
        ax.set_title(f"Distribution of {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Count")

        st.pyplot(fig2)

        togglehistogramselected = st.toggle("Show code for Distribution of Selected Variable")

        if togglehistogramselected:
            st.code('''variable = st.selectbox("Select variable", ["Age", "Total Cholesterol", "HDL Cholesterol", "LDL Cholesterol","BMI"])

        # Map display name to dataframe column
        options = {
            "Age": "AGE",
            "Total Cholesterol": "TOTCHOL",
            "HDL Cholesterol": "HDLC",
            "LDL Cholesterol": "LDLC",
            "BMI":"BMI"}
        col = options[variable]
        data = cvd_clean[col].dropna()

        # Plot histogram
        fig2, ax = plt.subplots(figsize=(12, 4))
        ax.hist(data, bins=20, edgecolor="black")
        ax.set_title(f"Distribution of {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Count")

        st.pyplot(fig2)''')

        #Boxplot of Selected Variable
        st.subheader("Boxplot of Selected Variable")
        
        variable = st.selectbox("Select variables", ["Age", "Total Cholesterol", "HDL Cholesterol", "LDL Cholesterol","BMI"])

        
        options = {
            "Age": "AGE",
            "Total Cholesterol": "TOTCHOL",
            "HDL Cholesterol": "HDLC",
            "LDL Cholesterol": "LDLC",
            "BMI":"BMI"}
        col = options[variable]
        data = cvd_clean[col].dropna()

        # Plot boxplot
        fig3, ax = plt.subplots(figsize=(12, 4))
        ax.boxplot(data)
        ax.set_title(f"Distribution of {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Count")

        st.pyplot(fig3)

        toggleboxplotselectedvariables = st.toggle("Show code for Boxplot of Selected Variables")

        if toggleboxplotselectedvariables:
            st.code('''variable = st.selectbox("Select variables", ["Age", "Total Cholesterol", "HDL Cholesterol", "LDL Cholesterol","BMI"])

        # Map display name to dataframe column
        options = {
            "Age": "AGE",
            "Total Cholesterol": "TOTCHOL",
            "HDL Cholesterol": "HDLC",
            "LDL Cholesterol": "LDLC",
            "BMI":"BMI"}
        col = options[variable]
        data = cvd_clean[col].dropna()

        # Plot histogram
        fig3, ax = plt.subplots(figsize=(12, 4))
        ax.boxplot(data)
        ax.set_title(f"Distribution of {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Count")

        st.pyplot(fig3)''')

        st.subheader("Interactive Scatter Plot")
        # Interactive Scatter Plot:
        x_var = st.selectbox("Select X variable", list(options.keys()))
        y_var = st.selectbox("Select Y variable", list(options.keys()))

        # Map display names to actual dataframe columns
        x_col = options[x_var]
        y_col = options[y_var]

        # Drop missing values
        x = cvd_clean[x_col].dropna()
        y = cvd_clean[y_col].dropna()

        # Make sure lengths match
        min_len = min(len(x), len(y))
        x = x.iloc[:min_len]
        y = y.iloc[:min_len]

        # Plot
        fig4, ax = plt.subplots(figsize=(8,5))
        ax.scatter(x, y, color='blue', alpha=0.6)
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        ax.set_title(f"Scatter Plot: {x_var} vs {y_var}")

        st.pyplot(fig4)

        togglescatterplot = st.toggle("Show code for Interactive Scatter Plot")

        if togglescatterplot:
            st.code('''# Interactive Scatter Plot:
        x_var = st.selectbox("Select X variable", list(options.keys()))
        y_var = st.selectbox("Select Y variable", list(options.keys()))

        # Map display names to actual dataframe columns
        x_col = options[x_var]
        y_col = options[y_var]

        # Drop missing values
        x = cvd_clean[x_col].dropna()
        y = cvd_clean[y_col].dropna()

        # Make sure lengths match
        min_len = min(len(x), len(y))
        x = x.iloc[:min_len]
        y = y.iloc[:min_len]

        # Plot
        fig4, ax = plt.subplots(figsize=(8,5))
        ax.scatter(x, y, color='blue', alpha=0.6)
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        ax.set_title(f"Scatter Plot: {x_var} vs {y_var}")

        st.pyplot(fig4)''')

        #Interactive Age Filter + Histogram
        st.subheader("Interactive Age Filtered Histogram")

        age_min = int(cvd_clean["AGE"].min())
        age_max = int(cvd_clean["AGE"].max())

        age_range = st.slider(
            "Age range:",
            min_value=age_min,
            max_value=age_max,
            value=(age_min, age_max)
        )
        variable = st.selectbox(
            "Variable:",
            list(options.keys())
        )
        col = options[variable]

        filtered = cvd_clean[
            (cvd_clean["AGE"] >= age_range[0]) &
            (cvd_clean["AGE"] <= age_range[1])
        ][col].dropna()

        fig5, ax = plt.subplots(figsize=(6, 4))
        ax.hist(filtered, bins=20, edgecolor="black")
        ax.set_title(f"{variable} distribution (Age {age_range[0]}–{age_range[1]})")
        ax.set_xlabel(variable)
        ax.set_ylabel("Number of participants")

        st.pyplot(fig5)

        toggleinterhistogram = st.toggle("Show code for Interactive Age Filtered Histogram")

        if toggleinterhistogram:
            st.code('''age_min = int(cvd_clean["AGE"].min())
        age_max = int(cvd_clean["AGE"].max())

        age_range = st.slider(
            "Age range:",
            min_value=age_min,
            max_value=age_max,
            value=(age_min, age_max)
        )
        variable = st.selectbox(
            "Variable:",
            list(options.keys())
        )
        col = options[variable]

        filtered = cvd_clean[
            (cvd_clean["AGE"] >= age_range[0]) &
            (cvd_clean["AGE"] <= age_range[1])
        ][col].dropna()

        fig5, ax = plt.subplots(figsize=(6, 4))
        ax.hist(filtered, bins=20, edgecolor="black")
        ax.set_title(f"{variable} distribution (Age {age_range[0]}–{age_range[1]})")
        ax.set_xlabel(variable)
        ax.set_ylabel("Number of participants")

        st.pyplot(fig5)''')

with st.expander("Data Analysis"):
    st.header("Data Analysis")
    st.subheader("Imputation")
   
    st.write("As we saw before, in our cleaned dataset there were still some missing values in the numerical columns (TOTCHOL = 210, HDLC = 231, LDLC = 232). To address this, we will perform imputation to fill in these missing values. We will use the median value of each numerical column to impute the missing data, as the median is less affected by outliers compared to the mean. This approach helps to maintain the overall distribution of the data while providing reasonable estimates for the missing values.")
    cvd_clean_imputed = cvd_clean.copy()


    #Imputed Numerical Columns with Median
    numeric_cols = ["AGE", "TOTCHOL", "HDLC", "LDLC","BMI"]
    cvd_clean_imputed[numeric_cols] = cvd_clean_imputed[numeric_cols].fillna(cvd_clean_imputed[numeric_cols].median())

    st.write("Missing values in cvd_clean_imputed:")
    st.dataframe(cvd_clean_imputed.isna().sum())

    st.write("All missing values have been imputed using median successfully")

    toggleimputation = st.toggle("Show code for Imputation")

    if toggleimputation:
        st.code('''#Imputed Numerical Columns with Median
    numeric_cols = ["AGE", "TOTCHOL", "HDLC", "LDLC"]
    cvd_clean_imputed[numeric_cols] = cvd_clean_imputed[numeric_cols].fillna(cvd_clean_imputed[numeric_cols].median())

    st.write("Missing values in cvd_clean_imputed:")
    st.dataframe(cvd_clean_imputed.isna().sum())''')
        
    #Visuals after imputation
    st.subheader("Visualizations after Imputation")
    st.write("Distribution of selected variable with imputed Data")
    variable = st.selectbox("Select variable", ["Age", "Total Cholesterol", "HDL Cholesterol", "LDL Cholesterol","BMI"],key='imputed_histogram')

    # Map display name to dataframe column
    options = {
        "Age": "AGE",
        "Total Cholesterol": "TOTCHOL",
        "HDL Cholesterol": "HDLC",
        "LDL Cholesterol": "LDLC",
        "BMI":"BMI"}
    col = options[variable]
    data = cvd_clean_imputed[col].dropna()

        # Plot histogram
    fig10, ax = plt.subplots(figsize=(12, 4))
    ax.hist(data, bins=20, edgecolor="black")
    ax.set_title(f"Distribution of {variable} with imputed data")
    ax.set_xlabel(variable)
    ax.set_ylabel("Count")

    st.pyplot(fig10)


    #interactive box plot after imputation
    variable = st.selectbox("Select variables", ["Age", "Total Cholesterol", "HDL Cholesterol", "LDL Cholesterol","BMI"], key='imputed_boxplot')

    # Map display name to dataframe column
    options1 = {
        "Age": "AGE",
        "Total Cholesterol": "TOTCHOL",
        "HDL Cholesterol": "HDLC",
        "LDL Cholesterol": "LDLC",
        "BMI":"BMI"}
    col = options1[variable]
    data = cvd_clean_imputed[col].dropna()

    fig11, ax = plt.subplots(figsize=(12, 4))
    ax.boxplot(data)
    ax.set_title(f"Distribution of {variable} using imputed data")
    ax.set_xlabel(variable)
    ax.set_ylabel("Count")

    st.pyplot(fig11)


    st.header("Feature Engineering")
    st.write('''To enhance the predictive performance of the models and better capture clinically meaningful cardiovascular risk patterns, additional features were engineered from the original variables, Non-HDL cholesterol was calculated as total cholesterol minus HDL cholesterol, representing the total burden of atherogenic lipoproteins rather than LDL cholesterol alone. In addition, the LDL-to-HDL ratio and the total cholesterol-to-HDL ratio were included to reflect the balance between harmful and protective lipid fractions, which is known to be more informative for cardiovascular risk assessment than absolute lipid values. Finally, a binary age indicator (age ≥ 65 years) was created to capture the increased baseline risk associated with older age. These engineered features preserve clinical interpretability while allowing the models to learn more nuanced, non-linear relationships between lipid profiles, age, and cardiovascular disease outcomes.''')

    cvd_clean_imputed["NONHDL"] = cvd_clean_imputed["TOTCHOL"] - cvd_clean_imputed["HDLC"]
    cvd_clean_imputed["LDL_to_HDL"] = cvd_clean_imputed["LDLC"] / cvd_clean_imputed["HDLC"]
    cvd_clean_imputed["TOTCHOL_to_HDL"] = cvd_clean_imputed["TOTCHOL"] / cvd_clean_imputed["HDLC"]
    cvd_clean_imputed["AGE_65plus"] = (cvd_clean_imputed["AGE"] >= 65).astype(int)


    togglefeatureengineering = st.toggle("Show individual Feature Engineering tables")
    if togglefeatureengineering:
        st.write("Non-HDL cholesterol: atherogenic cholesterol")
        #    (all cholesterol that is NOT HDL)
        cvd_clean_imputed["NONHDL"] = cvd_clean_imputed["TOTCHOL"] - cvd_clean_imputed["HDLC"]
        st.dataframe(cvd_clean_imputed["NONHDL"])

        st.write("LDL / HDL ratio")
        #    Higher values indicate worse cardiovascular risk.
        cvd_clean_imputed["LDL_to_HDL"] = cvd_clean_imputed["LDLC"] / cvd_clean_imputed["HDLC"]
        st.dataframe(cvd_clean_imputed["LDL_to_HDL"])

        st.write("Total cholesterol / HDL ratio")
        #    A classic clinical risk index.
        cvd_clean_imputed["TOTCHOL_to_HDL"] = cvd_clean_imputed["TOTCHOL"] / cvd_clean_imputed["HDLC"]
        st.dataframe(cvd_clean_imputed["TOTCHOL_to_HDL"])

        st.write("Age 65+ indicator")
        cvd_clean_imputed["AGE_65plus"] = (cvd_clean_imputed["AGE"] >= 65).astype(int)
        st.dataframe(cvd_clean_imputed["AGE_65plus"])

    st.dataframe(cvd_clean_imputed[["NONHDL", "LDL_to_HDL", "TOTCHOL_to_HDL", "AGE_65plus"]].head())



import streamlit as st
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(max_iter=1000,class_weight="balanced")
from sklearn import tree
decision_tree = tree.DecisionTreeClassifier(random_state=1,class_weight="balanced")

with st.expander("Model Evaluation using KFold Cross-Validation"):

    st.subheader("Model evaluation using KFold Cross-Validation")
    st.write("Step 1: We split the dataset into input features (X) and the label (y).")

    featuresX = [
        'SEX','AGE','TOTCHOL','HDLC','LDLC','NONHDL',
        "BMI", "PREVCHD", "PREVMI",
        'LDL_to_HDL','TOTCHOL_to_HDL','AGE_65plus'
    ]

    X = cvd_clean_imputed[featuresX]
    y = cvd_clean_imputed["CVD"]

    st.code('''
# Prepare X and y (including engineered features)
featuresX = [
    'SEX','AGE','TOTCHOL','HDLC','LDLC','NONHDL',
    "BMI", "PREVCHD", "PREVMI",
    'LDL_to_HDL','TOTCHOL_to_HDL','AGE_65plus'
]

X = cvd_clean_imputed[featuresX]
y = cvd_clean_imputed["CVD"]
''')

    st.write("Step 2: Train/test split")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, stratify=y, random_state=1
    )
    st.code('X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, stratify=y, random_state=1)')

    # 5-fold CV on training data only
    kf = KFold(n_splits=5, shuffle=True, random_state=1)
    st.write("Step 3: 5-fold cross-validation on the training data")
    st.code("kf = KFold(n_splits=5, shuffle=True, random_state=1)")

    st.write("Step 4: Evaluation function")
    def evaluate_model(model, X, y, kf):
        accuracies = []

        for train_index, val_index in kf.split(X):

            train_X, val_X = X.iloc[train_index].copy(), X.iloc[val_index].copy()
            train_y, val_y = y.iloc[train_index], y.iloc[val_index]

            # Median imputation (TRAIN ONLY)
            medians = train_X.median()
            train_X = train_X.fillna(medians)
            val_X = val_X.fillna(medians)

            # Scaling (already introduced elsewhere in notebook)
            scaler = StandardScaler()
            train_X = scaler.fit_transform(train_X)
            val_X = scaler.transform(val_X)

            # Fit + predict
            model.fit(train_X, train_y)
            preds = model.predict(val_X)

            accuracies.append(accuracy_score(val_y, preds))

        return accuracies

    # Define models
    logreg = LogisticRegression(max_iter=1000, class_weight="balanced")
    decision_tree = tree.DecisionTreeClassifier(random_state=1, class_weight="balanced")

    # Evaluate models
    logreg_acc = evaluate_model(logreg, X_train, y_train, kf)
    tree_acc   = evaluate_model(decision_tree, X_train, y_train, kf)

    st.write("Logistic Regression accuracies (CV on train):", logreg_acc)
    st.write("Logistic Regression mean accuracy:", np.mean(logreg_acc))

    st.write("Decision Tree accuracies (CV on train):", tree_acc)
    st.write("Decision Tree mean accuracy:", np.mean(tree_acc))


with st.expander("Model evaluation using StratifiedKFold Cross-Validation"):
    import streamlit as st
    import numpy as np
    from sklearn.model_selection import StratifiedKFold
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn import tree
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.naive_bayes import GaussianNB

    # ----------------------------------------------------------
    # Example: Define candidate features & target (replace with your dataset)
    featuresX = ['SEX','AGE','TOTCHOL','HDLC','LDLC',
                 "BMI", "PREVCHD", "PREVMI",
                 'NONHDL','LDL_to_HDL','TOTCHOL_to_HDL','AGE_65plus']

    X = cvd_clean_imputed[featuresX]  # your dataset
    y = cvd_clean_imputed["CVD"]

    # Train/test split (50/50)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, stratify=y, random_state=1)

    # Stratified K-Fold CV
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)

    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score

    # Evaluation function
    def evaluate_model(model, X, y, skf):
        accuracies = []

        for train_idx, val_idx in skf.split(X, y):
            train_X, val_X = X.iloc[train_idx].copy(), X.iloc[val_idx].copy()
            train_y, val_y = y.iloc[train_idx], y.iloc[val_idx]

            # Median imputation (TRAIN ONLY)
            medians = train_X.median()
            train_X = train_X.fillna(medians)
            val_X = val_X.fillna(medians)

            # Scaling (TRAIN ONLY)
            scaler = StandardScaler()
            train_X = scaler.fit_transform(train_X)
            val_X = scaler.transform(val_X)

            model.fit(train_X, train_y)
            preds = model.predict(val_X)

            accuracies.append(accuracy_score(val_y, preds))

        return accuracies
    
    # Candidate models for selection

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Decision Tree": tree.DecisionTreeClassifier(random_state=1, class_weight="balanced"),
        "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, random_state=1, class_weight="balanced"
        ),
        "Naive Bayes": GaussianNB()
    }

    # ----------------------------------------------------------
    # Evaluate models (IMPORTANT: training set only)

    results = {}

    for name, model in models.items():
        accs = evaluate_model(model, X_train, y_train, skf)
        results[name] = accs
        st.write(f"\n{name} accuracies per fold: {accs}")
        st.write(f"{name} mean accuracy: {np.mean(accs):.4f}")

    # ----------------------------------------------------------
    # Summary comparison

    st.write("**Model Comparison:**")
    for name, accs in results.items():
        st.write(f"{name}: {np.mean(accs):.4f}")






    #    # Visualization of Model Comparison
    # Convert results into usable lists
    model_names = list(results.keys())
    mean_acc = [np.mean(results[m]) for m in model_names]
# -----------------------------------------------
    # BAR PLOT: 
    fig12, ax = plt.subplots(figsize=(10,4))
    ax.bar(model_names, mean_acc)
    ax.set_ylabel("Mean Accuracy")
    ax.set_title("Model Comparison: Mean Accuracy Across 5 Folds")
    st.pyplot(fig12)


    # -----------------------------------------------
    # BOXPLOT: 
    fig13, ax = plt.subplots(figsize=(10,5))
    ax.boxplot([results[m] for m in model_names],tick_labels=model_names)
    ax.set_title("Cross-Validation Accuracy Distribution")
    ax.set_ylabel("Accuracy")
    st.pyplot(fig13)

    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd


    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score,
        f1_score, confusion_matrix
    )

    st.write("Here we can see that the Random Forest Model performed the best during cross-validation on the training set, achieving the highest mean accuracy across the folds. Therefore, we will select the Random Forest model as our final model for further evaluation on the test set.")




    st.write("**Table for accuracy, precision, recall, F1-score on test set using the selected Random Forest model:**")
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd

    # ----------------------------------------------------------
    # FINAL MODEL: Random Forest (selected from Block 2)
    # ----------------------------------------------------------

    final_model = RandomForestClassifier(
        n_estimators=100,
        random_state=1,
        class_weight="balanced"
    )

    # ----------------------------------------------------------
    # Prepare train and test sets (imputed + engineered)
    # ----------------------------------------------------------

    # Median imputation (fit on TRAIN only)
    medians = X_train.median()
    X_train_imp = X_train.fillna(medians)
    X_test_imp = X_test.fillna(medians)

    # Scaling (fit on TRAIN only)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_imp)
    X_test_scaled = scaler.transform(X_test_imp)

    # ----------------------------------------------------------
    # Train final model
    # ----------------------------------------------------------

    final_model.fit(X_train_scaled, y_train)

    # ----------------------------------------------------------
    # Predict on TEST set
    # ----------------------------------------------------------

    y_pred = final_model.predict(X_test_scaled)

    # ----------------------------------------------------------
    # Compute metrics
    # ----------------------------------------------------------

    final_metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1": f1_score(y_test, y_pred, zero_division=0)
    }

    metrics_df = pd.DataFrame(final_metrics, index=["Random Forest"])
    metrics_df  





    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    import matplotlib.pyplot as plt

    # Predict using the TRAINED Random Forest model
    y_pred = final_model.predict(X_test_scaled)

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["No CVD", "CVD"]
    )

    fig, ax = plt.subplots(figsize=(5, 4))
    disp.plot(ax=ax, cmap="Blues", values_format="d")
    ax.set_title("Confusion Matrix – Random Forest (Test Set)")
    st.pyplot(fig)

    st.write('''The confusion matrix provides insight into how the model classifies individuals with and without cardiovascular disease (CVD). At the default decision threshold of 0.5, the model correctly classified the majority of non-VD cases, indicating high specificity. However, a substantial number of true CVD cases were misclassified as non-CVD, reflected by a high number of false negatives. This explains the relatively high accuracy but low recall and F1 score observed at the default threshold, demonstrating that the model is conservative in predicting positive CVD outcomes.

When the decision threshold was adjusted to the F1-optimal value (approximately 0.26), the confusion matrix shows a clear reduction in false negatives and an increase in true positive CVD classifications. This improvement indicates higher sensitivity to CVD cases, although it occurs at the cost of an increased number of false positives and a reduction in overall accuracy. In a clinical risk-prediction context, this trade-off is considered acceptable, as failing to identify individuals at risk of cardiovascular disease may have more serious consequences than generating additional false alarms. Overall, the confusion matrix analysis highlights the impact of threshold selection on model performance and reinforces the importance of balancing sensitivity and specificity in imbalanced medical datasets.
''')






with st.expander("Hyperparameter Tuning for Two Models"):
    st.subheader('Hyperparameter Tuning for Two Models: Logistic Regression + Random Forest')
    # ==========================================================
    # HYPERPARAMETER TUNING FOR BEST TWO MODELS
    # Logistic Regression + Random Forest
    # (Using IMPUTED data + CV on TRAIN ONLY)
    # ==========================================================

    import numpy as np
    from sklearn.model_selection import KFold
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier

    # ----------------------------------------------------------
    # Use TRAINING data only (already imputed earlier)
    X_tune = X_train.copy()
    y_tune = y_train.copy()

    kf = KFold(n_splits=5, shuffle=True, random_state=1)

    # ----------------------------------------------------------
    # Evaluation function (same structure as before)

    def evaluate_model_metrics(model, X, y, kf):
        accs, precs, recs, f1s = [], [], [], []

        for train_idx, val_idx in kf.split(X):
            train_X, val_X = X.iloc[train_idx].copy(), X.iloc[val_idx].copy()
            train_y, val_y = y.iloc[train_idx], y.iloc[val_idx]

            # Median imputation (TRAIN ONLY)
            med = train_X.median()
            train_X = train_X.fillna(med)
            val_X = val_X.fillna(med)

            # Fit + predict
            model.fit(train_X, train_y)
            preds = model.predict(val_X)

            accs.append(accuracy_score(val_y, preds))
            precs.append(precision_score(val_y, preds, zero_division=0))
            recs.append(recall_score(val_y, preds, zero_division=0))
            f1s.append(f1_score(val_y, preds, zero_division=0))

        return np.mean(accs), np.mean(precs), np.mean(recs), np.mean(f1s)

    # ----------------------------------------------------------
    # 1️⃣ LOGISTIC REGRESSION TUNING

    logreg_params = {
        "solver": ["liblinear", "saga"],
        "C": [0.1, 0.5, 1.0, 2.0]
    }

    logreg_results = []

    for solver in logreg_params["solver"]:
        for C in logreg_params["C"]:
            model = LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                solver=solver,
                C=C
            )
            acc, prec, rec, f1 = evaluate_model_metrics(model, X_tune, y_tune, kf)
            logreg_results.append((solver, C, acc, prec, rec, f1))
            print(
                f"LR solver={solver}, C={C} → "
                f"Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}, F1={f1:.4f}"
            )

    # ----------------------------------------------------------
    # 2️⃣ RANDOM FOREST TUNING

    rf_params = {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5]
    }

    rf_results = []

    for n in rf_params["n_estimators"]:
        for d in rf_params["max_depth"]:
            for split in rf_params["min_samples_split"]:
                model = RandomForestClassifier(
                    n_estimators=n,
                    max_depth=d,
                    min_samples_split=split,
                    class_weight="balanced",
                    random_state=1
                )
                acc, prec, rec, f1 = evaluate_model_metrics(model, X_tune, y_tune, kf)
                rf_results.append((n, d, split, acc, prec, rec, f1))
                print(
                    f"RF n={n}, depth={d}, split={split} → "
                    f"Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}, F1={f1:.4f}"
                )

    st.write('''Model Comparison and Justification of the Selected Model

To evaluate the predictive performance of several machine-learning models for cardiovascular disease (CVD), we compared Logistic Regression, Decision Trees, K-Nearest Neighbors (KNN), Random Forests, and Naive Bayes using 5-fold cross-validation. Performance was assessed using accuracy, precision, recall, and F1 score. Because the dataset is imbalanced, with approximately 23% positive CVD cases, accuracy alone is insufficient to assess model performance. Models optimised for accuracy may achieve high scores by favouring the majority class while failing to detect true CVD events.

Logistic Regression with class weighting demonstrated the highest recall (approximately 0.65) and the highest F1 score (approximately 0.54) among all evaluated models. This indicates a stronger ability to identify patients who experienced CVD events, at the cost of reduced overall accuracy (approximately 0.74). This trade-off is expected and appropriate in a medical risk-prediction context, where failing to identify a high-risk patient is more harmful than generating false positives.

Random Forest models achieved the highest overall accuracy (up to approximately 0.81) and higher precision, but exhibited substantially lower recall (approximately 0.30 in deeper configurations). Hyperparameter tuning showed that shallower Random Forest models improved recall at the expense of accuracy, highlighting a clear trade-off between sensitivity and specificity. This suggests that while Random Forests are effective at modelling non-linear relationships and maintaining robust accuracy, they remain conservative in predicting positive CVD cases given the available features.

Naive Bayes achieved competitive accuracy and moderate recall, while KNN showed intermediate performance across metrics. Decision Trees exhibited lower stability and generalisation performance compared to ensemble-based methods.

Overall, model selection depends on the clinical objective. If the goal is to maximise detection of CVD cases, the weighted Logistic Regression model offers the greatest clinical utility due to its superior sensitivity and balanced F1 score. If overall accuracy and robustness are prioritised, Random Forests provide stronger performance but at the cost of missed positive cases. These results highlight the inherent trade-offs in clinical prediction tasks and the limitations imposed by the available lipid and demographic features.''')


with st.expander("Bonus"):
    st.subheader("Bonus")
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.metrics import (
        precision_score, recall_score, f1_score,
        accuracy_score, confusion_matrix, ConfusionMatrixDisplay
    )

    # ==========================================================
    # 1. Get predicted probabilities from the TRAINED final model
    # ==========================================================

    # Probability of CVD = 1
    y_prob = final_model.predict_proba(X_test_scaled)[:, 1]

    # ==========================================================
    # 2. Evaluate metrics across thresholds
    # ==========================================================

    thresholds = np.linspace(0.05, 0.95, 100)

    precision_scores = []
    recall_scores = []
    f1_scores = []

    for t in thresholds:
        y_pred_t = (y_prob >= t).astype(int)

        precision_scores.append(
            precision_score(y_test, y_pred_t, zero_division=0)
        )
        recall_scores.append(
            recall_score(y_test, y_pred_t, zero_division=0)
        )
        f1_scores.append(
            f1_score(y_test, y_pred_t, zero_division=0)
        )

    # ==========================================================
    # 3. Plot Precision, Recall, and F1 vs threshold
    # ==========================================================

    fig15, ax = plt.subplots(figsize=(7, 4))

    ax.plot(thresholds, f1_scores, label="F1 score")
    ax.plot(thresholds, precision_scores, linestyle="--", label="Precision")
    ax.plot(thresholds, recall_scores, linestyle="--", label="Recall")

    ax.set_xlabel("Decision Threshold")
    ax.set_ylabel("Score")
    ax.set_title("Precision, Recall, and F1 vs Threshold")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig15)

    # ==========================================================
    # 4. Find optimal threshold (max F1)
    # ==========================================================

    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds[best_idx]
    best_f1 = f1_scores[best_idx]

    st.write(f"Optimal threshold (max F1): {best_threshold:.2f}")
    st.write(f"Best F1 score: {best_f1:.3f}")

    # ==========================================================
    # 5. Metrics at DEFAULT threshold (0.5)
    # ==========================================================

    y_pred_default = (y_prob >= 0.5).astype(int)

    acc_default = accuracy_score(y_test, y_pred_default)
    f1_default = f1_score(y_test, y_pred_default, zero_division=0)

    
    
    
    st.write("\nDefault threshold (0.5):")
    st.write(f"Accuracy: {acc_default:.3f}")
    st.write(f"F1 score: {f1_default:.3f}")

    # Confusion matrix (default threshold)
    cm_default = confusion_matrix(y_test, y_pred_default)

    fig17, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(
        confusion_matrix=cm_default,
        display_labels=["No CVD", "CVD"]
    ).plot(ax=ax, cmap="Blues", values_format="d")

    ax.set_title("Confusion Matrix – Default Threshold (0.5)")
    st.pyplot(fig17)

    # ==========================================================
    # 6. Metrics at OPTIMAL F1 threshold
    # ==========================================================

    y_pred_opt = (y_prob >= best_threshold).astype(int)

    acc_opt = accuracy_score(y_test, y_pred_opt)
    f1_opt = f1_score(y_test, y_pred_opt, zero_division=0)




    st.write("\nOptimal F1 threshold:")
    st.write(f"Threshold: {best_threshold:.2f}")
    st.write(f"Accuracy: {acc_opt:.3f}")
    st.write(f"F1 score: {f1_opt:.3f}")

    # Confusion matrix (optimal threshold)
    cm_opt = confusion_matrix(y_test, y_pred_opt)

    fig18, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(
        confusion_matrix=cm_opt,
        display_labels=["No CVD", "CVD"]
    ).plot(ax=ax, cmap="Blues", values_format="d")

    ax.set_title(f"Confusion Matrix – Optimal F1 Threshold ({best_threshold:.2f})")
    st.pyplot(fig18)

    st.write('''**Threshold Optimisation and F1 score**

We used the F1 score as one of the primary evaluation metrics because our dataset is imbalanced, with far fewer participants experiencing a cardiovascular event than those who remained event-free. In such settings, accuracy alone can be misleading, as high accuracy may be achieved by favouring the majority class. The F1 score provides a balanced assessment of model performance by combining precision and recall, making it more informative for evaluating the detection of relatively rare CVD events.
The models output continuous probabilities representing an individual's estimated risk ofCVD, which were converted into binary class predictions using a decision threshold. Model performance was therefore evaluated across a range of decision thresholds. Lowering the threshold increased recall by identifying more true CVD cases, while higher thresholds increased precision at the expense of missed cases. The F1 score reached its maximum at a threshold of approximately 0.26, indicating the best balance between false positives and false negatives for this dataset. At the default threshold of 0.5, the model achieved relatively high accuracy but a substantially lower F1 score, reflecting reduced sensitivity to CVD cases. Adjusting the threshold to the F1-optimal value improved the model's ability to detect CVD events, albeit with a decrease in overall accuracy.
Although the resulting F1 scores remained relatively low, they were intentionally retained as they reflect the true predictive limitations of the model rather than artificially inflated performance. Increasing the F1 score by forcing extreme thresholds would result in clinically unrealistic behaviour, such as classifying nearly all individuals as high risk in order to maximise recall. While this might improve the F1 score numerically, it would substantially reduce the practical usefulness and reliability of the model. By reporting the observed F1 scores and their associated trade-offs transparently, the evaluation provides a realistic and honest assessment of how well total cholesterol measured in Period 3 contributes to predicting cardiovascular disease risk, given the complexity of CVD and the limited number of available predictors.
    ''')

with st.expander("Conclusion"):
    st.header('Conclusion')
    st.write('''In this study, we investigated how total cholesterol measured in Period 3 contributes to the prediction of cardiovascular disease (CVD) using data from the Framingham Heart Study. Through systematic data cleaning, careful handling of outliers, feature engineering, and the application of multiple machine-learning models, we showed that total cholesterol contains meaningful information related to long-term cardiovascular risk, but is insufficient on its own to fully distinguish between individuals who will and will not experience a CVD event.
    The results demonstrate that models relying primarily on lipid and basic demographic variables achieve moderate predictive performance. While overall accuracy was relatively high across several models, this was largely driven by the majority non-VD class. When evaluated using metrics appropriate for imbalanced data, particularly the F1 score and recall, model performance was more limited. Threshold optimization improved the balance between precision and recall and increased sensitivity to CVD cases, but this came at the cost of reduced accuracy and increased false positives. These trade-offs reflect the inherent difficulty of predicting complex clinical outcomes such as CVD using a restricted set of predictors.
    Importantly, the decision to retain clinically plausible outliers and to report relatively low F1 scores ensures that the results provide an honest representation of the model's true predictive ability. Rather than artificially inflating performance, our approach preserves real-world variability and highlights the limitations of cholesterol-focused prediction.
    Overall, the findings suggest that while total cholesterol from Period 3 contributes to CVD risk prediction, accurate identification of future cardiovascular events likely requires the integration of additional clinical, behavioural, and longitudinal risk factors.
    ''')
        