import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

# from jupyter_dash import JupyterDash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
from flask_cors import CORS

app = Dash(__name__)
server = app.server
CORS(server)

df1 = pd.read_csv('../Sentiment & Engagement Datasets/ready_data_score.csv')

df2 = pd.read_csv('../Sentiment & Engagement Datasets/subreddit_flair_data.csv')

df3 = pd.read_csv('../Sentiment & Engagement Datasets/engagement_metrics_by_sentiment.csv')
df4 = pd.read_csv('../Sentiment & Engagement Datasets/engagement_metrics_by_day_and_sentiment.csv')
df5 = pd.read_csv('../Sentiment & Engagement Datasets/top_performing_posts.csv')
df6 = pd.read_csv('../Sentiment & Engagement Datasets/low_performing_posts.csv')
df7 = pd.read_csv('../Sentiment & Engagement Datasets/avg_sentiment_scores.csv')

order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']

unique_subreddits = df2['subreddit'].unique()

subreddit_flair_mapping = {
    'careeradvice': 'category_careeradvice',
    'resumes': 'category_resumes',
    'ITCareerQuestions': 'category_ITCareerQuestions',
    'FinancialCareers': 'category_FinancialCareers',
    'LegalAdviceOffTopic': 'category_LegalAdviceOffTopic',
    'teachers': 'category_teachers',
    'AskHR': 'category_AskHR',
    'sales': 'category_sales',
    'careerguidance': 'category_careerguidance',
    'jobs': 'category_jobs',
    'cscareerquestions': 'category_cscareerquestions'
}

# Function to apply consistent styling to all hists
def style_histogram(fig, title, xaxis_title, yaxis_title='Count'):
    color_discrete_sequence = px.colors.qualitative.Pastel1
    fig.update_traces(marker_line_width=1, marker_color=color_discrete_sequence[0], 
                      marker_line_color='blue')
    fig.update_layout(
        title_text=title,
        title_font_size=18,
        xaxis=dict(
            title=xaxis_title,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightPink'
        ),
        yaxis=dict(
            title=yaxis_title,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightPink'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell")
    )
    return fig

fig_avg_sentiment = px.bar(
    df7, 
    x='subreddit', 
    y=['Low-Performing', 'Top-Performing'], 
    barmode='group',
    title="Average Sentiment Scores for Top vs. Low Performing Posts by Subreddit"
)

# Main app layout with tabs
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Sentiment Score Distribution Analysis', value='tab-1', children=[
            html.Div([
                html.H1("Sentiment Score Distribution Analysis", style={'textAlign': 'center'}),
                html.Div([
                    html.H2("Filter by:"),
                    html.Div([
                        html.H3("Year"),
                        dcc.Checklist(
                            id='year-checklist',
                            options=[{'label': str(year), 'value': year} for year in sorted(df1['year'].unique())],
                            value=[],
                            labelStyle={'display': 'block'}
                        ),
                    ]),
                    html.Div([
                        html.H3("Month"),
                        dcc.Checklist(
                            id='month-checklist',
                            options=[{'label': month, 'value': month} for month in months_order if month in df1['month'].unique()],
                            value=[],
                            labelStyle={'display': 'block'}
                        ),
                    ]),
                    html.Div([
                        html.H3("Day of the Week"),
                        dcc.Checklist(
                            id='day-checklist',
                            options=[{'label': day, 'value': day} for day in order],
                            value=[],
                            labelStyle={'display': 'block'}
                        ),
                    ]),
                ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                html.Div([
                    html.H2("Sentiment Score Distribution by Time of Day", style={'textAlign': 'center'}),
                    html.P("This plot displays the spread of sentiment scores across different hours of the day. Use the filters to customize the data view by year, month, and day of the week.", style={'textAlign': 'center'}),
                    dcc.Graph(id='sentiment-distribution-plot'),
                ], style={'width': '80%', 'display': 'inline-block'}),
            ])
        ]),
        dcc.Tab(label='Subreddit Engagement Analysis', value='tab-2', children=[
            html.Div([
                html.H1("Subreddit to Flair - Engagement Distribution Analysis", style={'textAlign': 'center', 'marginBottom': '1em'}),
                html.H2("Subreddit-Level Engagement"),
                html.P("Select a subreddit from the dropdown to view the distribution of engagement metrics like the number of comments and score. Logarithmic transformations are applied for a better visual representation of the distribution, and outlier detection highlights posts with unusually high engagement."),
        
                html.Div([
                    html.Label("Select a Subreddit:", style={'fontSize': '18px', 'marginTop': '10px'}),
                    dcc.Dropdown(
                        id='subreddit-dropdown',
                        options=[{'label': subreddit, 'value': subreddit} for subreddit in unique_subreddits],
                        value=unique_subreddits[0],  
                        clearable=False,
                        searchable=True,
                        placeholder="Select a subreddit",
                    ),
                ], style={'width': '30%', 'display': 'inline-block'}),
        
                html.Div([
                    html.Label("Choose a Visualization Type:", style={'fontSize': '18px', 'marginTop': '10px'}),
                    dcc.Dropdown(
                        id='visual-dropdown',
                        options=[
                            {'label': 'Histogram', 'value': 'hist'},
                            {'label': 'Violin Plot', 'value': 'violin'}
                        ],
                        value='hist',  
                        clearable=False,
                        searchable=False,
                        placeholder="Select a visual type",
                    ),
                ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '20px'}),

                html.Div(id='subreddit-visualization-container'),

                html.H2("Flair-Level Engagement"),
                html.P("After selecting a subreddit, choose a flair to drill down into the engagement metrics specific to different content categories within the subreddit. This can provide insights into what types of posts generate the most discussion or receive the highest scores."),
        
                html.Div([
                    html.Label("Select a Flair:", style={'fontSize': '18px', 'marginTop': '10px'}),
                    dcc.Dropdown(
                        id='flair-dropdown',
                        options=[],
                        placeholder="Select a flair",
                        searchable=True,
                        clearable=True  
                    ),
                ], style={'width': '30%', 'display': 'none', 'marginLeft': '20px'}, id='flair-dropdown-container'),

                html.Div(id='flair-visualization-container')
            ])
        ]),
        dcc.Tab(label='Sentiment and Engagement Comparative Analysis', value='tab-3', children=[
            html.Div([
                html.H1("Sentiment and Engagement Comparative Analysis", style={'textAlign': 'center'}),
                html.Div([
                    html.H2("Engagement Metrics by Sentiment Score Categories"),
                    html.P("Explore how different sentiment categories affect engagement metrics."),
                    dcc.Dropdown(
                        id='metric-selector-1',
                        options=[
                            {'label': 'Number of Comments', 'value': 'num_comments'},
                            {'label': 'Upvote Ratio', 'value': 'upvote_ratio'},
                            {'label': 'Score', 'value': 'score'}
                        ],
                        value='num_comments',
                        style={'width': '50%'}
                    ),
                    dcc.Graph(id='engagement-metrics-chart')
                ], style={'padding': '20px'}),

                html.Div([
                    html.H2("Engagement Metrics by Day and Sentiment"),
                    html.P("See how engagement metrics vary by day and sentiment category."),
                    dcc.Dropdown(
                        id='day-metric-selector',
                        options=[
                            {'label': 'Number of Comments', 'value': 'num_comments'},
                            {'label': 'Upvote Ratio', 'value': 'upvote_ratio'},
                            {'label': 'Score', 'value': 'score'}
                        ],
                        value='num_comments',
                        style={'width': '50%'}
                    ),
                    dcc.Graph(id='day-engagement-chart')
                ], style={'padding': '20px'}),

                html.Div([
                    html.H2("Distribution Analysis of Sentiment Scores"),
                    html.P("Analyze the distribution of sentiment scores for top-performing vs. low-performing posts."),
                    dcc.Dropdown(
                        id='subreddit-selector',
                        options=[{'label': x, 'value': x} for x in pd.concat([df5['subreddit'], df6['subreddit']]).unique()],
                        value=None,
                        style={'width': '50%'}
                    ),
                    dcc.Graph(id='sentiment-distribution-chart')
                ], style={'padding': '20px'}),

                html.Div([
                    html.H3("Average Sentiment Scores for Top vs. Low Performing Posts by Subreddit"),
                    dcc.Graph(id='avg-sentiment-chart', figure=fig_avg_sentiment)
                ])
            ])
        ]),
        dcc.Tab(label='Static Visuals', value='tab-4', children=[
            html.Div([
                html.H1("Static Visual Content", style={'textAlign': 'center'}),
                html.Img(src='path_to_image.jpg'),
                html.P("Description of the static visual content.")
            ])
        ])
    ])
])

@app.callback(
    Output('sentiment-distribution-plot', 'figure'),
    [Input('year-checklist', 'value'),
     Input('month-checklist', 'value'),
     Input('day-checklist', 'value')]
)

#the function
def update_graph(selected_years, selected_months, selected_days):
    
    filtered_df = df1[df1['year'].isin(selected_years) & df1['month'].isin(selected_months) & df1['day_of_week'].isin(selected_days)]
    
    
    
    fig = px.box(filtered_df, x='hour_of_day', y='sentiment_score',

                 points="all", 
                 custom_data=['created_datetime', 'day_of_week', 'year', 'month'])
    #hover data
    fig.update_traces(
    hovertemplate="<br>".join([
        "Datetime: %{customdata[0]}",
        "Day: %{customdata[1]}",
        "Year: %{customdata[2]}",
        "Month: %{customdata[3]}",
        "Hour: %{x}",
        "Sentiment: %{y:.2f}"
    ]),
        marker=dict(color='LightSkyBlue', outliercolor='rgba(219, 64, 82, 0.6)', 
                line=dict(outliercolor='rgba(219, 64, 82, 0.6)', outlierwidth=2)),
    boxmean='sd'
        
    )
    
    fig.update_layout(
    xaxis=dict(title='Hour of Day', showgrid=True, gridwidth=1, gridcolor='LightPink'),
    yaxis=dict(title='Sentiment Score', showgrid=True, gridwidth=1, gridcolor='LightPink'),
    paper_bgcolor='rgb(243, 243, 243)',  
    plot_bgcolor='rgb(243, 243, 243)',  
    showlegend=False,
    width=800,
    height=600, 
)
   
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
    
    
    return fig
    
@app.callback(
    [Output('flair-dropdown', 'options'),
     Output('flair-dropdown-container', 'style')],
    [Input('subreddit-dropdown', 'value')]
)
def update_flair_dropdown_options(subreddit):
    if not subreddit or subreddit not in subreddit_flair_mapping:
       
        return [], {'display': 'none'}
    
    # Use the mapping to get the correct flair column for the selected subreddit
    flair_column = subreddit_flair_mapping.get(subreddit)
    if flair_column:
        # Extract unique flairs from this column
        unique_flairs = df2[flair_column].dropna().unique()
        flair_options = [{'label': flair, 'value': flair} for flair in unique_flairs]
        
        # Return the options for the dropdown and make the container visible
        return flair_options, {'display': 'block', 'width': '30%', 'marginLeft': '20px'}
    else:
        
        return [], {'display': 'none'}


    
#subreddit level callback setup    
@app.callback(
    Output('subreddit-visualization-container', 'children'),
    [Input('subreddit-dropdown', 'value'),
     Input('visual-dropdown', 'value')]
)
def update_subreddit_visuals(subreddit, visual_type):
    
    filtered_df = df2[df2['subreddit'] == subreddit]
    
    if visual_type == 'hist':
        fig_log_comments = style_histogram(
            px.histogram(filtered_df, x='log_num_comments'),
            'Log of Number of Comments',
            'Logarithmic Number of Comments'
        )
        fig_log_score = style_histogram(
            px.histogram(filtered_df, x='log_score'),
            'Log of Score',
            'Logarithmic Score'
        )
        
    elif visual_type == 'violin':
        fig_log_comments = px.violin(filtered_df, y='log_num_comments', box=True, points="all", title='Log of Number of Comments')
        fig_log_score = px.violin(filtered_df, y='log_score', box=True, points="all", title='Log of Score')
    # Prepare visuals for outliers

    outliers_comments = filtered_df[filtered_df['outlier_num_comments']]
    outliers_score = filtered_df[filtered_df['outlier_score']]
    
    if visual_type == 'hist':
        fig_outliers_comments = style_histogram(
            px.histogram(filtered_df[filtered_df['outlier_num_comments']], x='num_comments'),
            'Outliers: Number of Comments',
            'Number of Comments'
        )
        fig_outliers_score = style_histogram(
            px.histogram(filtered_df[filtered_df['outlier_score']], x='score'),
            'Outliers: Score',
            'Score'
        )
        
    elif visual_type == 'violin':
        fig_outliers_comments = px.violin(outliers_comments, y='num_comments', box=True, points="all", title='Outliers: Number of Comments')
        fig_outliers_score = px.violin(outliers_score, y='score', box=True, points="all", title='Outliers: Score')



    return html.Div([
        html.Div([dcc.Graph(figure=fig_log_comments)], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([dcc.Graph(figure=fig_outliers_comments)], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([dcc.Graph(figure=fig_log_score)], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([dcc.Graph(figure=fig_outliers_score)], style={'display': 'inline-block', 'width': '50%'})
    ])



#flair_level callback setup
@app.callback(
    Output('flair-visualization-container', 'children'),
    [Input('subreddit-dropdown', 'value'),
     Input('flair-dropdown', 'value')]
)
def update_flair_visuals(subreddit, flair):
    # Check if a subreddit and flair are selected
    if not subreddit or not flair:
       
        return []

    # Use the mapping to get the correct flair column for the selected subreddit
    flair_column = subreddit_flair_mapping.get(subreddit)
    
    # Filter DataFrame based on selected flair within the selected subreddit
    if flair_column:
        filtered_df = df2[df2[flair_column] == flair]
    else:
        
        return []

    # hists
    fig_log_comments = style_histogram(
        px.histogram(filtered_df, x='log_num_comments'),
        f'Log of Number of Comments for {flair} in {subreddit}',
        'Logarithmic Number of Comments'
    )
    fig_log_score = style_histogram(
        px.histogram(filtered_df, x='log_score'),
        f'Log of Score for {flair} in {subreddit}',
        'Logarithmic Score'
    )
    fig_outliers_comments = style_histogram(
        px.histogram(filtered_df[filtered_df['outlier_num_comments']], x='num_comments'),
        f'Outliers: Number of Comments for {flair} in {subreddit}',
        'Number of Comments'
    )
    fig_outliers_score = style_histogram(
        px.histogram(filtered_df[filtered_df['outlier_score']], x='score'),
        f'Outliers: Score for {flair} in {subreddit}',
        'Score'
    )

    
    return html.Div([
        html.Div([dcc.Graph(figure=fig_log_comments)], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([dcc.Graph(figure=fig_outliers_comments)], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([dcc.Graph(figure=fig_log_score)], style={'display': 'inline-block', 'width': '50%'}),
        html.Div([dcc.Graph(figure=fig_outliers_score)], style={'display': 'inline-block', 'width': '50%'})
    ])
    

@app.callback(
    Output('engagement-metrics-chart', 'figure'),
    Input('metric-selector-1', 'value')
)
def update_engagement_metrics_chart(selected_metric):
    fig = px.bar(df3, x='sentiment_category', y=selected_metric, color='sentiment_category', 
                 title="Engagement Metrics by Sentiment Score Categories")
    return fig

#for section two

@app.callback(
    Output('day-engagement-chart', 'figure'),
    Input('day-metric-selector', 'value')
)
def update_day_engagement_chart(selected_metric):
    fig = px.line(df4, x='day_of_week', y=selected_metric, color='sentiment_category', 
                  title="Engagement Metrics by Day and Sentiment")
    return fig

#for section three

@app.callback(
    Output('sentiment-distribution-chart', 'figure'),
    [Input('subreddit-selector', 'value')]
)
def update_sentiment_distribution_chart(selected_subreddit):
    if selected_subreddit is not None:
        
        filtered_top = df5[df5['subreddit'] == selected_subreddit].copy()
        filtered_low = df6[df6['subreddit'] == selected_subreddit].copy()

        # Combine the filtered df
        filtered_top['Performance'] = 'Top-Performing'
        filtered_low['Performance'] = 'Low-Performing'
        combined_df = pd.concat([filtered_top, filtered_low])

        # create the hist
        fig = px.histogram(
            combined_df, 
            x='sentiment_score', 
            color='Performance', 
            barmode='overlay', 
            nbins=50,  
            title=f"Sentiment Scores Distribution for {selected_subreddit}"
        )
        fig.update_layout(bargap=0.1)  
        return fig
    else:
        return go.Figure()
    
    
if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=8050)
