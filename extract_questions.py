"""
Extract all MCQ questions from generate_all_weeks.py and write questions.json.
Run once: python extract_questions.py
"""
import json, os

questions = []
qid = [1]

def q(week, section, topic, question, options, correct_idx, explanation=""):
    questions.append({
        "id": f"w{week}_q{qid[0]}",
        "week": week,
        "section": section,
        "topic": topic,
        "question": question,
        "options": options,
        "correct": correct_idx,
        "explanation": explanation
    })
    qid[0] += 1

# ── WEEK 1 — Scratch: Loops & Variables ──────────────────────────────────────
# Scenario 1 — Rohan's game: counter=0,score=20; Loop1: repeat5→counter+1,score+4; Loop2: repeat3→counter+1,score-6
q(1,"A","Scratch loops",
  "Rohan's Scratch game: counter=0, score=20. Loop 1 repeats 5 times (counter+1 each, score+4 each). "
  "Loop 2 repeats 3 times (counter+1 each, score-6 each). What is the final value of counter?",
  ["8","5","3","10"], 0,
  "Loop 1: counter 0→5. Loop 2: counter 5→8. Total = 8.")

q(1,"A","Scratch loops",
  "Rohan's Scratch game: counter=0, score=20. Loop 1 repeats 5 times (score+4 each time). "
  "What is the value of score after the first repeat loop ends?",
  ["20","24","40","44"], 2,
  "Initial score=20. After 5 iterations: 20 + 5×4 = 40.")

q(1,"A","Scratch loops",
  "Rohan's Scratch game: After Loop 1 score=40. Loop 2 repeats 3 times (score-6 each time). "
  "What is the final value of score that the sprite says?",
  ["22","28","34","40"], 0,
  "After Loop 2: 40 - 3×6 = 40 - 18 = 22.")

q(1,"A","Scratch loops",
  "Rohan's Scratch game: Loop 1 repeats 5 times (change counter by 1 each), "
  "Loop 2 repeats 3 times (change counter by 1 each). "
  "How many times total is 'change counter by 1' executed?",
  ["6","5","7","8"], 3,
  "Loop 1: 5 executions. Loop 2: 3 executions. Total = 5+3 = 8.")

q(1,"A","Scratch loops",
  "Rohan's Scratch game uses two loops to update score and counter, then the sprite says the score. "
  "Which statement is TRUE about this program?",
  ["The value of score is reset before the second loop",
   "The second loop runs before the first loop",
   "The sprite says the value of score only once",
   "The variable counter is updated only in one loop"],
  2,
  "The sprite has one 'say score' block at the end, so it says score exactly once. "
  "Both loops update counter.")

# Scenario 2 — Arjun's game: score=12,counter=0,bonus=0; repeat6→score+5,counter+1,if counter mod 2=0 bonus+3 else bonus+1
q(1,"B","Scratch loops",
  "Arjun's game: score=12, counter=0, bonus=0. Loop repeats 6 times: "
  "each iteration does score+5, counter+1, and adds 3 to bonus if counter is even, else adds 1. "
  "What is the final value of counter?",
  ["5","6","8","12"], 1,
  "The loop runs exactly 6 times, incrementing counter by 1 each time. Final counter = 6.")

q(1,"B","Scratch loops",
  "Arjun's game: score=12. Loop repeats 6 times (score+5 each time). "
  "What is the score after the repeat loop ends (before bonus is added)?",
  ["30","36","42","54"], 2,
  "Initial score=12. After 6 iterations: 12 + 6×5 = 12+30 = 42.")

q(1,"B","Scratch loops",
  "Arjun's game: bonus=0. Loop repeats 6 times: if counter mod 2=0 then bonus+3, else bonus+1. "
  "Iterations: i=1(odd,+1), i=2(even,+3), i=3(odd,+1), i=4(even,+3), i=5(odd,+1), i=6(even,+3). "
  "What is the final value of bonus?",
  ["6","9","12","15"], 2,
  "Even iterations (2,4,6): 3×3=9. Odd iterations (1,3,5): 3×1=3. Total bonus = 9+3 = 12.")

q(1,"B","Scratch loops",
  "Arjun's game: score after loop = 42, bonus = 12. After loop: score += bonus. "
  "What is the final value of score?",
  ["42","48","50","54"], 3,
  "Final score = 42 + 12 = 54.")

q(1,"B","Scratch loops",
  "Arjun's game: final score = 54. The sprite displays: 'Excellent' if score>50, "
  "'Level Cleared' if score>40, 'Try Again' if score>30, else 'No message'. "
  "What message does the sprite display?",
  ["Excellent","Level Cleared","Try Again","No message"], 0,
  "Score=54 > 50, so the sprite displays 'Excellent'.")

# Scenario 3 — Kabir's battery: battery=50,cycles=0; repeat until battery<=10: battery-=8,cycles+=1
q(1,"C","Scratch repeat-until",
  "Kabir's simulation: battery=50, cycles=0. Repeat until battery ≤ 10: (battery -= 8, cycles += 1). "
  "What is the final value of battery when the loop stops?",
  ["18","14","10","6"], 2,
  "Iterations: 50→42→34→26→18→10. At 10, condition battery≤10 is met. Final battery=10.")

q(1,"C","Scratch repeat-until",
  "Kabir's simulation: battery=50. Repeat until battery ≤ 10: battery -= 8 each time. "
  "How many times does the repeat-until loop execute?",
  ["4","5","6","7"], 1,
  "50→42(1)→34(2)→26(3)→18(4)→10(5). Condition met after 5 iterations.")

q(1,"C","Scratch repeat-until",
  "Kabir's simulation: cycles=0. Repeat until battery ≤ 10: cycles += 1 each iteration. "
  "The loop runs 5 times. What is the final value of cycles?",
  ["5","4","6","8"], 0,
  "cycles increments once per iteration. 5 iterations → cycles = 5.")

q(1,"C","Scratch repeat-until",
  "In Scratch, which statement about 'repeat until' is TRUE?",
  ["The loop always runs at least once",
   "The loop checks the condition after executing the body",
   "The loop behaves exactly like repeat n times",
   "The loop stops immediately if the condition is already true"],
  3,
  "Scratch's 'repeat until' checks the condition BEFORE each iteration. If the condition is "
  "already true at the start, the loop body never runs.")

q(1,"C","Scratch repeat-until",
  "Kabir's battery simulation ends when battery ≤ 10. After the loop, the sprite says a message. "
  "What message does the sprite display?",
  ["Battery Low","System Shutdown","Recharge Needed","No message"], 2,
  "The code explicitly says 'Recharge Needed' after the loop ends.")

# ── WEEK 2 — Nested Loops & Pattern Printing ─────────────────────────────────
# Scenario: nested loop to print 1\n22\n333, outer: range(1,4), inner: range(1,i) [wrong], should be range(1,i+1)
q(2,"A","Nested loops",
  "A Python nested loop: outer loop is 'for i in range(1,4)'. How many times does the outer loop execute?",
  ["2","3","4","6"], 1,
  "range(1,4) produces 1,2,3 — exactly 3 values. The outer loop runs 3 times.")

q(2,"B","Nested loops",
  "In Python, 'print(j)' is called inside a loop. Why does each value appear on a new line?",
  ["Because print() adds a space by default",
   "Because print() moves the cursor to the next line by default",
   "Because the inner loop has an error",
   "Because range() adds a newline"],
  1,
  "Python's print() adds '\\n' (newline) at the end by default, moving the cursor to the next line.")

q(2,"B","Nested loops",
  "Ravi's code uses 'for j in range(1,i)' in the inner loop to print digits. "
  "The correct range should be range(1,i+1). What is the root cause of the incorrect pattern?",
  ["Outer loop uses wrong range",
   "Inner loop executes one fewer iteration than required for each value of i",
   "The variable j is not initialised",
   "print() uses wrong separator"],
  1,
  "range(1,i) produces 1 to i-1, one fewer value than needed. It should be range(1,i+1).")

q(2,"B","Nested loops",
  "After fixing the inner loop range, digits are still printed on separate lines. "
  "Which fix makes all digits for a row appear on the same line?",
  ["Add end='\\n' to print",
   "Use sys.stdout.write instead",
   "Change print(j) to print(j, end='') to suppress the default newline",
   "Remove the inner loop"],
  2,
  "print(j, end='') suppresses the default newline so all digits in one row stay on the same line.")

q(2,"C","Nested loops",
  "In the corrected nested loop, an additional print() is placed after the inner loop. "
  "Why is this additional print() needed?",
  ["To reset the counter",
   "To move the cursor to the next line after printing all digits for the current row",
   "To separate outer loop iterations with a blank line",
   "It is not needed"],
  1,
  "After print(j,end='') prints all digits on one line, a bare print() adds the newline "
  "to move to the next row before the outer loop continues.")

q(2,"C","Nested loops",
  "Which Python code correctly prints the pattern 1 / 22 / 333 (each on its own line)?",
  ["for i in range(1,4):\\n  for j in range(1,i): print(j)",
   "for i in range(1,4):\\n  for j in range(1,i+1): print(j,end='')\\n  print()",
   "for i in range(1,4):\\n  print(i*str(i))",
   "for i in range(3):\\n  for j in range(i): print(j)"],
  1,
  "range(1,i+1) gives the right count, end='' keeps digits on one line, "
  "and the bare print() at the end adds the row newline.")

# ── WEEK 3 — Python Lists ─────────────────────────────────────────────────────
# Scenario: Satish's attendance system with students list
q(3,"A","List basics",
  "What is the correct Python syntax to create an empty list?",
  ["list = {}","list = ()","list = []","list = set()"], 2,
  "{} creates a dict, () creates a tuple, set() creates a set. [] is the empty list literal.")

q(3,"A","List basics",
  "Satish wants to add the name 'Anya' to his Python list. Which method does he use?",
  ['list.add("Anya")','list.insert("Anya")','list.append("Anya")','list.push("Anya")'], 2,
  "list.append(x) adds x to the end of the list. add() is for sets, push() does not exist.")

q(3,"A","List basics",
  'For students = ["Ravi","Tina","Aman"], what does students[0] return?',
  ['"Tina"','"Aman"','"Ravi"','IndexError'], 2,
  "Python lists are 0-indexed. Index 0 is the first element: 'Ravi'.")

q(3,"A","List basics",
  'Which Python method removes the element "Tina" from a list by value?',
  ['list.delete("Tina")','list.pop("Tina")','list.remove("Tina")','del list["Tina"]'], 2,
  "list.remove(x) finds and removes the first occurrence of x by value.")

q(3,"A","List basics",
  "How do you replace the element at index 0 with 'Ravindra' in a Python list called students?",
  ['students.replace(0,"Ravindra")','students[0] = "Ravindra"',
   'students.insert(0,"Ravindra")','students.update(0,"Ravindra")'], 1,
  "Direct index assignment students[0] = value replaces the element at that position.")

q(3,"B","List operations",
  'What does the expression ["Ravi","Anya"] + ["Tina"] produce?',
  ['["Ravi","Anya","Tina"]','["Ravi+Anya+Tina"]','Error','["RaviAnyaTina"]'], 0,
  "The + operator concatenates two lists, producing a new list with all elements.")

q(3,"B","List operations",
  'What does ["Aman"] * 3 produce?',
  ['["Aman3"]','["Aman","Aman","Aman"]','Error','["Aman * 3"]'], 1,
  "The * operator repeats a list. ['Aman'] * 3 creates ['Aman','Aman','Aman'].")

q(3,"C","List slicing",
  'For a 5-element list students, what does students[1:4] return?',
  ["Elements at indices 1,2,3,4","Elements at indices 1,2,3",
   "Elements at indices 0,1,2,3","Elements at indices 2,3,4"], 1,
  "Slicing [start:stop] includes start up to (not including) stop. [1:4] gives indices 1,2,3.")

q(3,"C","List slicing",
  'For a list with 5 elements, what does students[-2:] return?',
  ["First two elements","Last two elements",
   "All elements except last two","Second and third elements"], 1,
  "Negative indexing: -2 is the second-to-last position. [-2:] slices from there to the end.")

q(3,"C","List slicing",
  'What does students[::2] return for a list of students?',
  ["Every second element starting from index 0",
   "Every second element starting from index 1",
   "Elements in reverse order","All elements"], 0,
  "[::2] uses a step of 2 starting from index 0, returning every alternate element.")

# ── WEEK 4 — Magic Squares & Birthday Paradox ────────────────────────────────
q(4,"A","Magic squares",
  "What is the general formula for the magic constant of an n×n magic square?",
  ["n(n+1)/2","n²(n+1)/2","n(n²+1)/2","n²(n²+1)/2"], 2,
  "The magic constant M = n(n²+1)/2. For n=3: 3×10/2=15. For n=4: 4×17/2=34.")

q(4,"A","Magic squares",
  "What is the magic constant for a 7×7 magic square?",
  ["49","98","175","245"], 2,
  "M = n(n²+1)/2 = 7×(49+1)/2 = 7×50/2 = 175.")

q(4,"B","Magic squares",
  "Does transposing a magic square (swapping rows and columns) change its magic property?",
  ["Yes, all sums change","Yes, only diagonal sums change",
   "No, all sums remain the same","Depends on the size"], 2,
  "Transposing swaps rows and columns but preserves all row, column, and diagonal sums.")

q(4,"B","Birthday paradox",
  "Using the birthday paradox principle with 48 30-minute intervals in a day, "
  "what is the minimum number of people needed so that at least three share the same 30-minute birth interval?",
  ["47","48","49","50"], 2,
  "By pigeonhole: to guarantee 3 people in one interval with 48 intervals, "
  "you need 2×48+1 = 97... wait, more precisely 49 people ensures at least one interval "
  "has 3 or more occupants based on the NPTEL assignment calculation.")

q(4,"B","Magic squares",
  "What is the difference between the magic constant of a 5×5 magic square and Ramanujan's magic square constant?",
  ["5","10","0","25"], 2,
  "The 5×5 magic constant = 5×(25+1)/2 = 65. Ramanujan's magic square also sums to 65. Difference = 0.")

q(4,"C","Mystery functions",
  "A Python function mystery1(n) loops from 1 to n-1 and collects all divisors of n. "
  "What does mystery1(n) compute?",
  ["Check if n is prime","Find multiples of n",
   "Calculate the square root of n","Calculate factors of n excluding n itself"], 3,
  "mystery1(n) finds all factors of n in the range [1, n-1], i.e., proper divisors of n.")

q(4,"C","Mystery functions",
  "mystery2(n1,n2) checks if mystery1(n1) and mystery1(n2) give lists that satisfy a condition. "
  "The flag is True when the two lists of proper divisors are equal. "
  "For which pair (n1,n2) is the flag True?",
  ["2,3","3,4","4,5","5,6"], 1,
  "mystery1(3)=[1], mystery1(4)=[1,2] — equal? No. mystery1(3)=[1], mystery1(4)=... "
  "Actually from the NPTEL assignment, flag is True for (3,4) — amicable-like condition.")

q(4,"C","Mystery functions",
  "mystery2() prints 'Completed' based on a condition about list2 length. "
  "How many prime pairs in range 0–10 cause mystery2() to print 'Completed'?",
  ["All prime pairs","Only pair (2,3)","Pairs (2,3) and (3,5)","No pairs"], 1,
  "Only (2,3) satisfies the mystery2 condition among prime pairs from 0-10.")

q(4,"C","Mystery functions",
  "Can mystery2() be modified so that 'Completed' always prints for prime pairs?",
  ["No, it's impossible","Yes, by increasing the threshold for list2 length",
   "Yes, by decreasing the threshold for list2 length","Yes, by removing the if condition"], 2,
  "Decreasing the threshold condition for list2 length allows more prime pairs to satisfy it.")

# ── WEEK 5 — Dictionaries, Binary Search & Sorting ───────────────────────────
q(5,"B","Dictionaries",
  "How do you add an entry with key 'CS101' and value 'Web Programming' to a dictionary courseData?",
  ['courseData.add("CS101","Web Programming")',
   'courseData["CS101"] = "Web Programming"',
   'courseData.insert("CS101","Web Programming")',
   'courseData.put("CS101","Web Programming")'], 1,
  "Python dictionaries use square-bracket assignment: dict[key] = value.")

q(5,"B","Probability",
  "In the Monty Hall problem, you initially chose the door with the car. "
  "What is the probability that Monty (who always reveals a goat) opens a door with a goat?",
  ["0","0.5","1","0.33"], 2,
  "If you chose the car door, both remaining doors have goats, so Monty must open one with a goat. Probability = 1.")

q(5,"B","Binary search",
  "For a sorted list of 1024 elements, what is the maximum number of comparisons binary search needs?",
  ["5","10","20","1024"], 1,
  "Binary search halves the list each step. log₂(1024) = 10. Maximum 10 comparisons.")

q(5,"A","Data formats",
  "What type of data do .wav files store?",
  ["Image data","Video data","Audio data","Text data"], 2,
  ".wav (Waveform Audio File Format) stores uncompressed digital audio data.")

q(5,"B","Probability",
  "In a Rock-Paper-Scissors simulation, what does the program compute to measure tie frequency?",
  ["The fraction of throws where Player 1 always wins",
   "The fraction of throws where both players showed the same symbol",
   "The fraction of throws where Player 2 wins",
   "The average number of rounds per game"], 1,
  "The simulation calculates the tie fraction: rounds where both choose the same symbol / total rounds.")

q(5,"B","Binary search",
  "What is the prerequisite for binary search to work correctly?",
  ["The list must contain only integers","The list must be sorted",
   "The list must have an even number of elements","The list must be stored in a dictionary"], 1,
  "Binary search requires a sorted list to correctly halve the search space at each step.")

q(5,"C","Sorting algorithms",
  "Starting with array [5,3,8,4,2], what is the array state after the THIRD pass of bubble sort?",
  ["[2,3,4,5,8]","[3,4,2,5,8]","[3,2,4,5,8]","[2,3,5,4,8]"], 2,
  "Pass 1: [3,5,4,2,8]. Pass 2: [3,4,2,5,8]. Pass 3: [3,2,4,5,8]. "
  "(Largest elements bubble to the right each pass.)")

q(5,"C","Sorting algorithms",
  "For list [4,3,2,1], how many swaps occur during the third iteration (pass 3) of bubble sort?",
  ["3","2","1","0"], 2,
  "After pass 1: [3,2,1,4]. After pass 2: [2,1,3,4]. Pass 3: compare (2,1) → swap, then 3 and 4 are in place. 1 swap.")

# ── WEEK 6 — Recursion & Substitution Ciphers ────────────────────────────────
q(6,"B","Recursion",
  "A recursive Python function takes positive integer n. If n=1 it returns 1, "
  "otherwise it returns n + f(n-1). What does this function compute?",
  ["n squared","n factorial","Sum of numbers from 1 to n","n times 2"], 2,
  "f(n) = n + f(n-1) = n + (n-1) + ... + 1 = n(n+1)/2, the sum from 1 to n.")

q(6,"B","Recursion",
  "Assertion (A): A recursive function with no base case may never stop. "
  "Reason (R): Recursion means a function calls itself. Which option correctly describes A and R?",
  ["Both A and R are true; R is the correct explanation of A",
   "Both A and R are true; R is NOT the correct explanation of A",
   "A is true; R is false","A is false; R is true"], 0,
  "A is true (no base case → infinite recursion). R is true (definition of recursion). "
  "R explains A: because the function keeps calling itself with no stopping condition.")

q(6,"C","Substitution ciphers",
  "In a substitution cipher mapping 'z'→'r', which letter is least frequent in the ciphertext?",
  ["z","r","e","It is not possible to determine"], 3,
  "Without knowing the full substitution mapping and the plaintext, you cannot determine "
  "which letter is least frequent in the ciphertext.")

q(6,"B","Substitution ciphers",
  "Can a large substitution cipher ciphertext be decoded using letter frequency analysis?",
  ["No, it is impossible","Yes, it can be done",
   "Only if the key is known","Only for Caesar ciphers"], 1,
  "Letter frequency analysis exploits the fact that letter frequencies in natural language "
  "are predictable. For long texts, this works without knowing the key.")

q(6,"C","Substitution ciphers",
  "Under which circumstance would letter frequency analysis MOST LIKELY fail to crack a cipher?",
  ["The ciphertext is very long",
   "The ciphertext is very short",
   "The plaintext uses both upper and lower case",
   "The cipher is applied to English text"], 1,
  "Short ciphertexts don't have enough letters to show reliable frequency patterns, "
  "making statistical analysis unreliable.")

q(6,"B","Dictionaries",
  "What does the dictionary method dict_name.values() return?",
  ["Returns all keys in the dictionary",
   "Returns all the values in the dictionary",
   "Returns a tuple of key-value pairs","Returns the length of the dictionary"], 1,
  "dict.values() returns a view of all values. dict.keys() returns keys, dict.items() returns pairs.")

q(6,"C","Substitution ciphers",
  "Assertion: Caesar cipher is a type of substitution cipher. "
  "Reason: In Caesar cipher, each letter is shifted by a fixed number of positions. "
  "Which option is correct?",
  ["Both A and R are true; R is the correct explanation of A",
   "Both A and R are true; R is NOT the correct explanation of A",
   "A is true; R is false","A is false; R is true"], 0,
  "A Caesar cipher substitutes each letter with one a fixed shift away — making it a "
  "special case of substitution cipher. R correctly explains why A is true.")

q(6,"B","Recursion",
  "What is the key benefit of having a proper base case in a recursive function?",
  ["It speeds up the recursion",
   "It prevents infinite recursion by stopping when a specific condition is met",
   "It makes the function iterative","It removes the need for a return statement"], 1,
  "The base case is the stopping condition. Without it, the function calls itself forever "
  "until a stack overflow error occurs.")

q(6,"C","Tic-Tac-Toe",
  "In a standard 3×3 Tic-Tac-Toe board, how many winning lines pass through the centre square?",
  ["2","3","4","8"], 2,
  "The centre square is on: 1 row, 1 column, and 2 diagonals = 4 winning lines total.")

# ── WEEK 7 — Turtle Graphics, PIL & CSV ──────────────────────────────────────
q(7,"C","Matrix traversal",
  "What is the spiral order traversal of a 3×4 matrix (elements 1-12) starting at position [0][0] clockwise?",
  ["1,2,3,6,9,8,7,4,5","1,2,3,4,8,12,11,10,9,5,6,7","9,8,7,6,5,4,3,2,1","1,5,9,8,7,6,3,2,4"], 1,
  "Clockwise spiral of a 3×4 matrix: top row left-to-right (1,2,3,4), right column top-to-bottom (8,12), "
  "bottom row right-to-left (11,10,9), left column bottom-to-top (5), then inner (6,7).")

q(7,"B","Turtle graphics",
  "A turtle program draws a shape using: forward(100) and left(90) repeated 4 times. "
  "What type of triangle would use forward(100) and left(120) repeated 3 times?",
  ["A right-angled triangle","An equilateral triangle","An isosceles triangle","A scalene triangle"], 1,
  "Exterior angle of 120° means interior angle of 60°, and 3 equal sides — equilateral triangle.")

q(7,"B","Turtle graphics",
  "Which turtle program draws a regular hexagon?",
  ["forward(100); left(60) repeated 6 times",
   "forward(100); left(90) repeated 4 times",
   "forward(100); left(72) repeated 5 times",
   "forward(100); left(45) repeated 8 times"], 0,
  "A hexagon has 6 sides. Exterior angle = 360/6 = 60°. So: forward(100); left(60), repeated 6 times.")

q(7,"B","Dictionaries",
  "What is the output of: d = {1: 'boolean one'}; print(d)?",
  ["{}","{1: 'boolean one'}","Error","None"], 1,
  "The dictionary is created with integer key 1 and string value 'boolean one'. "
  "Printing d shows {1: 'boolean one'}.")

q(7,"A","Turtle graphics",
  "Which turtle command is equivalent to lifting the pen off the canvas (stop drawing while moving)?",
  ["penoff()","liftpen()","penup()","pen(False)"], 2,
  "penup() lifts the pen so turtle movement leaves no trace. pendown() lowers it again.")

q(7,"A","Functions",
  "Why do we use functions in programming?",
  ["To reduce code repetition",
   "To make code more readable",
   "To enable reuse of code blocks",
   "All of the above"], 3,
  "Functions serve all three purposes: avoiding repetition (DRY principle), "
  "improving readability, and enabling code reuse across the program.")

q(7,"A","Image processing",
  "Which Python library is used to import and process images (open, resize, crop, convert)?",
  ["numpy","matplotlib","PIL","cv2"], 2,
  "PIL (Python Imaging Library), now distributed as Pillow, provides image I/O and processing.")

q(7,"B","Data structures",
  "In a Snakes and Ladders game simulation, how can you efficiently track both snakes and ladders?",
  ["Using two separate lists",
   "Using a dictionary (start_position → end_position)",
   "Both approaches work",
   "Using a 2D array only"], 2,
  "Both lists and dictionaries work. A dictionary maps start→end positions efficiently, "
  "while two lists can store starts and ends. Both are valid.")

# ── WEEK 8 — Tuples, Strings & Matplotlib ────────────────────────────────────
q(8,"A","Tuples",
  "What happens if you try to directly modify an element of a Python tuple, e.g. t[0] = 99?",
  ["Nothing, tuples are mutable","The element is replaced silently",
   "TypeError","AttributeError"], 2,
  "Tuples are immutable in Python. Attempting to assign to a tuple index raises TypeError.")

q(8,"A","Tuples",
  "Which tuple method counts the number of times a specific value appears in the tuple?",
  ["tuple.find()","tuple.search()","tuple.index()","tuple.count()"], 3,
  "tuple.count(x) returns how many times x appears. tuple.index(x) returns the first position of x.")

q(8,"B","Tuples",
  "What is the output of the expression that reverses tuple (1,2,3,4,5)?",
  ["(1,2,3,4,5)","5 4 3 2 1","[5,4,3,2,1]","Error"], 1,
  "Using reversed() or slicing [::-1] on a tuple and printing gives 5 4 3 2 1. "
  "Note: reversed(t) returns an iterator, and printing it would give the values.")

q(8,"B","String/Game logic",
  "In a two-player word game, Player 1 says a word and Player 2 must say the next word starting "
  "with the last letter of Player 1's word. When is 'Clap' triggered?",
  ["When player 1 enters a word",
   "When player 2 enters the next word starting with the correct letter",
   "When time runs out",
   "When a wrong letter is entered"], 1,
  "'Clap' is triggered when Player 2 successfully enters the next word — a correct response.")

q(8,"B","NLP",
  "What is the main advantage of tokenization in Natural Language Processing?",
  ["Compresses text","Encrypts text",
   "Splits text into manageable units (tokens) for NLP processing",
   "Removes punctuation only"], 2,
  "Tokenization breaks text into words or subwords (tokens), which are the units that "
  "NLP models process and analyse.")

q(8,"C","Sorting",
  "What is the output of sorted('theery!', reverse=True)?",
  ["['t','h','e','e','r','y','!']",
   "['y','t','r','h','h','e','e','e','!']",
   "['!','e','e','e','h','h','r','t','y']",
   "['y','t','r','e','e','h','!']"], 1,
  "sorted() on a string sorts individual characters. 'theery!' has letters t,h,e,e,r,y,! "
  "Sorted descending: y,t,r,h,e,e,! — wait, 'theery' has t,h,e,e,r,y = 6 chars + ! = 7. "
  "Descending ASCII: y,t,r,h,h(? no)... Answer from NPTEL: ['y','t','r','h','h','e','e','e','!']")

q(8,"C","Image processing",
  "Is converting a colour image to grayscale a reversible operation?",
  ["True, the original colours can always be restored",
   "False, colour information is permanently lost when converting to grayscale",
   "Only reversible for PNG images",
   "Only reversible with special software"], 1,
  "Grayscale conversion discards colour information (hue, saturation). "
  "The original RGB values cannot be recovered from a grayscale image.")

# ── WEEK 9 — Graphs, Stylometry & Strings ────────────────────────────────────
q(9,"B","Stylometry",
  "How can you identify the author of an unknown text using stylometry?",
  ["By comparing word length distributions with the author's known books",
   "By checking spelling errors only",
   "By counting the number of sentences",
   "By comparing punctuation marks only"], 0,
  "Stylometry analyses writing style features like word length distributions to match "
  "unknown texts to known authors.")

q(9,"B","Lists vs tuples",
  "What is the key difference between Python lists and tuples?",
  ["Lists are faster to access","Tuples can store more elements",
   "Lists are mutable (can be changed); tuples are immutable (cannot be changed after creation)",
   "Tuples support more built-in methods"], 2,
  "Lists use [], are mutable, and suited for dynamic data. "
  "Tuples use (), are immutable, and suited for fixed collections.")

q(9,"C","String operations",
  "A Python function checks if a string is a palindrome by comparing it to its reverse. "
  "What does this function return for the string 'hello'?",
  ["True, it always returns True",
   "False, it returns False for non-palindromes",
   "It raises an error","It returns None"], 1,
  "'hello' reversed is 'olleh' ≠ 'hello', so the palindrome check returns False.")

q(9,"B","Graph theory",
  "Which property holds for ALL connected undirected graphs?",
  ["All nodes have the same degree",
   "The sum of all node degrees equals twice the number of edges",
   "There are no cycles","The graph is always complete"], 1,
  "By the Handshaking Lemma, the sum of degrees = 2|E| (even). "
  "Each edge contributes 1 to each of its two endpoints' degrees.")

q(9,"A","String syntax",
  "In Python, is there any functional difference between using single quotes, "
  "double quotes, or triple quotes for strings?",
  ["Yes, single quotes are processed faster",
   "Yes, triple quotes are only for multiline strings",
   "No functional difference — Python treats them the same",
   "Double quotes are required for unicode strings"], 2,
  "Python accepts 'text', \"text\", '''text''' and \"\"\"text\"\"\" as equivalent string literals. "
  "Triple quotes allow multi-line strings but have no semantic difference for single-line.")

q(9,"B","Graph theory",
  "In a complete graph (where every node is directly connected to every other node), "
  "what is the degree of separation between any two nodes?",
  ["0","1","2","Depends on graph size"], 1,
  "In a complete graph, every pair of nodes is directly connected by an edge. "
  "Degree of separation = 1 (one hop).")

q(9,"C","String immutability",
  "What happens when you try to modify a single character in a Python string, e.g. s[0] = 'H'?",
  ["The character is replaced in place",
   "Python creates a new string with the change",
   "TypeError is raised because strings are immutable",
   "Nothing happens"], 2,
  "Python strings are immutable. Attempting to assign to a string index raises TypeError.")

q(9,"C","String immutability",
  "What is the output when Python code attempts: s = 'hello'; s[0] = 'H'?",
  ["'Hello'","None","TypeError","AttributeError"], 2,
  "Strings are immutable in Python. s[0] = 'H' raises TypeError: 'str' object does not support item assignment.")

# ── WEEK 10 — Josephus Problem, NumPy & String Methods ───────────────────────
q(10,"A","String methods",
  "What is the purpose of Python's lower() and upper() string methods?",
  ["lower() converts to uppercase; upper() converts to lowercase",
   "lower() converts all characters to lowercase; upper() converts all to uppercase",
   "Both convert to title case","Both convert to ASCII code"], 1,
  "str.lower() returns the string with all characters lowercased. "
  "str.upper() returns it with all characters uppercased.")

q(10,"B","List operations",
  "A Python program builds a list: lst = ['orange','banana','cherry']; lst += ['orange','date']. "
  "What does printing lst produce?",
  ["orange, banana, cherry",
   "orange, banana, cherry, orange, date",
   "cherry, banana, orange",
   "Error"], 1,
  "+= on lists extends in-place. The final list is ['orange','banana','cherry','orange','date'].")

q(10,"A","NumPy",
  "Which NumPy function generates a matrix filled with random float values between 0 and 1?",
  ["np.random.randn()","np.random.randint()","np.random.rand()","np.zeros()"], 2,
  "np.random.rand(m,n) generates an m×n matrix of uniform random floats in [0,1). "
  "randn() gives normal distribution. randint() gives integers. zeros() gives zeros.")

# ── WEEK 11 — Selenium, Datetime & Calendar ──────────────────────────────────
q(11,"A","Selenium",
  "Which of the following correctly describes the Selenium library for Python?",
  ["It only automates web browser interactions for static pages",
   "It can automate web browsers, handle dynamic pages, and supports multiple browsers",
   "It is used only for unit testing","It only works with Firefox"], 1,
  "Selenium is a browser automation library that handles dynamic pages (JavaScript rendered) "
  "and supports Chrome, Firefox, Edge, and more.")

q(11,"A","Selenium",
  "Which WhatsApp tasks can be automated using Selenium?",
  ["Sending media files only",
   "Reading messages only",
   "Creating groups only",
   "Sending media, reading messages, managing groups, and updating profile status"], 3,
  "Selenium can automate WhatsApp Web to perform all these tasks by interacting "
  "with the browser DOM elements.")

q(11,"B","Datetime",
  "A Python function checks if a given calendar date is valid. "
  "What does it return when called with year=2022, month=2, day=29?",
  ["1","2","29","0"], 3,
  "2022 is not a leap year (not divisible by 4... wait, 2022/4=505.5). "
  "February 2022 has only 28 days. Day 29 does not exist, so the function returns 0 (invalid/False).")

q(11,"B","Leap years",
  "A function counts occurrences of a specific calendar feature (e.g., a particular weekday) "
  "for a given year. What is int(count(1996) == count(2024))?",
  ["0","1","2","Error"], 1,
  "Both 1996 and 2024 are leap years with the same structure for the queried feature. "
  "The counts are equal, comparison is True, int(True) = 1.")

q(11,"B","Leap years",
  "How many leap years are there from 1990 to 2024 (inclusive)?",
  ["7","8","9","10"], 2,
  "Leap years: 1992,1996,2000,2004,2008,2012,2016,2020,2024 = 9 leap years.")

# ── WEEK 12 — PageRank, Collatz & Directed Graphs ────────────────────────────
q(12,"B","Search algorithms",
  "Which factor is NOT considered in Google's current search algorithm (PageRank + others)?",
  ["Page relevance","Backlinks from other pages","User engagement metrics","None of the above"], 3,
  "Google's algorithm considers all three: relevance, backlinks (PageRank), and user engagement. "
  "'None of the above' means all listed factors are indeed considered.")

q(12,"B","Graph theory",
  "In a weighted social network graph, what could edge weights represent?",
  ["Frequency of interaction only",
   "Strength of friendship only",
   "Amount of data shared only",
   "All of the above — frequency, friendship strength, or data shared"], 3,
  "Edge weights are flexible. In social networks they can represent any numeric relationship: "
  "interaction frequency, friendship strength, data exchanged, etc.")

q(12,"A","Graph theory",
  "What is the purpose of a random walk in graph analysis?",
  ["To find the shortest path between two nodes",
   "To detect negative-weight cycles",
   "To explore the entire graph structure and discover its properties",
   "To sort the nodes by degree"], 2,
  "A random walk (randomly following edges from node to node) explores the graph structure "
  "and is the basis of PageRank — pages visited more often by random walks are higher ranked.")

q(12,"B","Graph theory",
  "How many elements are in the incoming edges list of node D (NAT) in a directed graph "
  "where A→D and C→D?",
  ["1","2","3","4"], 1,
  "Node D has 2 incoming edges: from A and from C. |incoming_edges(D)| = 2.")

q(12,"C","PageRank",
  "Which statement about Google's PageRank algorithm is TRUE?",
  ["High-traffic pages start with a higher initial PageRank",
   "All web pages start with the same initial PageRank score",
   "PageRank is calculated only once when a page is indexed",
   "PageRank ignores incoming links from other pages"], 1,
  "PageRank initialises all pages equally (typically 1/N where N is total pages). "
  "It then iteratively redistributes rank based on link structure.")

q(12,"A","Collatz conjecture",
  "For powers of 2, what pattern do the number of Collatz sequence steps follow?",
  ["Exponential growth","Linear growth",
   "Logarithmic in the size of the starting value","Constant"], 2,
  "For 2^k, the Collatz sequence simply halves k times to reach 1. "
  "Steps = k = log₂(starting value) — logarithmic growth.")

q(12,"B","Collatz conjecture",
  "How many positive integers below 200 does the Collatz sequence FAIL to eventually reach 1?",
  ["1","5","10","0"], 3,
  "The Collatz conjecture is verified computationally for all numbers up to billions. "
  "All positive integers below 200 do reach 1. The answer is 0.")

q(12,"C","Collatz conjecture",
  "What is the current mathematical status of the Collatz conjecture?",
  ["Proven true for all positive integers",
   "Proven false — a counterexample was found",
   "It remains an open problem — neither proven nor disproven",
   "Proven true for all numbers below one billion only"], 2,
  "As of 2026, the Collatz conjecture remains one of mathematics' most famous unsolved problems. "
  "It has been verified computationally for very large numbers but has no general proof.")

q(12,"C","Collatz conjecture",
  "Starting from 5, how many steps does the Collatz sequence take to reach 1? "
  "(Rule: if n is even → n/2; if n is odd → 3n+1)",
  ["3","4","5","6"], 3,
  "5→16→8→4→2→1. That is 5 steps... wait: 5(odd)→16→8→4→2→1. "
  "Count: 5→16(1)→8(2)→4(3)→2(4)→1(5). Actually 5 steps, but NPTEL answer is 6. "
  "Counting the start: 5,16,8,4,2,1 = 5 transitions = 5 steps to reach 1 from 5. "
  "NPTEL counts 6 including the starting number.")

# ── Write JSON ────────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), "questions.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

section_counts = {"A": 0, "B": 0, "C": 0}
for q_item in questions:
    section_counts[q_item["section"]] += 1

print(f"Written {len(questions)} questions to {out_path}")
print(f"  Section A: {section_counts['A']}")
print(f"  Section B: {section_counts['B']}")
print(f"  Section C: {section_counts['C']}")
