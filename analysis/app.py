import pandas as pd
from shiny import App, ui
from shinywidgets import output_widget, render_widget
from shiny import reactive, render
import analysis

app_ui = ui.page_sidebar(
    ui.sidebar(
              # input zip file of responses
        ui.input_file("zip", "Step 1: upload the zip file of responses", accept=[".zip"], multiple=False, placeholder='.zip file'),
              ui.input_file("csv", "Step 2: upload the quantitative evaluation", accept=[".csv"], multiple=False, placeholder='.csv file'),
              ui.download_link('sample', 'Sample.csv'),
              ui.input_task_button('analyze', 'Analyze!', type='success'),
               bg="#f8f8f8",
               open='always',
               width=400),

        # demographic information
    ui.layout_columns(
             # role
        ui.card(ui.card_header("Roles of respondents"),
                output_widget("role"), height=400),

             # years of experience
              ui.card(ui.card_header("Years of experience of respondents"),
                      output_widget("years"), height=400),

             # educational level
             ui.card(ui.card_header("Educational level of respondents"),
                     output_widget("education"), height=400),
        ),

        # severity and risk magnitude
         ui.layout_columns(
             # severity
        # ui.card(ui.card_header("Severity measurement results"),
        #                    ui.output_data_frame('severity'),
        #                    height=500),

             # risk magnitude
              ui.card(ui.card_header("Risk magnitude measurement results"),
                            ui.output_data_frame('magnitude'),
                            ui.card_footer('Ng=Negligible, Mn=Minor, Mj=Major, Cr=Critical'),
                            height=600),
        ),

    title='Response Analysis'
)

def server(input, output, session):
    @reactive.calc
    def file_unzip():
        file = input.zip()
        if file is not None:
            return analysis.un_zip(file_name=input.zip()[0]['datapath'])

    @render.download
    def sample():
        return 'quantitative_eval.csv'

    # Demographic information
    @render_widget
    @reactive.event(input.analyze)
    def role():
        df = file_unzip()
        return analysis.demographic_pie(df=df, i=0)

    @render_widget
    @reactive.event(input.analyze)
    def years():
        df = file_unzip()
        return analysis.demographic_pie(df=df, i=1)

    @render_widget
    @reactive.event(input.analyze)
    def education():
        df = file_unzip()
        return analysis.demographic_pie(df=df, i=2)

    # Severity measurement results
    @render.data_frame
    @reactive.event(input.analyze)
    def severity():
        df = file_unzip()
        e = pd.read_csv(input.csv()[0]['datapath'])
        return analysis.severity_table(df, e)

    # Risk magnitude measurement results
    @render.data_frame
    @reactive.event(input.analyze)
    def magnitude():
        df = file_unzip()
        e = pd.read_csv(input.csv()[0]['datapath'])
        return analysis.rm_table(df, e)


app = App(app_ui, server)
app.run()