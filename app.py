import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime, timedelta

# Assuming 'data' is a DataFrame with your tasks following the structure provided in the images


# Creating a DataFrame based on the provided internship planning structure
data = {
    'Cycle': ['Preparation', 'Cycle 1 Personal planning and analysis', 'Cycle 2 Department analysis',
              'Cycle 3 Organisation analysis', 'Survey', 'Q&A session', 'Cycle 4 Professional analysis',
              'Interim appraisal', 'Cycle 4 Professional analysis', 'Cycle 5 Context analysis',
              'Cycle 6 Reflection and evaluation', 'Assessment', 'Completion', 'Internship grade'],
    'When': ['Week 0', 'Week 2', 'Week 5', 'Week 9', 'Week 10', 'Week 10', 'Week 10/11', 'Week 11/12',
             'Week 12', 'Week 15', 'Week 17', 'Week 19', 'Week 20/21', 'Week 20/21'],
    'What': [
        'Send IPF to IS, Introductory meeting with IS, Schedule meeting with IS',
        'Overview deliverables, Personal Internship Plan, Plan an introductory meeting with IS and CC',
        'Department Analysis, Report Company Communication, Matrix final portfolio report',
        'Business Canvas Model, Justification report',
        'Fill in and return internship survey',
        'Online Q&A session',
        '360-Feedback form, Interim appraisal form, Interim performance report (part 1 and 2)',
        'Interim appraisal meeting',
        'Complete interim performance report (part 3 and 4)',
        'Sustainability Scan, Justification Report, Report Company Culture',
        'Draft version final portfolio report, Final internship portfolio report',
        'Criterium Based Interview',
        'Assessment form and grade',
        'Grade in Osiris'
    ],
    'Who': [
        'Student/IS', 'Student, approved by IS', 'Student', 'Student', 'Student', 'Student', 
        '1 Colleague, CC, Student', 'Student, CC, IS', 'Student', 'Student', 'Student, CC', 'Student CC, IS',
        'IS', 'IS'
    ],
    'How': [
        'In person/Teams', 'Email/Teams', 'Email/Teams', 'Email/Teams', 'Upload via link', 'Online',
        'Email/Teams', 'In person/Teams', 'Email/Teams', 'Email/Teams', 'Email/Teams, HandIn', 
        'In person/Teams', 'HandIn', 'HandIn'
    ]
}

data = pd.DataFrame(data)

# Displaying the first few rows of the DataFrame to ensure it's created correctly
data.head()

# Assuming your internship starts on a specific date
internship_start_date = datetime(2024, 1, 22)

def calculate_deadline(week_number):
    start_date = internship_start_date + timedelta(weeks=week_number)
    end_date = start_date + timedelta(weeks=1)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")



app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Internship Task Tracker"),
    
    html.Div([
        html.Div([
            html.H2("Cycle"),
            dcc.Dropdown(
                id='cycle-dropdown',
                options=[{'label': cycle, 'value': cycle} for cycle in data['Cycle'].unique()],
                value=data['Cycle'].unique()[0],
                style={'width': '100%'}
            ),
            html.Div(id='selected-cycle', style={'marginTop': '20px', 'fontSize': '20px'})  # Placeholder for selected cycle
        ], className='three columns'),

        html.Div(id='task-details', className='nine columns'),
    ], className='row')
])

@app.callback(
    Output('task-details', 'children'),
    [Input('cycle-dropdown', 'value')]
)
def update_task_details(selected_cycle):
    current_date = datetime.now().date()  # Get the current date
    cycle_data = data[data['Cycle'] == selected_cycle]

    tasks_layout = []
    for _, row in cycle_data.iterrows():
        week_text = row['When'].split(' ')[1]  # Extracts the week number text, e.g., '10/11'

        # Handle week ranges
        if '/' in week_text:
            start_week, end_week = week_text.split('/')
            start_date, _ = calculate_deadline(int(start_week))
            _, end_date = calculate_deadline(int(end_week))
        else:
            start_date, end_date = calculate_deadline(int(week_text))

        # Check if the deadline is over
        deadline_over = current_date > datetime.strptime(end_date, "%Y-%m-%d").date()

        task_style = {'border': '1px solid black', 'padding': '10px', 'marginBottom': '10px'}
        if deadline_over:
            task_style['backgroundColor'] = '#ffcccc'  # Change background color if deadline is over

        task_layout = html.Div([
            html.H3(row['What']),
            html.P(f"When: {row['When']} (Deadline: {start_date} to {end_date})"),
            html.P(f"Who: {row['Who']}"),
            html.P(f"How: {row['How']}"),
            dcc.Textarea(
                id={'type': 'comment-box', 'index': row['What']},
                placeholder='Enter comments here',
                style={'width': '100%'}
            )
        ], style=task_style)
        tasks_layout.append(task_layout)

    return tasks_layout


if __name__ == '__main__':
    app.run_server(debug=False)


from datetime import datetime, timedelta

# Example usage
week_2_deadline = calculate_deadline(2)  # For Cycle 1
print("Cycle 1 Deadline:", week_2_deadline)