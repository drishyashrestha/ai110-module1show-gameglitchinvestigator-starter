import random
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"


    if guess > secret:
        return "Too High", "📈 Go LOWER!"
    else:
        return "Too Low", "📉 Go HIGHER!"



def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High" or outcome == "Too Low":
        return current_score - 5

    return current_score

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="centered")

# ── Difficulty theme ───────────────────────────────────────────────────────────
difficulty_colors = {"Easy": "#00b894", "Normal": "#0984e3", "Hard": "#d63031"}
difficulty_emojis = {"Easy": "🟢", "Normal": "🔵", "Hard": "🔴"}

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Animated gradient background ── */
@keyframes bgMove {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes floatUp {
    0%   { transform: translateY(0px); opacity: 0.6; }
    50%  { transform: translateY(-18px); opacity: 1; }
    100% { transform: translateY(0px); opacity: 0.6; }
}

.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
    background-size: 400% 400%;
    animation: bgMove 10s ease infinite;
}

/* ── Floating emoji particles ── */
.particles {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.particle {
    position: absolute;
    font-size: 1.4rem;
    animation: floatUp 4s ease-in-out infinite;
    opacity: 0.5;
}

/* ── Game title ── */
.game-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a29bfe, #fd79a8, #fdcb6e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeSlideIn 0.6s ease;
    margin-bottom: 0;
}
.game-subtitle {
    text-align: center;
    color: #a0a8c0;
    font-size: 0.9rem;
    margin-top: 2px;
    margin-bottom: 20px;
}

/* ── Score + attempts bar ── */
.stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
    animation: fadeSlideIn 0.5s ease;
}
.stat-box {
    flex: 1;
    border-radius: 12px;
    padding: 12px 16px;
    text-align: center;
    font-weight: 700;
    font-size: 1.1rem;
    color: #fff;
}

/* ── Hint boxes ── */
.hint-box {
    border-radius: 10px;
    padding: 12px 18px;
    font-weight: 600;
    font-size: 1rem;
    margin: 10px 0;
    animation: fadeSlideIn 0.4s ease;
}
.hint-high  { background: rgba(214, 48, 49, 0.25);  border-left: 4px solid #d63031; color: #ff7675; }
.hint-low   { background: rgba(9, 132, 227, 0.25);  border-left: 4px solid #0984e3; color: #74b9ff; }
.hint-win   { background: rgba(0, 184, 148, 0.25);  border-left: 4px solid #00b894; color: #55efc4; }
.hint-error { background: rgba(253, 121, 168, 0.2); border-left: 4px solid #fd79a8; color: #fd79a8; }

/* ── History badges ── */
.history-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}
.badge {
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #fff;
}

/* ── Range info box ── */
.range-box {
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 0.95rem;
    color: #dfe6e9;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# ── Floating background particles ──────────────────────────────────────────────
st.markdown("""
<div class="particles">
  <span class="particle" style="left:5%;  top:15%; animation-delay:0s;">🎯</span>
  <span class="particle" style="left:20%; top:70%; animation-delay:1s;">⭐</span>
  <span class="particle" style="left:40%; top:30%; animation-delay:2s;">🎲</span>
  <span class="particle" style="left:60%; top:80%; animation-delay:0.5s;">✨</span>
  <span class="particle" style="left:75%; top:20%; animation-delay:1.5s;">🎮</span>
  <span class="particle" style="left:90%; top:60%; animation-delay:3s;">🔢</span>
</div>
""", unsafe_allow_html=True)

# ── Title ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="game-title">🎮 Glitchy Guesser</div>', unsafe_allow_html=True)
st.markdown('<div class="game-subtitle">Can you find the secret number? 🕵️</div>', unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("## ⚙️ Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
    format_func=lambda d: f"{difficulty_emojis[d]} {d}",
)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

color = difficulty_colors[difficulty]
emoji = difficulty_emojis[difficulty]

st.sidebar.markdown(f"""
<div style="background:rgba(255,255,255,0.07); border-radius:10px; padding:12px; margin-top:8px;">
  <div style="color:{color}; font-weight:700; font-size:1rem;">{emoji} {difficulty} Mode</div>
  <div style="color:#b2bec3; font-size:0.85rem; margin-top:4px;">📏 Range: {low} – {high}</div>
  <div style="color:#b2bec3; font-size:0.85rem;">🎯 Attempts: {attempt_limit}</div>
</div>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────────
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

# ── Score + attempts stats ─────────────────────────────────────────────────────
attempts_left = attempt_limit - st.session_state.attempts
attempts_color = "#00b894" if attempts_left > 3 else "#fdcb6e" if attempts_left > 1 else "#d63031"
attempts_rgba = "0,184,148" if attempts_left > 3 else "253,203,110" if attempts_left > 1 else "214,48,49"

st.markdown(f"""
<div class="stat-row">
  <div class="stat-box" style="background:rgba(108,92,231,0.3); border:1px solid #6c5ce7;">
    ⭐ Score<br><span style="font-size:1.5rem;">{st.session_state.score}</span>
  </div>
  <div class="stat-box" style="background:rgba({attempts_rgba},0.3); border:1px solid {attempts_color};">
    🎯 Attempts Left<br><span style="font-size:1.5rem;">{attempts_left}</span>
  </div>
  <div class="stat-box" style="background:rgba(9,132,227,0.3); border:1px solid {color};">
    {emoji} Mode<br><span style="font-size:1.1rem;">{low}–{high}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Debug expander ─────────────────────────────────────────────────────────────
with st.expander("🛠️ Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# ── Input + buttons ────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="range-box" style="background:rgba(255,255,255,0.05); border-left: 4px solid {color};">
  🔢 Guess a number between <strong>{low}</strong> and <strong>{high}</strong>
</div>
""", unsafe_allow_html=True)

raw_guess = st.text_input(
    "Enter your guess:",
    placeholder=f"Pick a number between {low} and {high}...",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("🚀 Submit Guess", use_container_width=True)
with col2:
    new_game = st.button("🔁 New Game", use_container_width=True)
with col3:
    show_hint = st.checkbox("💡 Show hint", value=True)

# ── New game ───────────────────────────────────────────────────────────────────
if new_game:
    st.session_state.attempts = 1
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.markdown('<div class="hint-box hint-win">🔁 New game started — good luck!</div>', unsafe_allow_html=True)
    st.rerun()

# ── Game over states ───────────────────────────────────────────────────────────
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.markdown('<div class="hint-box hint-win">🏆 You already won! Start a new game to play again.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hint-box hint-error">💀 Game over. Start a new game to try again.</div>', unsafe_allow_html=True)
    st.stop()

# ── Submit logic ───────────────────────────────────────────────────────────────
if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.markdown(f'<div class="hint-box hint-error">⚠️ {err}</div>', unsafe_allow_html=True)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            if outcome == "Too High":
                st.markdown(f'<div class="hint-box hint-high">{message}</div>', unsafe_allow_html=True)
            elif outcome == "Too Low":
                st.markdown(f'<div class="hint-box hint-low">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="hint-box hint-win">{message}</div>', unsafe_allow_html=True)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.markdown(f"""
<div class="hint-box hint-win" style="font-size:1.1rem;">
  🎉 You won! The secret was <strong>{st.session_state.secret}</strong>.<br>
  🏆 Final score: <strong>{st.session_state.score}</strong>
</div>
""", unsafe_allow_html=True)
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.markdown(f"""
<div class="hint-box hint-error" style="font-size:1.1rem;">
  💀 Out of attempts! The secret was <strong>{st.session_state.secret}</strong>.<br>
  📊 Final score: <strong>{st.session_state.score}</strong>
</div>
""", unsafe_allow_html=True)

# ── Guess history ──────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("#### 📜 Guess History")
    badges = ""
    for g in st.session_state.history:
        if g < st.session_state.secret:
            bg = "#0984e3"
            label = f"⬆️ {g}"
        elif g > st.session_state.secret:
            bg = "#d63031"
            label = f"⬇️ {g}"
        else:
            bg = "#00b894"
            label = f"✅ {g}"
        badges += f'<span class="badge" style="background:{bg};">{label}</span>'
    st.markdown(f'<div class="history-row">{badges}</div>', unsafe_allow_html=True)

st.divider()
st.markdown('<div style="text-align:center; color:#636e72; font-size:0.8rem;">🤖 Built by an AI that claims this code is production-ready.</div>', unsafe_allow_html=True)
