import sqlite3
import pandas as pd

# Your initial comments list
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

# Create initial DataFrame
df = pd.DataFrame({
    'comment': comments_data,
    'reply': [[] for _ in comments_data],
    'upvotes': [0] * len(comments_data),
    'theme': [0] * len(comments_data),          # dummy placeholders
    'theme_name': [''] * len(comments_data),    # will be set later by app
    'x': [0.0] * len(comments_data),            # will be set by embedding
    'y': [0.0] * len(comments_data),
})

# Save to SQLite
DB_FILE = "comments.db"
TABLE_NAME = "comments"

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
    df['reply'] = df['reply'].apply(str)
    conn.execute(f"DELETE FROM {TABLE_NAME}")  # optional: clear table before insert
    df.to_sql(TABLE_NAME, conn, if_exists='append', index=False)

print(f"Inserted {len(df)} comments into {DB_FILE}.")
