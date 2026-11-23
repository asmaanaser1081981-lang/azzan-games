
import streamlit as st
import random

st.set_page_config(
    page_title="عالم عزّان للألعاب",
    page_icon="🎮",
    layout="wide"
)

# ---------- التصميم ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f4f8ff, #fff5fb, #f3fff8);
}
h1, h2, h3, p {
    text-align: center;
}
div.stButton > button {
    border-radius: 15px;
    min-height: 55px;
    font-size: 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- بيانات الجلسة ----------
defaults = {
    "score": 0,
    "game": None,
    "quiz_index": 0,
    "quiz_answer": None,
    "word_index": 0,
    "word_done": False,
    "cards": [],
    "open_cards": [],
    "matched": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- عنوان الموقع ----------
st.title("🎮 عالم عزّان للألعاب التعليمية")
st.subheader("🌟 العب • تعلم • اكتشف")

st.markdown(
    f"""
    <div style="
        background:white;
        padding:18px;
        border-radius:20px;
        text-align:center;
        border:2px solid #ffe29a;
        font-size:26px;
        font-weight:bold;">
        🏆 نقاطك: {st.session_state.score}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ---------- القائمة الرئيسية ----------
if st.session_state.game is None:

    st.markdown("## 👇 اختر اللعبة التي تفضلها")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("## 🧠")
        st.markdown("### تحدّي المعلومات")
        st.write("اختبر معلوماتك وأجب عن الأسئلة.")

        if st.button("🚀 ابدأ التحدي", use_container_width=True):
            st.session_state.game = "quiz"
            st.session_state.quiz_index = 0
            st.session_state.quiz_answer = None
            st.rerun()

    with col2:
        st.markdown("## 🔤")
        st.markdown("### خمّن الكلمة")
        st.write("اكتشف الكلمة من خلال التلميح.")

        if st.button("✨ ابدأ التخمين", use_container_width=True):
            st.session_state.game = "word"
            st.session_state.word_index = random.randint(0, 4)
            st.session_state.word_done = False
            st.rerun()

    with col3:
        st.markdown("## 🃏")
        st.markdown("### لعبة الذاكرة")
        st.write("اكتشف الصور المتشابهة وطابقها.")

        if st.button("🎯 ابدأ اللعب", use_container_width=True):
            cards = ["🐱", "🐶", "🦁", "🐸",
                     "🐱", "🐶", "🦁", "🐸"]
            random.shuffle(cards)
            st.session_state.cards = cards
            st.session_state.open_cards = []
            st.session_state.matched = []
            st.session_state.game = "memory"
            st.rerun()

# ---------- تحدي المعلومات ----------
if st.session_state.game == "quiz":

    questions = [
        {
            "q": "ما الكوكب الذي نعيش عليه؟",
            "options": ["المريخ", "الأرض", "زحل"],
            "answer": "الأرض"
        },
        {
            "q": "ما الحيوان الذي يسمى ملك الغابة؟",
            "options": ["الفيل", "الأسد", "الأرنب"],
            "answer": "الأسد"
        },
        {
            "q": "كم عدد أيام الأسبوع؟",
            "options": ["5 أيام", "6 أيام", "7 أيام"],
            "answer": "7 أيام"
        },
        {
            "q": "ما العضو الذي نستخدمه للرؤية؟",
            "options": ["الأذن", "العين", "الأنف"],
            "answer": "العين"
        },
        {
            "q": "أي مادة يجذبها المغناطيس؟",
            "options": ["الخشب", "الحديد", "البلاستيك"],
            "answer": "الحديد"
        }
    ]

    st.header("🧠 تحدّي المعلومات")

    index = st.session_state.quiz_index

    if index < len(questions):

        q = questions[index]

        st.progress(index / len(questions))
        st.markdown(f"### السؤال {index + 1} من {len(questions)}")
        st.markdown(f"## {q['q']}")

        if st.session_state.quiz_answer is None:

            for option in q["options"]:
                if st.button(
                    option,
                    key=f"quiz_{index}_{option}",
                    use_container_width=True
                ):
                    st.session_state.quiz_answer = option

                    if option == q["answer"]:
                        st.session_state.score += 10

                    st.rerun()

        else:

            if st.session_state.quiz_answer == q["answer"]:
                st.success("🎉 إجابة صحيحة! حصلت على 10 نقاط")
            else:
                st.info(f"الإجابة الصحيحة هي: {q['answer']}")

            if st.button("➡️ السؤال التالي", use_container_width=True):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answer = None
                st.rerun()

    else:
        st.balloons()
        st.success("🏆 انتهى التحدي! أحسنت يا عزّان!")
        st.markdown(f"## مجموع نقاطك: {st.session_state.score}")

        if st.button("🔄 إعادة التحدي"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_answer = None
            st.rerun()

# ---------- لعبة تخمين الكلمة ----------
if st.session_state.game == "word":

    words = [
        {"word": "مدرسة", "hint": "مكان نتعلم فيه"},
        {"word": "مغناطيس", "hint": "يجذب بعض المعادن"},
        {"word": "فراشة", "hint": "حشرة جميلة لها أجنحة"},
        {"word": "برتقال", "hint": "فاكهة لونها برتقالي"},
        {"word": "قمر", "hint": "يظهر في السماء ليلًا"}
    ]

    item = words[st.session_state.word_index]

    st.header("🔤 خمّن الكلمة")
    st.markdown("### 💡 التلميح")
    st.markdown(f"## {item['hint']}")

    if not st.session_state.word_done:

        answer = st.text_input("✏️ اكتب الكلمة هنا")

        if st.button("🔍 تحقق من الإجابة", use_container_width=True):

            if answer.strip() == item["word"]:
                st.session_state.score += 10
                st.session_state.word_done = True
                st.success("🎉 أحسنت! إجابة صحيحة!")
                st.rerun()
            else:
                st.error("❌ حاول مرة أخرى!")

    else:
        st.success("🎉 الكلمة الصحيحة هي: " + item["word"])

        if st.button("🔄 كلمة جديدة", use_container_width=True):
            st.session_state.word_index = random.randint(0, 4)
            st.session_state.word_done = False
            st.rerun()

# ---------- لعبة الذاكرة ----------
if st.session_state.game == "memory":

    st.header("🃏 لعبة الذاكرة")
    st.write("اضغط على بطاقتين وحاول العثور على الصور المتطابقة.")

    cols = st.columns(4)

    for i in range(8):

        with cols[i % 4]:

            if i in st.session_state.matched:
                label = st.session_state.cards[i]
            elif i in st.session_state.open_cards:
                label = st.session_state.cards[i]
            else:
                label = "❓"

            if st.button(label, key=f"card_{i}", use_container_width=True):

                if (
                    i not in st.session_state.matched
                    and i not in st.session_state.open_cards
                    and len(st.session_state.open_cards) < 2
                ):
                    st.session_state.open_cards.append(i)

                    if len(st.session_state.open_cards) == 2:
                        a, b = st.session_state.open_cards

                        if st.session_state.cards[a] == st.session_state.cards[b]:
                            st.session_state.matched.extend([a, b])
                            st.session_state.score += 10
                            st.session_state.open_cards = []

                    st.rerun()

    if len(st.session_state.matched) == 8:
        st.balloons()
        st.success("🎉 رائع! وجدت جميع الصور المتطابقة!")
        st.markdown(f"## 🏆 نقاطك: {st.session_state.score}")

    elif len(st.session_state.open_cards) == 2:
        st.warning("البطاقتان غير متطابقتين؟ اضغط إخفاء البطاقتين ثم تابع.")

        if st.button("🙈 إخفاء البطاقتين", use_container_width=True):
            st.session_state.open_cards = []
            st.rerun()

    if st.button("🔄 إعادة لعبة الذاكرة", use_container_width=True):
        cards = ["🐱", "🐶", "🦁", "🐸",
                 "🐱", "🐶", "🦁", "🐸"]
        random.shuffle(cards)
        st.session_state.cards = cards
        st.session_state.open_cards = []
        st.session_state.matched = []
        st.rerun()

# ---------- العودة للقائمة ----------
if st.session_state.game is not None:

    if st.button("🏠 العودة إلى الألعاب", use_container_width=True):
        st.session_state.game = None
        st.rerun()

st.divider()

# ---------- تصفير النقاط ----------
if st.button("🗑️ تصفير النقاط", use_container_width=True):
    st.session_state.score = 0
    st.session_state.game = None
    st.session_state.quiz_index = 0
    st.session_state.quiz_answer = None
    st.session_state.word_done = False
    st.session_state.matched = []
    st.session_state.open_cards = []
    st.rerun()

st.markdown(
    "<p style='text-align:center;color:#888;'>"
    "✨ موقع عزّان التعليمي | العب وتعلم واستمتع ✨"
    "</p>",
    unsafe_allow_html=True
)
