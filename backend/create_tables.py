from app import create_app
from app.extensions import db
from app.models.question import Question
from app.models.chapter import Chapter
from app.models.quiz import Quiz

app = create_app()

# Realistic questions + options

question_bank = {
    "Data Structures": [
        ("What is a stack?", ["LIFO", "FIFO", "Queue", "Array"], "option1"),
        ("What is a queue?", ["FIFO", "LIFO", "Tree", "Set"], "option1"),
        ("What is a binary tree?", ["Tree with max 2 children", "Unordered list", "Stack", "Circular array"], "option1"),
        ("What is the time complexity of binary search?", ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "option2"),
        ("What is a linked list?", ["Node chain", "Fixed-size array", "Stack", "Heap"], "option1"),
    ],
    "Algorithms": [
        ("What is bubble sort?", ["Comparison-based sort", "Recursion", "Greedy", "DFS"], "option1"),
        ("What is the time complexity of quicksort?", ["O(n²)", "O(n log n)", "O(n)", "O(1)"], "option2"),
        ("What is dynamic programming?", ["Memoization", "Sorting", "Greedy", "Divide and conquer"], "option1"),
        ("What is recursion?", ["Function calling itself", "Loop", "Pointer", "Thread"], "option1"),
        ("What is a greedy algorithm?", ["Locally optimal choices", "Memoized recursion", "Stack usage", "Optimal sorting"], "option1"),
    ],
    "Operating Systems": [
        ("What is a process?", ["Running program", "Memory block", "Queue", "Loop"], "option1"),
        ("What is a thread?", ["Lightweight process", "Memory block", "Variable", "Class"], "option1"),
        ("What is context switching?", ["Switching between processes", "IO operation", "Paging", "Deadlock"], "option1"),
        ("What is deadlock?", ["Processes waiting on each other", "IO wait", "Memory leak", "Infinite loop"], "option1"),
        ("What is virtual memory?", ["Disk-based RAM extension", "Main memory", "Cache", "ROM"], "option1"),
    ],
    "Calculus": [
        ("What is the derivative of x²?", ["2x", "x", "x²", "1"], "option1"),
        ("What is an integral?", ["Area under a curve", "Derivative", "Function", "Limit"], "option1"),
        ("What is a limit?", ["Approaching value", "Exact value", "Infinity", "Slope"], "option1"),
        ("What is the chain rule?", ["Derivative of composed functions", "Summation", "Product rule", "Limit law"], "option1"),
        ("What is a definite integral?", ["Integral with limits", "Indefinite integral", "Partial derivative", "Limit"], "option1"),
    ],
    "Linear Algebra": [
        ("What is a matrix?", ["Rectangular array", "Scalar", "Vector", "Equation"], "option1"),
        ("What is a determinant?", ["Scalar value of square matrix", "Vector norm", "Rank", "Size"], "option1"),
        ("What is an eigenvalue?", ["Scalar λ in Ax=λx", "Matrix inverse", "Diagonal element", "Norm"], "option1"),
        ("What is a vector?", ["Quantity with direction & magnitude", "Scalar", "Matrix", "Point"], "option1"),
        ("What is the rank of a matrix?", ["Max number of linearly independent rows", "Number of columns", "Dimension", "Eigenvalue count"], "option1"),
    ],
    "Probability": [
        ("What is a random variable?", ["Numerical outcome of experiment", "Event", "Constant", "Probability"], "option1"),
        ("What is conditional probability?", ["P(A|B)", "P(A)", "P(A and B)", "P(B)"], "option1"),
        ("What is Bayes' Theorem?", ["P(A|B) = P(B|A)P(A)/P(B)", "P(A) = 1 − P(A')", "Sum Rule", "Multiplication Rule"], "option1"),
        ("What is expected value?", ["Mean of distribution", "Mode", "Median", "Range"], "option1"),
        ("What is variance?", ["Spread around mean", "Average", "Sum", "Product"], "option1"),
    ],
    "Mechanics": [
        ("What is Newton's Second Law?", ["F=ma", "E=mc²", "V=IR", "W=Fd"], "option1"),
        ("What is kinetic energy?", ["½mv²", "mv", "mgh", "F*d"], "option1"),
        ("What is momentum?", ["mv", "½mv²", "ma", "d/t"], "option1"),
        ("What is force?", ["ma", "mv", "½mv²", "m/g"], "option1"),
        ("What is torque?", ["r × F", "F × m", "mv", "ma"], "option1"),
    ],
    "Thermodynamics": [
        ("What is entropy?", ["Measure of disorder", "Energy", "Temperature", "Heat"], "option1"),
        ("What is the first law of thermodynamics?", ["Energy conservation", "Entropy law", "PV=nRT", "ΔG=ΔH−TΔS"], "option1"),
        ("What is heat?", ["Energy transfer due to temp diff", "Mass", "Temperature", "Work"], "option1"),
        ("What is temperature?", ["Measure of avg kinetic energy", "Heat", "Volume", "Entropy"], "option1"),
        ("What is thermal equilibrium?", ["No heat flow", "Max entropy", "Equal mass", "Equal density"], "option1"),
    ],
    "Optics": [
        ("What is refraction?", ["Bending of light", "Splitting", "Reflection", "Absorption"], "option1"),
        ("What is the speed of light?", ["3×10⁸ m/s", "1.5×10⁸ m/s", "3×10⁶ m/s", "1×10⁸ m/s"], "option1"),
        ("What is total internal reflection?", ["Light reflects completely", "Light passes through", "Diffraction", "Refraction"], "option1"),
        ("What is a convex lens?", ["Converging lens", "Diverging", "Flat", "Opaque"], "option1"),
        ("What is dispersion?", ["Splitting of light", "Absorption", "Diffraction", "Reflection"], "option1"),
    ],
    "Organic Chemistry": [
        ("What is an alkane?", ["Saturated hydrocarbon", "Aromatic", "Alcohol", "Acid"], "option1"),
        ("What is an alcohol?", ["OH group", "COOH group", "NH2 group", "CH3"], "option1"),
        ("What is a functional group?", ["Group determining reactivity", "Atom", "Ion", "Electron"], "option1"),
        ("What is aromaticity?", ["Stability due to resonance", "Reactivity", "Acidity", "Basicity"], "option1"),
        ("What is a substitution reaction?", ["Atom replaces another", "Addition", "Elimination", "Oxidation"], "option1"),
    ],
    "Inorganic Chemistry": [
        ("What is a coordination compound?", ["Central atom + ligands", "Salt", "Acid", "Base"], "option1"),
        ("What is periodicity?", ["Repeating trends", "Valence", "Acidity", "Basicity"], "option1"),
        ("What is a transition metal?", ["d-block element", "s-block", "p-block", "f-block"], "option1"),
        ("What is lattice energy?", ["Energy to separate ionic solid", "Bond energy", "Ionization", "Affinity"], "option1"),
        ("What is oxidation state?", ["Charge of atom in compound", "Number of neutrons", "Mass", "Valency"], "option1"),
    ],
    "Physical Chemistry": [
        ("What is the ideal gas law?", ["PV=nRT", "E=mc²", "F=ma", "pV=nkT"], "option1"),
        ("What is the rate of reaction?", ["Change in conc/time", "Equilibrium", "Mass/time", "Energy/time"], "option1"),
        ("What is an electrolyte?", ["Ion-conducting compound", "Covalent", "Metal", "Insulator"], "option1"),
        ("What is Gibbs free energy?", ["ΔG=ΔH−TΔS", "E=mc²", "ΔG=ΔS−TΔH", "PV=nRT"], "option1"),
        ("What is pH?", ["−log[H⁺]", "log[OH⁻]", "H⁺ + OH⁻", "Ka/Kb"], "option1"),
    ],
    "Grammar": [
        ("What is a noun?", ["Person/place/thing", "Action", "Modifier", "Conjunction"], "option1"),
        ("What is a verb?", ["Action word", "Name", "Describer", "Joining word"], "option1"),
        ("What is an adjective?", ["Describes noun", "Describes verb", "Connects phrases", "Action"], "option1"),
        ("What is an adverb?", ["Describes verb/adjective", "Name", "Action", "Person"], "option1"),
        ("What is subject-verb agreement?", ["Verb matches subject", "Noun matches verb", "Tense shift", "Plurality"], "option1"),
    ],
    "Vocabulary": [
        ("What is a synonym of 'happy'?", ["Joyful", "Sad", "Angry", "Confused"], "option1"),
        ("What is an antonym of 'dark'?", ["Bright", "Black", "Dim", "Night"], "option1"),
        ("Which word means 'confident'?", ["Assured", "Nervous", "Doubtful", "Weak"], "option1"),
        ("What is a homonym?", ["Words with same sound", "Opposites", "Synonyms", "Foreign words"], "option1"),
        ("What is a prefix?", ["Beginning part", "Ending", "Root", "Plural"], "option1"),
    ],
    "Reading Comprehension": [
        ("What is the main idea of a passage?", ["Central message", "First line", "Author", "Conclusion"], "option1"),
        ("What does inference mean?", ["Logical guess", "Exact quote", "Opinion", "Prediction"], "option1"),
        ("How do you identify the author’s tone?", ["Language choice", "Font", "Paragraph length", "Punctuation"], "option1"),
        ("What is a supporting detail?", ["Evidence for main idea", "Topic sentence", "Title", "Footnote"], "option1"),
        ("What is summarization?", ["Brief restatement", "Word count", "Conclusion", "Expansion"], "option1"),
    ]
}

with app.app_context():
    updated = 0

    for chapter in Chapter.query.all():
        topic = chapter.name.strip()
        if topic not in question_bank:
            continue

        questions_data = question_bank[topic]

        quizzes = Quiz.query.filter_by(chapter_id=chapter.id).order_by(Quiz.id).all()
        if not quizzes:
            continue

        for quiz in quizzes:
            questions = Question.query.filter_by(quiz_id=quiz.id).order_by(Question.id).all()

            for i, question in enumerate(questions):
                if i >= len(questions_data):
                    break
                qtext, options, correct = questions_data[i]
                question.question_statement = qtext
                question.option1 = options[0]
                question.option2 = options[1]
                question.option3 = options[2]
                question.option4 = options[3]
                question.correct_option = correct
                updated += 1

    db.session.commit()
    print(f"✅ Updated {updated} existing questions with real content.")


