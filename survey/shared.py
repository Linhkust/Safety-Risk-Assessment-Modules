from shiny import ui
import pandas as pd

choices = {'N/A' : '',
    '1/9': 'Extremely less important',
                 '1/8': 'Very substantially to extremely less important',
                 '1/7': 'Very substantially less important',
                 '1/6': 'Substantial to very substantial less important',
                 '1/5': 'Substantial less important',
                 '1/4': 'Medium to substantial less important',
                 '1/3': 'Medium less important',
                 '1/2': 'Equal to medium less important',
                 '1': 'Equally important',
                 '2': 'Equal to medium more important',
                 '3': 'Medium more important',
                 '4': 'Medium to substantial more important',
                 '5': 'Substantial more important',
                 '6': 'Substantial to very substantial more important',
                 '7': 'Very substantially more important',
                 '8': 'Very substantially to extremely more important',
                 '9': 'Extremely more important'}

risk = pd.DataFrame(pd.read_csv('risks.csv'))

probability_scales = {'N/A' : '',
    '1' : 'Very Low',
                      '3' : 'Low',
                      '5' : 'Medium',
                      '7'	: 'High',
                      '9'	: 'Very High'}

severity_scales = {'1' : 'Trivial',
                      '3' : 'Significant',
                      '5' : 'Moderate',
                      '7'	: 'High',
                      '9'	: 'Catastrophic'}

frequency_scales = {'N/A' : '',
    '1' : 'Very Rare',
                      '3' : 'Rare',
                      '5' : 'Occasional',
                      '7'	: 'Regular',
                      '9'	: 'Permanent'}

detectability_scales = {'N/A' : '',
    '1' : 'Absolutely possible',
                      '3' : 'Strongly possible ',
                      '5' : 'Possible',
                      '7'	: 'Impossible',
                      '9'	: 'Strongly impossible'}

INPUTS = {
    "role": ui.input_select("role", "1. Your Position",
                            ['', 'Academic researchers/educators',
                                       'Site managers/Project managers',
                                       'Construction Workers',
                                       'Health and Safety Consultants',
                                       'Contractors and subcontractors']),
    "years": ui.input_select(
        "years",
        "2. Years of experience",
        choices=["",
                 "Less than 5 years",
                 "5-10 years",
                 "11-20 years",
                 'More than 20 years'],
    ),

    "education": ui.input_select(
        "education",
        "3. Your education level",
        choices=["",
                 "Less than high school degree",
                 "High school degree or equivalent",
                 "Bachelor's degree",
                 "Master's Degree",
                 "Doctorate (Ph.D.)"],
    )
}