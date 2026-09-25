import os
import random
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

QUIZ_SIZES = {20, 40, 60, 80, 100}
LECTURES = ["intro", "presentation", "pbl", "group"]

sessions = {}


def tg(method, payload):
    return requests.post(
        f"{API}/{method}",
        json=payload,
        timeout=10
    ).json()


def shuffle_copy(items):
    items = items[:]
    random.shuffle(items)
    return items


def build_quiz(size):
    each = size // 4
    picked = []

    for lecture in LECTURES:
        pool = [
            i for i, q in enumerate(QUESTIONS)
            if q["lecture"] == lecture
        ]

        random.shuffle(pool)
        picked.extend(pool[:each])

    random.shuffle(picked)
    return picked


def option_order(question):
    order = list(range(len(question["options"])))

    if question["type"] != "tf":
        random.shuffle(order)

    return order


def menu_markup():
    return {
        "inline_keyboard": [
            [
                {"text": "20", "callback_data": "s|20"},
                {"text": "40", "callback_data": "s|40"},
                {"text": "60", "callback_data": "s|60"}
            ],
            [
                {"text": "80", "callback_data": "s|80"},
                {"text": "100", "callback_data": "s|100"}
            ]
        ]
    }


def show_menu(chat_id):
    result = tg(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": (
                "Learning Skills Quiz\n\n"
                "How many questions do you want?"
            ),
            "reply_markup": menu_markup()
        }
    )

    if result.get("ok"):
        sessions[chat_id] = {
            "message_id": result["result"]["message_id"],
            "mode": "menu"
        }QUESTIONS = [

    # ================= INTRODUCTION =================

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "In teacher-centered learning, who mainly controls the material and the way students study it?",
        "options": [
            "The students",
            "The teacher",
            "The study group",
            "The assessment committee"
        ],
        "answer": 1,
        "explanation": "In teacher-centered learning, the teacher controls what, when, where, how, and at what pace students learn."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "In student-centered learning, students are actively involved in learning.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Student-centered learning actively involves students in the learning process."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Which statement best describes student-centered learning?",
        "options": [
            "Students receive information passively",
            "The teacher is the only source of knowledge",
            "Learning addresses the distinct needs and aspirations of students",
            "Students must all learn at exactly the same pace"
        ],
        "answer": 2,
        "explanation": "Student-centered learning addresses the distinct learning needs and aspirations of students."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "In teacher-centered learning, students mainly receive information passively.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Students mainly receive information passively in teacher-centered learning."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "What is the main role of the teacher in student-centered learning?",
        "options": [
            "The only source of knowledge",
            "A facilitator to different sources of knowledge",
            "A passive observer",
            "Only an examiner"
        ],
        "answer": 1,
        "explanation": "The teacher acts as a facilitator to various sources of knowledge, skills, and practices."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "Student-centered learning encourages students to become self-directed learners.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "With facilitation from teachers, students become self-directed learners."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Learning was described in the lecture as a transformative process involving:",
        "options": [
            "Memorization only",
            "Input, process, and reflection",
            "Testing only",
            "Listening without application"
        ],
        "answer": 1,
        "explanation": "Learning is based on input, process, and reflection."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "A learner is considered to have learned when they can apply and use information they have memorized.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "The lecture emphasizes application and use of information."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "An autonomous person is able to:",
        "options": [
            "Depend completely on the teacher",
            "Make judgments based on values, preferences, and beliefs",
            "Avoid making decisions",
            "Learn only through lectures"
        ],
        "answer": 1,
        "explanation": "An autonomous person can make judgments and actions based on personal values, preferences, and beliefs."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Which is one of the principles of adult learning?",
        "options": [
            "Provide a respectful and comfortable learning environment",
            "Prevent learners from expressing concerns",
            "Avoid learner participation",
            "Set all goals without learner involvement"
        ],
        "answer": 0,
        "explanation": "Adult learners should feel safe and comfortable expressing ideas, concerns, and queries."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Engaging learners in identifying their own learning needs mainly helps increase:",
        "options": [
            "Internal motivation",
            "Dependence",
            "Competition",
            "Passive learning"
        ],
        "answer": 0,
        "explanation": "Identifying learning needs helps bring about internal motivation."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "Adult learners should participate in deciding curricular content and delivery methodology.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Learner participation in curricular content and delivery methodology is a principle of adult learning."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Encouraging learners to set their own learning objectives helps them:",
        "options": [
            "Take control of their learning",
            "Avoid responsibility",
            "Depend more on the teacher",
            "Become passive"
        ],
        "answer": 0,
        "explanation": "Setting personal learning objectives helps learners take control of learning."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "Supporting learners in identifying learning resources is a principle of adult learning.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Learners should identify appropriate resources and ways to utilize them."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Encouraging learners to evaluate their own work mainly develops:",
        "options": [
            "Critical appreciation",
            "Passive reception",
            "Teacher dependence",
            "Memorization only"
        ],
        "answer": 0,
        "explanation": "Self-evaluation fosters critical appreciation."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Information enters the brain through three main routes according to the lecture:",
        "options": [
            "Sight, hearing, and touch",
            "Reading, writing, and speaking",
            "Taste, smell, and balance",
            "Memory, logic, and emotion"
        ],
        "answer": 0,
        "explanation": "The lecture lists sight, hearing, and touch."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "A student who benefits from charts, maps, notes, and flash cards is most likely:",
        "options": [
            "Auditory",
            "Visual",
            "Tactile",
            "Interpersonal"
        ],
        "answer": 1,
        "explanation": "Charts, maps, notes, and flash cards are useful strategies for visual learners."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "Visual learners mainly learn by hearing.",
        "options": ["True", "False"],
        "answer": 1,
        "explanation": "Visual learners primarily learn by sight."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Which behavior is most characteristic of an auditory learner?",
        "options": [
            "Prefers to hear information",
            "Learns mainly by touch",
            "Uses only diagrams",
            "Avoids lectures"
        ],
        "answer": 0,
        "explanation": "Auditory learners prefer hearing information."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "Auditory learners may read aloud to themselves.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Reading aloud is listed as a characteristic of auditory learners."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Which activity best suits a tactile or kinesthetic learner?",
        "options": [
            "Role-playing",
            "Listening only",
            "Watching diagrams only",
            "Reading silently only"
        ],
        "answer": 0,
        "explanation": "Role-playing and hands-on activity benefit tactile or kinesthetic learners."
    },

    {
        "lecture": "intro",
        "type": "tf",
        "q": "Tactile learners may benefit from writing important facts and creating study sheets.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Both strategies are listed for tactile or kinesthetic learners."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "An intrapersonal learner is also described as:",
        "options": [
            "A social learner",
            "A solitary or self learner",
            "A number-smart learner",
            "A word-smart learner"
        ],
        "answer": 1,
        "explanation": "Intrapersonal means solitary or self learner."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "A linguistic learner is also described as:",
        "options": [
            "Word smart",
            "Number smart",
            "Body smart",
            "Social smart"
        ],
        "answer": 0,
        "explanation": "Linguistic learners are described as word smart."
    },

    {
        "lecture": "intro",
        "type": "mcq",
        "q": "Using a combination of learning styles is classified as:",
        "options": [
            "Mix",
            "Logical only",
            "Visual only",
            "Auditory only"
        ],
        "answer": 0,
        "explanation": "Mix means a combination of learning styles."
    },    # ================= PRESENTATION =================

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Presentation is not only about delivering information. It is also about:",
        "options": [
            "Influencing, engaging, and inspiring the audience",
            "Using as many slides as possible",
            "Avoiding interaction",
            "Reading written material only"
        ],
        "answer": 0,
        "explanation": "Effective presentations influence, engage, and inspire the audience."
    },

    {
        "lecture": "presentation",
        "type": "tf",
        "q": "A good idea may not be accepted if it is presented poorly.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "A good idea may not be accepted if presented poorly."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Presentation skills include all of the following EXCEPT:",
        "options": [
            "Structure",
            "Slide design",
            "Tone of voice",
            "Ignoring body language"
        ],
        "answer": 3,
        "explanation": "Body language is an important component of presentation skills."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Why is structure important in a presentation?",
        "options": [
            "It creates logical flow",
            "It makes the presentation longer",
            "It removes the need to prepare",
            "It replaces the purpose"
        ],
        "answer": 0,
        "explanation": "Structure creates a logical flow that helps the audience follow."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "To determine your presentation purpose, you should ask:",
        "options": [
            "What main points should my audience take away?",
            "How many animations should I use?",
            "How can I avoid questions?",
            "How can I fill every slide?"
        ],
        "answer": 0,
        "explanation": "The presentation purpose is based on what the audience should take away."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Audience pre-assessment identifies the audience's:",
        "options": [
            "Characteristics, knowledge, and needs",
            "Favorite color",
            "Number only",
            "Age only"
        ],
        "answer": 0,
        "explanation": "Audience characteristics, knowledge, and needs should be identified."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "The opening or bridge should primarily:",
        "options": [
            "Grab audience attention",
            "Present all details",
            "Replace the closing",
            "Give references only"
        ],
        "answer": 0,
        "explanation": "The opening should grab audience attention."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "The major portion of a presentation is the:",
        "options": ["Opening", "Body", "Closing", "Title"],
        "answer": 1,
        "explanation": "The body is the major portion of a presentation."
    },

    {
        "lecture": "presentation",
        "type": "tf",
        "q": "The body should support points clearly and concisely.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Points should be supported clearly and concisely."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "The closing should:",
        "options": [
            "Connect back to the purpose",
            "Introduce unrelated topics",
            "Leave the audience confused",
            "Avoid key points"
        ],
        "answer": 0,
        "explanation": "The closing reconnects to the purpose."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "According to the 10-20-30 rule, the recommended number of slides is:",
        "options": ["5", "10", "20", "30"],
        "answer": 1,
        "explanation": "The rule recommends 10 slides."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "In the 10-20-30 rule, 20 refers to:",
        "options": ["Slides", "Minutes", "Font size", "Audience members"],
        "answer": 1,
        "explanation": "20 refers to minutes."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "In the 10-20-30 rule, 30 refers to:",
        "options": ["Slides", "Minutes", "Font size", "Questions"],
        "answer": 2,
        "explanation": "30 refers to font size."
    },

    {
        "lecture": "presentation",
        "type": "tf",
        "q": "Limiting slides may help manage the audience's cognitive load.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Limiting slides can help manage cognitive load."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Which are examples of visual aids?",
        "options": [
            "Images",
            "Videos",
            "Illustrations",
            "All of the above"
        ],
        "answer": 3,
        "explanation": "Images, videos, and illustrations are visual aids."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Which body-language behavior is recommended?",
        "options": [
            "Make eye contact without staring",
            "Avoid eye contact",
            "Slouch",
            "Keep a blank face"
        ],
        "answer": 0,
        "explanation": "Eye contact is recommended without staring."
    },

    {
        "lecture": "presentation",
        "type": "tf",
        "q": "Facial expressions should match the tone of your words.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Facial expressions should match the tone."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Which can help reduce presentation fear?",
        "options": [
            "Getting organized",
            "Avoiding preparation",
            "Ignoring materials",
            "Reading every slide"
        ],
        "answer": 0,
        "explanation": "Getting organized can reduce presentation fear."
    },

    {
        "lecture": "presentation",
        "type": "tf",
        "q": "A presenter should read a script word for word.",
        "options": ["True", "False"],
        "answer": 1,
        "explanation": "A presenter should not read a script word for word."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Practicing in front of a mirror helps you observe:",
        "options": [
            "Facial expressions, gestures, and movements",
            "Only slide colors",
            "Only timing",
            "Only audience size"
        ],
        "answer": 0,
        "explanation": "Mirror practice helps observe expressions, gestures, and movements."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Recording yourself presenting helps you:",
        "options": [
            "Review your delivery and improve it",
            "Avoid learning your voice",
            "Eliminate practice",
            "Ignore body language"
        ],
        "answer": 0,
        "explanation": "Recording helps review and improve delivery."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Working on breathing may help:",
        "options": [
            "Reduce stress and improve clarity",
            "Increase tension",
            "Cause a monotone voice",
            "Replace preparation"
        ],
        "answer": 0,
        "explanation": "Breathing exercises can reduce stress and improve clarity."
    },

    {
        "lecture": "presentation",
        "type": "tf",
        "q": "Practicing with another person and asking for honest critique is recommended.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Receiving honest critique is recommended."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Which is a common presentation mistake?",
        "options": [
            "Reading directly from a slide",
            "Practicing",
            "Making eye contact",
            "Getting organized"
        ],
        "answer": 0,
        "explanation": "Reading directly from slides is a common mistake."
    },

    {
        "lecture": "presentation",
        "type": "mcq",
        "q": "Which combination contains only common presentation mistakes?",
        "options": [
            "Overloading slides, monotone voice, ignoring time",
            "Eye contact, practice, organization",
            "Visual aids, breathing, preparation",
            "Structure, purpose, audience assessment"
        ],
        "answer": 0,
        "explanation": "Overloading slides, monotone voice, and ignoring time are common mistakes."
    },


    # ================= PBL =================

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Problem-Based Learning was pioneered by Barrows and Tamblyn at:",
        "options": [
            "McMaster University",
            "Harvard University",
            "Oxford University",
            "Princess Nourah University"
        ],
        "answer": 0,
        "explanation": "PBL was pioneered at McMaster University."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "PBL is best described as:",
        "options": [
            "A student-centered approach using carefully constructed problems",
            "A teacher-centered lecture",
            "A memorization technique",
            "An examination method"
        ],
        "answer": 0,
        "explanation": "PBL is a student-centered instructional approach."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "In PBL, students define their own learning needs.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Students identify their learning needs in PBL."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "PBL integrates theory with practice.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "PBL promotes integration of theory and practice."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Which is an advantage of PBL?",
        "options": [
            "Active learning is enhanced",
            "Students become dependent",
            "Group interaction is prevented",
            "SDL is eliminated"
        ],
        "answer": 0,
        "explanation": "PBL enhances active learning."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "PBL may help students retain knowledge for a longer time.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Longer knowledge retention is an advantage of PBL."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Which is a possible disadvantage of PBL?",
        "options": [
            "It can be time-consuming",
            "There are no assessment challenges",
            "It eliminates group issues",
            "It guarantees deep learning"
        ],
        "answer": 0,
        "explanation": "PBL can be time-consuming."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "Potential superficial learning is a possible disadvantage of PBL.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Potential superficial learning is a possible disadvantage."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "The major difference between PBL and problem solving is that in PBL:",
        "options": [
            "The problem comes first",
            "Knowledge is always taught first",
            "Knowledge is never applied",
            "There are no learning needs"
        ],
        "answer": 0,
        "explanation": "In PBL, the problem comes first."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "A PBL facilitator must always be a content expert.",
        "options": ["True", "False"],
        "answer": 1,
        "explanation": "Content expertise is not always necessary for effective facilitation."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Which is a facilitator role?",
        "options": [
            "Create a safe environment",
            "Give ready-made learning objectives",
            "Dominate discussion",
            "Prevent feedback"
        ],
        "answer": 0,
        "explanation": "Creating a safe environment is a facilitator role."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "The facilitator helps students frame learning objectives but should not give ready-made objectives.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "The facilitator guides rather than supplies ready-made objectives."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Which behavior should a tutor avoid?",
        "options": [
            "Over-participating and directing",
            "Monitoring group progress",
            "Creating a safe climate",
            "Giving feedback"
        ],
        "answer": 0,
        "explanation": "Over-participating and directing should be avoided."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Which is a role of the leader?",
        "options": [
            "Group organization and task distribution",
            "Recording all ideas as scribe",
            "Giving ready-made objectives",
            "Avoiding discussion"
        ],
        "answer": 0,
        "explanation": "The leader organizes the group and distributes tasks."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "The leader should encourage quiet colleagues to participate.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Encouraging quiet colleagues is a leader role."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Which is a role of the scribe?",
        "options": [
            "Listen carefully and record ideas",
            "Control all discussion",
            "Assign grades",
            "Avoid participating"
        ],
        "answer": 0,
        "explanation": "The scribe records and organizes ideas."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "Leader and scribe roles should rotate every session.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Roles should rotate so members practice different roles."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Other PBL group members should:",
        "options": [
            "Participate actively in all steps",
            "Only observe",
            "Study only one objective",
            "Avoid feedback"
        ],
        "answer": 0,
        "explanation": "All members should participate actively."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "One of the first steps of PBL is:",
        "options": [
            "Clarifying difficult terms",
            "Giving mini-lectures",
            "Taking an exam",
            "Skipping the problem"
        ],
        "answer": 0,
        "explanation": "Clarifying difficult terms is an early PBL step."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "During brainstorming, students use:",
        "options": [
            "Existing knowledge and experience",
            "Only tutor answers",
            "Only textbooks",
            "Only memorized definitions"
        ],
        "answer": 0,
        "explanation": "Brainstorming uses existing knowledge and experience."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Learning issues are:",
        "options": [
            "Questions that cannot be answered with current group knowledge",
            "Facts everyone already knows",
            "Tutor-provided answers",
            "Unrelated topics"
        ],
        "answer": 0,
        "explanation": "Learning issues represent gaps in current knowledge."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "Each student should study all learning goals, not just the one assigned to them.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Each student should study all learning goals."
    },

    {
        "lecture": "pbl",
        "type": "tf",
        "q": "Mini-lectures from students are encouraged during the reporting phase.",
        "options": ["True", "False"],
        "answer": 1,
        "explanation": "Mini-lectures should be avoided."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "According to Malcolm Knowles, SDL includes all EXCEPT:",
        "options": [
            "Diagnosing learning needs",
            "Formulating learning goals",
            "Identifying learning resources",
            "Waiting passively for the teacher"
        ],
        "answer": 3,
        "explanation": "SDL requires learner initiative."
    },

    {
        "lecture": "pbl",
        "type": "mcq",
        "q": "Readiness for SDL includes:",
        "options": [
            "Desire for learning, self-control, and self-management",
            "Competition and dependence",
            "Only exam marks",
            "Only tutor guidance"
        ],
        "answer": 0,
        "explanation": "Readiness includes desire for learning, self-control, and self-management."
    },


    # ================= GROUP DYNAMICS =================

    {
        "lecture": "group",
        "type": "mcq",
        "q": "A group is best described as individuals who have:",
        "options": [
            "Regular contact, interaction, mutual influence, companionship, and common goals",
            "No interaction",
            "Only occasional contact",
            "No common goals"
        ],
        "answer": 0,
        "explanation": "These characteristics describe a group."
    },

    {
        "lecture": "group",
        "type": "tf",
        "q": "Frequent interaction is a characteristic of a group.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Frequent interaction is a characteristic of a group."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Group dynamics refers to:",
        "options": [
            "Interactions that influence attitudes and behavior in a group",
            "Only group size",
            "An examination system",
            "Individual learning"
        ],
        "answer": 0,
        "explanation": "Group dynamics concern interactions influencing attitudes and behavior."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "What is the correct sequence of group stages?",
        "options": [
            "Forming, Storming, Norming, Performing, Mourning",
            "Storming, Forming, Performing, Norming, Mourning",
            "Forming, Norming, Storming, Mourning, Performing",
            "Performing, Forming, Storming, Norming, Mourning"
        ],
        "answer": 0,
        "explanation": "The stages are Forming, Storming, Norming, Performing, and Mourning."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "During Forming, members are usually:",
        "options": [
            "Uncertain about their roles",
            "Working with high trust",
            "In strong competition",
            "Resisting group termination"
        ],
        "answer": 0,
        "explanation": "Members may be uncertain about their roles during Forming."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "During Forming, the tutor helps build:",
        "options": [
            "Trust and acceptance",
            "Competition",
            "Conflict",
            "Dependence"
        ],
        "answer": 0,
        "explanation": "The tutor helps build trust and acceptance."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Storming is characterized by:",
        "options": [
            "Competition and conflict",
            "Complete harmony",
            "Group termination",
            "No interaction"
        ],
        "answer": 0,
        "explanation": "Storming often includes competition and conflict."
    },

    {
        "lecture": "group",
        "type": "tf",
        "q": "Conflict during Storming can be a normal and healthy development.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Conflict during Storming can be normal."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "During Storming, the tutor should:",
        "options": [
            "Recognize and normalize conflicts",
            "Ignore all conflicts",
            "Encourage unfairness",
            "Stop discussion"
        ],
        "answer": 0,
        "explanation": "The tutor should recognize and normalize conflict."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Norming is characterized by:",
        "options": [
            "Cohesion and exchange of ideas",
            "Maximum conflict",
            "Role uncertainty",
            "Group dissolution"
        ],
        "answer": 0,
        "explanation": "Norming involves cohesion and exchange of ideas."
    },

    {
        "lecture": "group",
        "type": "tf",
        "q": "During Norming, students become more independent.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Students become more independent during Norming."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "During Norming, the tutor:",
        "options": [
            "Can be less active but should continue monitoring",
            "Must dominate",
            "Should disappear completely",
            "Should encourage competition"
        ],
        "answer": 0,
        "explanation": "The tutor can be less active while continuing to monitor."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Performing is characterized by:",
        "options": [
            "High trust and effective teamwork",
            "Role uncertainty",
            "Beginning conflict",
            "Group termination"
        ],
        "answer": 0,
        "explanation": "Performing involves high trust and effective teamwork."
    },

    {
        "lecture": "group",
        "type": "tf",
        "q": "During Performing, group energy is directed primarily toward the task.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Energy is primarily directed toward the task."
    },

    {
        "lecture": "group",
        "type": "tf",
        "q": "All groups necessarily reach the Performing stage.",
        "options": ["True", "False"],
        "answer": 1,
        "explanation": "Not all groups reach the Performing stage."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "During Mourning, members may:",
        "options": [
            "Resist moving on to a new group",
            "Begin learning roles for the first time",
            "Begin Storming",
            "Stop social interaction"
        ],
        "answer": 0,
        "explanation": "Members may resist moving on to a new group."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "During Mourning, the tutor should:",
        "options": [
            "Normalize the transition",
            "Force the group to stay together",
            "Ignore the situation",
            "Increase competition"
        ],
        "answer": 0,
        "explanation": "The tutor should recognize and normalize the transition."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Maintenance of good group dynamics means:",
        "options": [
            "Building and nurturing relationships",
            "Avoiding feedback",
            "Keeping members isolated",
            "Removing ground rules"
        ],
        "answer": 0,
        "explanation": "Maintenance involves building and nurturing relationships."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Which is a common issue in a PBL group?",
        "options": [
            "The quiet group member",
            "The perfectly functioning group",
            "The group with no task",
            "The group with no members"
        ],
        "answer": 0,
        "explanation": "A quiet group member can be a common group issue."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Which is another common PBL group issue?",
        "options": [
            "The dominating group member",
            "The reflective member",
            "The punctual member",
            "The supportive member"
        ],
        "answer": 0,
        "explanation": "A dominating group member is a common issue."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Which helps maintain good group dynamics?",
        "options": [
            "Making and keeping ground rules",
            "Discouraging trust",
            "Avoiding feedback",
            "Preventing reflection"
        ],
        "answer": 0,
        "explanation": "Ground rules help maintain good group dynamics."
    },

    {
        "lecture": "group",
        "type": "tf",
        "q": "Trust and openness are vital for successful group functioning.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Trust and openness are important for group functioning."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Ground rules are useful because they:",
        "options": [
            "Create a safe environment and clarify expectations",
            "Prevent contributions",
            "Increase competition",
            "Remove responsibility"
        ],
        "answer": 0,
        "explanation": "Ground rules create safety and clarify expectations."
    },

    {
        "lecture": "group",
        "type": "tf",
        "q": "Ground rules can both prevent and solve group problems.",
        "options": ["True", "False"],
        "answer": 0,
        "explanation": "Ground rules can help prevent and resolve problems."
    },

    {
        "lecture": "group",
        "type": "mcq",
        "q": "Which advice is given to students working in groups?",
        "options": [
            "Learn to share rather than compete",
            "Compare constantly with other groups",
            "Never admit you do not know something",
            "Immediately solve the PBL case"
        ],
        "answer": 0,
        "explanation": "Students should learn to share rather than compete."
    }

]def render_question(chat_id, feedback=""):
    state = sessions[chat_id]

    question = QUESTIONS[
        state["ids"][state["pos"]]
    ]

    if state.get("order") is None:
        state["order"] = option_order(question)

    text = ""

    if feedback:
        text += feedback
        text += "\n\n--------------------\n\n"

    text += (
        "Learning Skills Quiz\n\n"
        f"Question {state['pos'] + 1} / {len(state['ids'])}"
        f"\n\n{question['q']}"
    )

    if question["type"] == "tf":
        text += "\n\nTrue or False?"

        keyboard = [[
            {
                "text": "True",
                "callback_data": f"a|{state['pos']}|0"
            },
            {
                "text": "False",
                "callback_data": f"a|{state['pos']}|1"
            }
        ]]

    else:
        letters = ["A", "B", "C", "D"]

        for shown_index, original_index in enumerate(state["order"]):
            text += (
                f"\n\n{letters[shown_index]}. "
                f"{question['options'][original_index]}"
            )

        keyboard = [[
            {
                "text": "A",
                "callback_data": f"a|{state['pos']}|0"
            },
            {
                "text": "B",
                "callback_data": f"a|{state['pos']}|1"
            },
            {
                "text": "C",
                "callback_data": f"a|{state['pos']}|2"
            },
            {
                "text": "D",
                "callback_data": f"a|{state['pos']}|3"
            }
        ]]

    tg(
        "editMessageText",
        {
            "chat_id": chat_id,
            "message_id": state["message_id"],
            "text": text,
            "reply_markup": {
                "inline_keyboard": keyboard
            }
        }
    )


def start_quiz(chat_id, message_id, size):
    if size not in QUIZ_SIZES:
        return

    sessions[chat_id] = {
        "message_id": message_id,
        "mode": "quiz",
        "ids": build_quiz(size),
        "pos": 0,
        "score": 0,
        "order": None
    }

    render_question(chat_id)


def handle_answer(chat_id, data):
    if chat_id not in sessions:
        return

    state = sessions[chat_id]

    if state.get("mode") != "quiz":
        return

    parts = data.split("|")

    if len(parts) != 3:
        return

    old_position = int(parts[1])
    displayed_choice = int(parts[2])

    if old_position != state["pos"]:
        return

    question = QUESTIONS[
        state["ids"][state["pos"]]
    ]

    actual_choice = state["order"][displayed_choice]

    correct = actual_choice == question["answer"]

    if correct:
        state["score"] += 1

    if correct:
        feedback = "Correct!"
    else:
        feedback = (
            "Incorrect.\n"
            "Correct answer: "
            + question["options"][question["answer"]]
        )

    feedback += (
        "\n\nExplanation: "
        + question["explanation"]
    )

    state["pos"] += 1
    state["order"] = None

    if state["pos"] >= len(state["ids"]):
        state["mode"] = "done"

        total = len(state["ids"])

        percent = round(
            state["score"] / total * 100
        )

        tg(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": state["message_id"],
                "text": (
                    feedback
                    + "\n\n====================\n\n"
                    + "Quiz finished!\n\n"
                    + f"Score: {state['score']} / {total}"
                    + f"\n\nPercentage: {percent}%"
                    + "\n\nSend /start to try again."
                )
            }
        )

        return

    render_question(chat_id, feedback)


@app.route("/", methods=["GET"])
def home():
    return "Learning Skills Quiz Bot is running", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(force=True)

    if "message" in update:
        message = update["message"]

        chat_id = message["chat"]["id"]

        text = str(
            message.get("text", "")
        ).strip()

        if (
            text == "/start"
            or text.startswith("/start@")
            or text == "/quiz"
            or text.startswith("/quiz@")
        ):
            show_menu(chat_id)

        return "OK", 200


    if "callback_query" in update:
        callback = update["callback_query"]

        tg(
            "answerCallbackQuery",
            {
                "callback_query_id": callback["id"]
            }
        )

        chat_id = callback["message"]["chat"]["id"]

        message_id = callback["message"]["message_id"]

        data = str(
            callback.get("data", "")
        )

        if data.startswith("s|"):
            size = int(
                data.split("|")[1]
            )

            start_quiz(
                chat_id,
                message_id,
                size
            )

        elif data.startswith("a|"):
            handle_answer(
                chat_id,
                data
            )

    return "OK", 200


if __name__ == "__main__":
    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
