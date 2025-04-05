import streamlit as st
import pandas as pd
import openai
from openai import OpenAI
import plotly.express as px
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@st.cache_data
def get_gpt_labels(comments, labels, n_clusters):
    theme_names = []
    for i in range(n_clusters):
        cluster_texts = [comments[j] for j in range(len(comments)) if labels[j] == i]
        prompt = f"""
        Given the following comments, generate a 5-8 word label that captures key issues, including as many different keywords from the comments as possible. Output nothing but text, without quotes. Comments:
        {cluster_texts}
        Label:
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a semantic expert."},
                {"role": "user", "content": prompt},
            ],
            max_completion_tokens=10000,
            stop="###"
        )
        label = response.choices[0].message.content.strip()
        theme_names.append(label)
    return theme_names

@st.cache_data
def cluster_comments(comments, n_clusters=5):
    if not comments or all(len(c.strip()) == 0 for c in comments):
        raise ValueError("No valid comments for clustering.")
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(comments)
    model = KMeans(n_clusters=n_clusters, random_state=16)
    labels = model.fit_predict(X)
    return labels, X.toarray()

@st.cache_data
def embed_comments(X):
    tsne = TSNE(n_components=2, random_state=42)
    embeddings = tsne.fit_transform(X)
    return embeddings

DB_FILE = "comments.db"
TABLE_NAME = "comments"

def initialize_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment TEXT,
                reply TEXT,
                upvotes INTEGER,
                theme INTEGER,
                theme_name TEXT,
                x REAL,
                y REAL
            )
        ''')
        conn.commit()

def load_comments():
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    df['reply'] = df['reply'].apply(lambda x: eval(x) if isinstance(x, str) else [])
    return df

def save_comments(df):
    df_copy = df.copy()
    df_copy['reply'] = df_copy['reply'].apply(str)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(f"DELETE FROM {TABLE_NAME}")
        df_copy.to_sql(TABLE_NAME, conn, if_exists='append', index=False)

initialize_database()

if 'comments_df' not in st.session_state:
    try:
        st.session_state.comments_df = load_comments()
    except:
        comments_data = [
    "I feel as if the world is fragmented. My need for unity is unmet — I don’t see the big picture, how everything is connected. Take political polarization: I have to manually do the cognitive work of filtering out people's extreme biases before I can extract the relevant information underneath. Nobody seems to agree on anything: as soon as I feel I have epistemic stability, where I have *some* stable foundations to stand on, the rug gets pulled out from under my feet. I don’t know what to believe.",
    "I don’t trust myself. I don’t trust my own instincts or observations or ideas or abilities. I don’t trust my ability to navigate the world — I’m always waiting for some external “objective” authority figure to free me from the burden of trusting my own judgement and the inherent uncertainty it comes with.",
    "I don’t know where I am. I’m an amalgamation of disparate, quickly evolving cultures that don’t give me strong enough answers or beliefs to navigate the world with.",
    "I come up with all these clever ideas and plans for schemes that excite me, but they don’t feel connected. What’s the *point*?",
    "I don’t know what virtue looks like. I feel as if I’m fighting to remember what being a good person looks like when ‘maturity’ and ‘adulthood’ tell me how naive such aspirations are. What is bravery? What is integrity? What is humanity? What do these good things have in common? Does “goodness” even exist?",
    "Most people don’t feel alive. They’re not curious, not responsive, they seem to lack the ability to defy social norms in a way that precludes the ability to act with any individuality. Finding conscious people is difficult.",
    "It feels as if I have too little in common with most people to connect. There are too many conditions that must be met for basic connection. Most people feel like strangers.",
    "I don’t know how to do purposeful work.",
    "I have trouble being heard.",
    "Housing, opportunity for growth, opportunity for clear life development, consistent stability, community and affirmation for self.",
    "Statistically more people are homeless, imprisoned, and addicted to opioids. While fewer people may be uninsured due to Medicaid expansions, the cost of care is skyrocketing. The elderly are also experiencing more of the burden.",
    "Reported mental illness is much greater in Gen Z. Suicide is more common in middle-aged men, but suicide attempts may be greater among women. It's better to look at racial and class disparities than generational ones.",
    "The biggest issue is public safety. Anyone can get a gun and shoot people at will, even in public spaces. This leads to constant vigilance and fear. Second is hard drugs like fentanyl and opioids, which have devastated communities.",
    "The disruption of real conversation and friendship is the primary concern.",
    "Read Tribe: On Homecoming and Belonging by Sebastian Junger for my answer.",
    "Not being under the condition of alienation — the lack of resonance as described by sociologist Hartmut Rosa — is a core unmet need.",
    "Rosa's resonance theory includes four axes: horizontal (relationships with people), diagonal (relationships to activities and objects), vertical (relationships to abstract categories like nature and art), and the self (relation with one's own body and psyche).",
    "Social acceleration creates a dynamic stabilization logic — a need for constant increase in resources, productivity, and innovation — which produces a loss of resonance in modern life.",
    "Modernity creates an ecological crisis (unsustainable extraction of nature), a political crisis (systems too slow to keep up), and a psychological crisis (burnout and overwhelm).",
    "Resonance theory offers a counterpoint to alienation through concepts like recognition, justice, and self-efficacy — emphasizing the need for relational and meaningful connection to the world.",
    "Meaning is elusive in modern Western life — a meaningful existence from the subjective point of view is an unmet, profound need.",
    "Human needs are a powerful source of motivation. Systems that fail to meet these needs are prone to instability and conflict.",
    "Social isolation is exacerbated by algorithmic networks — our digital systems often deepen loneliness.",
    "Loneliness is deeply tied to economic systems — commodification and individualism alienate us from one another.",
    "The three pillars of modernity (science and technology, democracy, capitalism) have diminished the human person as much as they have empowered society.",
    "Science once promised paradise on Earth, but today we live with its unintended consequences: climate change, nuclear risk, and ecological degradation.",
    "Optimism about human progress must be tempered by the insight that every great transformation has also created loss — as Sophocles said, 'Nothing that is vast enters the life of mortals without a curse.'",
    "The Agricultural Revolution was a turning point — it allowed large civilizations but worsened individual lives through worse diets, hierarchical labor, and mass exploitation.",
    "Modern longevity largely results from reduced infant mortality, not necessarily from improved adult well-being.",
    "Democracy gives us freedom, but also isolates us from community — individualism leads to estrangement.",
    "Loneliness is a central experience in modern life. It fuels unhealthy relationships, psychological distress, and addictive behavior.",
    "Promiscuity, often perceived as pleasure-seeking, is frequently an attempt to escape deep loneliness.",
    "American suburbia is designed for privacy at the expense of connection. Neighbors don’t know each other.",
    "Western literature centers loneliness as the human tragedy — unlike Chinese or classical literature, which do not see aloneness as essential to being human.",
    "There is a deep, pervading sickness in modern systems and culture — an output of unrestrained growth, systemic depravity, and deep isolation.",
    "Most people cannot articulate this precisely, but they feel that something fundamental is wrong — that a deep human need is not being met."
]
        st.session_state.comments_df = pd.DataFrame({
            'comment': comments_data,
            'reply': [[] for _ in comments_data],
            'upvotes': [0] * len(comments_data)
        })

comments = st.session_state.comments_df['comment'].tolist()
if not comments or all(len(c.strip()) == 0 for c in comments):
    st.error("No valid comments available for clustering.")
    st.stop()

labels, X = cluster_comments(comments)
embeddings = embed_comments(X)

theme_names = get_gpt_labels(comments, labels, n_clusters=5)

st.session_state.comments_df['theme'] = labels
st.session_state.comments_df['theme_name'] = [theme_names[label] for label in labels]
st.session_state.comments_df['x'] = embeddings[:, 0]
st.session_state.comments_df['y'] = embeddings[:, 1]

st.title("GENZ UNION")
st.markdown("""*Generation Z, along with Millenials, comprise 48.5% of the total electorate of the United States. This means we have significant political power, if we can unite around material issues that we all face. Politicians may want to pit us against each other using partisan or identity rhetoric, but we look around us and we see the material reality: rising education, housing, living costs, stagnating wages, decreasing job opportunities, precarious employment in the face of technological disruption, loneliness pandemic and mental health crises, digital exploitation, ecological destabilization. These are issues that we can unionize and organize around, using our collective political power as a generation to bring about policy changes that ensure our generation can actually have a livable future.*""")
st.success("This platform enables collective reflection and civic discourse around the unmet needs of our generation. Comments are clustered into themes for exploration.")

tab1, tab2, tab3 = st.tabs(["Discussion by Theme", "Theme Map", "Add Your Voice"])

with tab1:
    selected_theme_name = st.selectbox("Explore a theme:", sorted(st.session_state.comments_df['theme_name'].unique()))
    filtered_comments = st.session_state.comments_df[st.session_state.comments_df['theme_name'] == selected_theme_name]

    st.subheader(f"{selected_theme_name}")
    for idx, row in filtered_comments.iterrows():
        st.markdown(f"**User:** {row['comment']}")

        col1, col2 = st.columns([1, 8])
        with col1:
            if st.button(f"⬆️ {row['upvotes']}", key=f"upvote_{idx}"):
                st.session_state.comments_df.at[idx, 'upvotes'] += 1
                save_comments(st.session_state.comments_df)
                st.rerun()
        with col2:

            with st.expander("Reply / View Thread"):
                for r in row['reply']:
                    st.markdown(f"👉 {r}")
                new_reply = st.text_area(f"Write a reply to comment {idx}", key=f"reply_{idx}")
                if st.button(f"Submit Reply to {idx}"):
                    st.session_state.comments_df.at[idx, 'reply'].append(new_reply)
                    save_comments(st.session_state.comments_df)
                    st.success("Reply submitted!")

with tab2:
    st.subheader("Visual Map of Comments by Theme")
    fig = px.scatter(
        st.session_state.comments_df,
        x='x', y='y',
        color='theme_name',
        hover_data=['comment', 'upvotes'],
        title="Embedding Space of Comments with Thematic Clusters"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Add Your Voice")
    new_comment = st.text_area("What is a need you feel is not being met?")
    if st.button("Submit Comment"):
        new_label = cluster_comments([new_comment])[0][0]
        theme_name = get_gpt_labels([new_comment], [new_label], 1)[0]
        new_row = pd.DataFrame({
            'comment': [new_comment],
            'reply': [[]],
            'upvotes': [0],
            'theme': [new_label],
            'theme_name': [theme_name],
            'x': [0],
            'y': [0]
        })
        st.session_state.comments_df = pd.concat([st.session_state.comments_df, new_row], ignore_index=True)
        save_comments(st.session_state.comments_df)
        st.success("Comment submitted and assigned to a theme!")

st.query_params.clear()