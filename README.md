# Safety-Risk-Assessment-Modules
Data and codes for the paper "Towards safer construction industry: A systematic safety risk assessment framework integrating descriptive and prescriptive analytical approaches."
## Survey module
The survey module aims to assist decision-makers in completing the survey, including the collection of demographic information, pairwise comparison, and subjective evaluation. The `survey` folder contains all the data and codes of the survey module.
- The `ahp.py` calculates the weights based on pairwise comparison results.
- The `risk.csv` defines the identified safety risks.
- The `shared.py` defines the choices of AHP, scales of SCEA, and alternatives of demographic information.
- Run the `app.py` and the graphical user interface (GUI) of the survey module can be opened on the localhost.
## Analysis module
The analysis module aims to assist decision-makers in analyzing the survey results, including showing the distribution of respondents' information and risk assessment results. The `analysis` folder contains all the data and codes of the survey module.
- The `analysis.py` defines the necessary functions of risk assessment.
- The `quantitative _eval.csv` records the objective evaluation results of probability and severity risk parameters.
- The `fuzzy_scea.csv` and `fuzzy_scea.py` formulate the basis of the fuzzy SCEA risk assessment framework.
- The `response` folder includes all the survey results of respondents.
- Run the `app.py` and the graphical user interface (GUI) of the analysis module can be opened on the localhost.
