from pathlib import Path
import pandas as pd
import numpy as np
from shared import INPUTS
from shiny import App, Inputs, Outputs, Session, reactive, ui, render
from shiny_validate import InputValidator, check
from shared import choices, risk, frequency_scales, detectability_scales
from ahp import int_fraction, ahp_analysis, generate_random_str

app_dir = Path(__file__).parent

app_ui = ui.page_fixed(
    ui.include_css(app_dir / "styles.css"),
    ui.panel_title("Risk Magnitude Assessment Questionnaire Survey"),
    ui.card(
    ui.card_header("[A] Demographic Information"),
        INPUTS["role"],
        INPUTS["years"],
        INPUTS["education"],
    ),

    ui.card(
        ui.help_text(ui.card_header("[B.1] Pairwise Comparison"),
                     'Pairwise comparison for evaluating the importance degree of probability, severity, exposure, detectability for safety risk magnityude measurement'),
        ui.HTML("""
                <p>
                Definition: <br>
                [1] Probability:  likelihood or chance that a safety risk occur <br>
                [2] Severity: magnitude of harm or damage that result from a safety risk <br>
                [3] Exposure: how often workers are exposed to a safety risk <br>
                [4] Detectability: the ease with which a safety risk can be identified prior to its occurrence
                </p>
                <p>
                Note: Please click Consistency Check button after you fill the table to ensure consistency. Same for [B.2] section.
                 </p>
                """
        ),
        ui.output_data_frame('pc1'),
        ui.input_action_button("pc1submit", "Consistency Check", disabled=True, class_="btn btn-primary", width='200px')
    ),

    ui.card(
        ui.help_text(ui.card_header("[B.2] Pairwise Comparison"),
                     'Pairwise comparison for evaluating the importance degree of criteria for severity measurement'),
        ui.output_data_frame('pc2'),
        ui.input_action_button("pc2submit", "Consistency Check", disabled=True, class_="btn btn-primary", width='200px')
    ),

    ui.card(
        ui.help_text(ui.card_header("[C] Criteria Evaluation"),
                     'Evaluate the exposure and detectability of identified safety risks'),

    ui.HTML("""
                <p>
                Please evaluate the exposure and detectability by answering the following two questions: <br>
                [1] Exposure:  To what extent workers are exposed to the safety risk? <br>
                [2] Detectability: To what extent the safety risk could be detected by relative workers? <br>
                 </p>
                """
        ),
        ui.output_data_frame('ce')
    ),

    ui.div(
        ui.download_button("submit", "Submit", disabled=True, class_="btn btn-primary"),
        class_="d-flex justify-content-end",
    ),
)

def server(input: Inputs, output: Outputs, session: Session):
    input_validator = InputValidator()
    input_validator.add_rule("role", check.required())
    input_validator.add_rule("years", check.required())
    input_validator.add_rule("education", check.required())

    @output
    @render.data_frame
    def pc1():
        df = pd.DataFrame(index=range(4),
                          columns=['Criteria', 'probability', 'severity', 'exposure', 'detectability'])

        df_with_buttons = df.copy()

        df_with_buttons['Criteria'] = ['probability', 'severity', 'exposure', 'detectability']
        for i in range(4):
            for j in range(1, 5):
                if i+1 < j:
                    df_with_buttons.iloc[i, j] = ui.input_select(f"pc1_{i}{j}", label='', choices=choices)
                elif i + 1 == j :
                    df_with_buttons.iloc[i, j] = ui.input_select(f"pc1_{i}{j}", label='', choices={"A": "Equal"})

        return df_with_buttons

    @reactive.effect
    @reactive.event(input.pc1submit)
    def pc1_result():
        pc1_matrix = np.eye(4)
        pc1_matrix[0, 1] = int_fraction(input.pc1_02())
        pc1_matrix[0, 2] = int_fraction(input.pc1_03())
        pc1_matrix[0, 3] = int_fraction(input.pc1_04())
        pc1_matrix[1, 2] = int_fraction(input.pc1_13())
        pc1_matrix[1, 3] = int_fraction(input.pc1_14())
        pc1_matrix[2, 3] = int_fraction(input.pc1_24())

        for i in range(1, 4):
            for j in range(i):
                pc1_matrix[i, j] = 1 / pc1_matrix[j, i]
        cr = ahp_analysis(pc_result=pc1_matrix)[0]
        if cr > 0.1:  # Inconsistent pairwise comparison
            ui.notification_show(
                "The pairwise comparison matrix is inconsistent and please adjust!",
                type='error',
                duration=5,
            )
        else:
            ui.notification_show(
                f"The pairwise comparison matrix is consistent with CR value calculated as {cr}",
                type='message',
                duration=5,
            )

    @output
    @render.data_frame
    def pc2():
        df = pd.DataFrame(index=range(4),
                          columns=['Criteria', 'No. of total injuries', 'No. of total fatalities', 'Average injury rate', 'Average fatality rate'])

        df_with_buttons = df.copy()

        df_with_buttons['Criteria'] = ['No. of total injuries', 'No. of total fatalities', 'Average injury rate', 'Average fatality rate']
        for i in range(4):
            for j in range(1, 5):
                if i+1 < j:
                    df_with_buttons.iloc[i, j] = ui.input_select(f"pc2_{i}{j}", label='', choices=choices)
                elif i + 1 == j :
                    df_with_buttons.iloc[i, j] = ui.input_select(f"pc2_{i}{j}", label='', choices={"A": "Equal"})
        return df_with_buttons

    @reactive.effect
    @reactive.event(input.pc2submit)
    def pc2_result():
        pc2_matrix = np.eye(4)
        pc2_matrix[0, 1] = int_fraction(input.pc2_02())
        pc2_matrix[0, 2] = int_fraction(input.pc2_03())
        pc2_matrix[0, 3] = int_fraction(input.pc2_04())
        pc2_matrix[1, 2] = int_fraction(input.pc2_13())
        pc2_matrix[1, 3] = int_fraction(input.pc2_14())
        pc2_matrix[2, 3] = int_fraction(input.pc2_24())
        for i in range(1, 4):
            for j in range(i):
                pc2_matrix[i, j] = 1 / pc2_matrix[j, i]
        cr = ahp_analysis(pc_result=pc2_matrix)[0]
        if cr > 0.1: # Inconsistent pairwise comparison
            ui.notification_show(
                "The pairwise comparison matrix is inconsistent and please adjust!",
                type='error',
                duration=5,
            )
        else:
            ui.notification_show(
                f"The pairwise comparison matrix is consistent with CR value calculated as {cr}",
                type='message',
                duration=5,
            )

    @output
    @render.data_frame
    def ce():
        df = pd.DataFrame(index=range(len(risk)),
                          columns=['Safety risks', 'exposure', 'detectability'])

        df_with_buttons = df.copy()
        df_with_buttons['Safety risks'] = [f'R{i} {rp}' for i, rp in enumerate(list(risk['Risk descriptions']))]
        for i in range(len(risk)):
            for j, rp in enumerate(['exposure', 'detectability']):
                if rp=='exposure':
                    df_with_buttons.loc[i, rp] = ui.input_select(f"ce_{i}{j}", label='', choices=frequency_scales)
                if rp=='detectability':
                    df_with_buttons.loc[i, rp] = ui.input_select(f"ce_{i}{j}", label='', choices=detectability_scales)
        return df_with_buttons

    @render.download()
    def submit():
        # calculate the weights
        pc1_matrix = np.eye(4)
        pc1_matrix[0, 1] = int_fraction(input.pc1_02())
        pc1_matrix[0, 2] = int_fraction(input.pc1_03())
        pc1_matrix[0, 3] = int_fraction(input.pc1_04())
        pc1_matrix[1, 2] = int_fraction(input.pc1_13())
        pc1_matrix[1, 3] = int_fraction(input.pc1_14())
        pc1_matrix[2, 3] = int_fraction(input.pc1_24())

        for i in range(1, 4):
            for j in range(i):
                pc1_matrix[i, j] = 1 / pc1_matrix[j, i]
        weights_b1 = ahp_analysis(pc_result=pc1_matrix)[1]

        pc2_matrix = np.eye(4)
        pc2_matrix[0, 1] = int_fraction(input.pc2_02())
        pc2_matrix[0, 2] = int_fraction(input.pc2_03())
        pc2_matrix[0, 3] = int_fraction(input.pc2_04())
        pc2_matrix[1, 2] = int_fraction(input.pc2_13())
        pc2_matrix[1, 3] = int_fraction(input.pc2_14())
        pc2_matrix[2, 3] = int_fraction(input.pc2_24())
        for i in range(1, 4):
            for j in range(i):
                pc2_matrix[i, j] = 1 / pc2_matrix[j, i]

        weights_b2 = ahp_analysis(pc_result=pc2_matrix)[1]

        exposure = [input.ce_00(),
                    input.ce_10(),
                    input.ce_20(),
                    input.ce_30(),
                    input.ce_40(),
                    input.ce_50(),
                    input.ce_60(),
                    input.ce_70(),
                    input.ce_80(),
                    input.ce_90(),
                    input.ce_100(),
                    input.ce_110(),
                    input.ce_120(),
                    input.ce_130(),
                    input.ce_140(),
                    input.ce_150(),
                    input.ce_160(),
                    input.ce_170(),
                    input.ce_180(),
                    input.ce_190(),
                    input.ce_200(),
                    input.ce_210()]

        detectability = [input.ce_01(),
                    input.ce_11(),
                    input.ce_21(),
                    input.ce_31(),
                    input.ce_41(),
                    input.ce_51(),
                    input.ce_61(),
                    input.ce_71(),
                    input.ce_81(),
                    input.ce_91(),
                    input.ce_101(),
                    input.ce_111(),
                    input.ce_121(),
                    input.ce_131(),
                    input.ce_141(),
                    input.ce_151(),
                    input.ce_161(),
                    input.ce_171(),
                    input.ce_181(),
                    input.ce_191(),
                    input.ce_201(),
                    input.ce_211()]

        data = [[input.role(), input.years(), input.education(), weights_b1.tolist(), weights_b2.tolist(), exposure, detectability]]
        df = pd.DataFrame(data, columns=['Role',
                                         'Years of experience',
                                         'Education level',
                                         'Parameters_w',
                                         'Severity_w',
                                         'Exposure_e',
                                         'Detectability_e'])
        file_name = generate_random_str() + "_response.csv"
        df.to_csv(file_name, mode="a", header=True, index=False)

        ui.modal_show(ui.modal("Your response has been recorded!Thank you!"))
        return file_name

    # update button states
    @reactive.effect
    def update_consistency_pc1():
        if 'N/A' not in [input.pc1_02(),
                     input.pc1_03(),
                     input.pc1_04(),
                     input.pc1_13(),
                     input.pc1_14(),
                     input.pc1_24()]:
            ui.update_action_button(id='pc1submit', disabled=False)

    @reactive.effect
    def update_consistency_pc2():
        if 'N/A' not in [input.pc2_02(),
                         input.pc2_03(),
                         input.pc2_04(),
                         input.pc2_13(),
                         input.pc2_14(),
                         input.pc2_24()]:
            ui.update_action_button(id='pc2submit', disabled=False)

    @reactive.effect()
    def update_submit_button():
        exposure = [input.ce_00(),
                    input.ce_10(),
                    input.ce_20(),
                    input.ce_30(),
                    input.ce_40(),
                    input.ce_50(),
                    input.ce_60(),
                    input.ce_70(),
                    input.ce_80(),
                    input.ce_90(),
                    input.ce_100(),
                    input.ce_110(),
                    input.ce_120(),
                    input.ce_130(),
                    input.ce_140(),
                    input.ce_150(),
                    input.ce_160(),
                    input.ce_170(),
                    input.ce_180(),
                    input.ce_190(),
                    input.ce_200(),
                    input.ce_210()]

        detectability = [input.ce_01(),
                         input.ce_11(),
                         input.ce_21(),
                         input.ce_31(),
                         input.ce_41(),
                         input.ce_51(),
                         input.ce_61(),
                         input.ce_71(),
                         input.ce_81(),
                         input.ce_91(),
                         input.ce_101(),
                         input.ce_111(),
                         input.ce_121(),
                         input.ce_131(),
                         input.ce_141(),
                         input.ce_151(),
                         input.ce_161(),
                         input.ce_171(),
                         input.ce_181(),
                         input.ce_191(),
                         input.ce_201(),
                         input.ce_211()]

        if ('N/A' not in [input.pc2_02(),
                         input.pc2_03(),
                         input.pc2_04(),
                         input.pc2_13(),
                         input.pc2_14(),
                         input.pc2_24(),
                         input.pc2_02(),
                         input.pc2_03(),
                         input.pc2_04(),
                         input.pc2_13(),
                         input.pc2_14(),
                         input.pc2_24()]
                + detectability + exposure
        ):
            ui.update_action_button(id='submit', disabled=False)



app = App(app_ui, server)
app.run()