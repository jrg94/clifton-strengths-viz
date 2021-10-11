import plotly.graph_objects as go
import pandas as pd

THEMES_DOMAINS = {
    "Adaptability": "Relationship Building",
    "Connectedness": "Relationship Building",
    "Developer": "Relationship Building",
    "Empathy": "Relationship Building",
    "Harmony": "Relationship Building",
    "Includer": "Relationship Building",
    "Individualization": "Relationship Building",
    "Positivity": "Relationship Building",
    "Relator": "Relationship Building",
    "Activator": "Influencing",
    "Command": "Influencing",
    "Communication": "Influencing",
    "Competition": "Influencing",
    "Maximizer": "Influencing",
    "Self-Assurance": "Influencing",
    "Significance": "Influencing",
    "Woo": "Influencing",
    "Analytical": "Strategic Thinking",
    "Context": "Strategic Thinking",
    "Futuristic": "Strategic Thinking",
    "Ideation": "Strategic Thinking",
    "Input": "Strategic Thinking",
    "Intellection": "Strategic Thinking",
    "Learner": "Strategic Thinking",
    "Strategic": "Strategic Thinking",
    "Achiever": "Executing",
    "Arranger": "Executing",
    "Belief": "Executing",
    "Consistency": "Executing",
    "Deliberative": "Executing",
    "Discipline": "Executing",
    "Focus": "Executing",
    "Responsibility": "Executing",
    "Restorative": "Executing",
}

DOMAIN_COLOR = {
    "Strategic Thinking": "green",
    "Relationship Building": "blue",
    "Influencing": "orange",
    "Executing": "purple"
}

def plot_domain(fig, counts, domain):
    domain_data = counts[counts.index.isin(domains_themes[domain])]
    fig.add_trace(go.Barpolar( 
        r=domain_data.values,
        theta=domain_data.index,
        width=[1] * len(domain_data),
        marker_color=DOMAIN_COLOR[domain],
        marker_line_color="black",
        marker_line_width=2,
        opacity=0.8,
        name=domain
    ))

def plot_starburst(df: pd.DataFrame, title: str):
    fig = go.Figure()
    counts = df["Theme"].value_counts()
    for domain in DOMAIN_COLOR.keys():
        plot_domain(fig, counts, domain)
    fig.update_traces(showlegend=True)
    fig.update_layout(
        title={
            'text': title,
            'y': .95
        },
        template=None,
        legend_title="CliftonStrengths Domain",
        polar = dict(
            radialaxis = dict(range=[0, max(counts.values)], showticklabels=False, ticks="", nticks=int(max(counts.values))+1, showline=False),
            angularaxis = dict(categoryarray=list(THEMES_DOMAINS.keys()), nticks=0, tickfont=dict(size=8), ticklen=40)
        )
    )
    return fig

def plot_weighted_starburst(df: pd.DataFrame, title: str):
    fig = go.Figure()
    counts = df.groupby("Theme").sum()["Rank"]
    for domain in DOMAIN_COLOR.keys():
        plot_domain(fig, counts, domain)
    fig.update_traces(showlegend=True)
    fig.update_layout(
        title={
            'text': title,
            'y': .95
        },
        template=None,
        legend_title="CliftonStrengths Domain",
        polar = dict(
            radialaxis = dict(range=[0, max(counts.values)], showticklabels=False, ticks="", nticks=int(max(counts.values))+1, showline=False),
            angularaxis = dict(categoryarray=list(THEMES_DOMAINS.keys()), nticks=0, tickfont=dict(size=8), ticklen=40)
        )
    )
    return fig

def compute_similarity(df: pd.DataFrame):
    selfjoin = pd.merge(df, df, on="Theme")
    similarity = selfjoin.groupby(["Last Name_x", "First Name_x", "Last Name_y", "First Name_y"], as_index=False) \
        .size() \
        .sort_values("size", ascending=False)
    similarity = similarity[similarity["Last Name_x"] != similarity["Last Name_y"]]
    max_similarity = similarity.groupby(["Last Name_x", "First Name_x"]) \
        .first() \
        .sort_values("size", ascending=False)
    similarity.to_csv("similarity.csv")
    max_similarity.to_csv("max_similarity.csv")

if __name__ == "__main__":
    df = pd.read_csv("themes.csv")
    counts = df["Theme"].value_counts()

    domains_themes = dict()
    for key, value in THEMES_DOMAINS.items():
        domains_themes.setdefault(value, list()).append(key)

    df["Rank"] = df["Rank"].map(lambda x: 1 / x)

    # Collective
    fig = plot_starburst(df, "Collective CliftonStrengths Starburst")
    fig.write_image("collective-starburst.png")

    # Weighted Collective
    fig = plot_weighted_starburst(df, "Collective CliftonStrengths Weighted Starburst")
    fig.write_image("weight-collective-starburst.png")

    # CAREER
    career_df = df[df["Last Name"].isin(["Dringenberg", "Grifski", "Wallace", "Delpech"])]
    fig = plot_starburst(career_df, "CAREER CliftonStrengths Starburst")
    fig.write_image("career-starburst.png")

    # EHR
    ehr_df = df[df["Last Name"].isin(["Dringenberg", "Braaten", "Li", "Kramer"])]
    fig = plot_starburst(ehr_df, "EHR Core CliftonStrengths Starburst")
    fig.write_image("ehr-starburst.png")

    # RFE
    rfe_df = df[df["Last Name"].isin(["Dringenberg", "Leonard", "Guanes"])]
    fig = plot_starburst(rfe_df, "RFE CliftonStrengths Starburst")
    fig.write_image("rfe-starburst.png")

    # GTA
    gta_df = df[df["Last Name"].isin(["Guanes", "Leonard", "Grifski", "Opoku"])]
    fig = plot_starburst(gta_df, "GTA CliftonStrengths Starburst")
    fig.write_image("gta-starburst.png")

    compute_similarity(df)
