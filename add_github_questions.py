"""
Add ONLY 2025/2026 session questions from progiez/GitHub repos.
Answers determined by reasoning (progiez doesn't include inline answers).
Run once: python add_github_questions.py
"""
import json, os

QFILE = os.path.join(os.path.dirname(__file__), "questions.json")

with open(QFILE, encoding="utf-8") as f:
    existing = json.load(f)

existing_texts = {q["question"].lower()[:50] for q in existing}
next_id = max(int(q["id"].split("_q")[1]) for q in existing) + 1

new_qs = []

def add(week, section, topic, question, options, correct_idx, explanation=""):
    global next_id
    key = question.lower()[:50]
    if key in existing_texts:
        return
    existing_texts.add(key)
    new_qs.append({
        "id": f"w{week}_q{next_id}",
        "week": week,
        "section": section,
        "topic": topic,
        "question": question,
        "options": options,
        "correct": correct_idx,
        "explanation": explanation
    })
    next_id += 1

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 2 — Jul-Dec 2025 Session: Discount Calculator & Multiplication Tables
# ═══════════════════════════════════════════════════════════════════════════════
add(2, "A", "Data types",
    "What is the most appropriate data type to take customer purchase input, calculate final price, and print savings?",
    ["int", "float", "bool", "str"], 1,
    "Prices involve decimals (e.g., Rs.99.50). float handles decimal values. "
    "int truncates decimals, str is text, bool is True/False.")

add(2, "A", "Input handling",
    "What is the correct Python syntax to take a customer purchase amount as numeric input?",
    ["input(float())", "float(input())", "input = float()", "float = input()"], 1,
    "float(input()) first gets string input via input(), then converts to float. "
    "input(float()) would pass a float object as the prompt string.")

add(2, "B", "Arithmetic",
    "Which expression correctly applies a 20% discount on a purchase amount stored in variable 'amount'?",
    ["discounted = amount * 0.2", "discounted = amount - (amount * 0.2)",
     "discounted = amount / 20", "discounted = amount * 0.8"], 1,
    "20% discount means subtract 20% from original: amount - (amount × 0.2). "
    "Option D (amount * 0.8) gives the same result but represents final price, not discounted amount.")

add(2, "A", "Conditionals",
    "A customer spends more than Rs.5000 and gets a 20% discount. Which if-statement is correct?",
    ["if amount > 5000:", "if amount >= 5000:", "if amount = 5000:", "if amount => 5000:"], 0,
    "'>' means strictly greater than. '=' is assignment (not comparison). "
    "'=>' is not valid Python syntax. 'amount > 5000' checks if purchase exceeds 5000.")

add(2, "C", "Conditionals",
    "What is the output of the following code if amount = 6000?\n"
    "amount = float(input())\nif amount > 5000:\n    amount = amount - amount * 0.2\nprint(amount)",
    ["6000", "4800.0", "5000", "1200"], 1,
    "6000 > 5000 is True. Discount: 6000 × 0.2 = 1200. Final: 6000 - 1200 = 4800.0")

add(2, "B", "F-strings",
    "Which line correctly prints both original price and savings using Python f-strings?",
    ['print("Original: Rs.", amount, "Saved: Rs.", saved)',
     'print(f"Original: Rs.{amount}, Saved: Rs.{saved}")',
     "print(f'Original = Rs.amount, Saved = Rs.saved')",
     'print("Original Rs.f{amount}, Saved Rs.f{saved}")'], 1,
    "f-strings use {variable} inside f\"...\" to embed values. "
    "Option A works but uses comma separation (adds spaces). "
    "Option C doesn't use {} so prints literal 'amount'. Option D has f outside the string.")

add(2, "B", "Loops",
    "Which Python loop is most suitable to print a multiplication table from 1 to 10?",
    ["while loop", "for loop", "if loop", "do-while loop"], 1,
    "for loop with range(1,11) is most suitable for a known count (10 iterations). "
    "while works too but needs manual counter. 'if loop' and 'do-while' don't exist in Python.")

add(2, "B", "Range function",
    "What values does range(1, 11) produce inside a for loop?",
    ["1 to 10 (inclusive)", "0 to 10 (inclusive)", "1 to 11 (inclusive)", "1 to 9 (inclusive)"], 0,
    "range(1, 11) produces 1, 2, 3, ..., 10. The stop value (11) is excluded.")

add(2, "A", "Loops",
    "Which keyword skips the current iteration of a loop and continues with the next one?",
    ["stop", "break", "continue", "pass"], 2,
    "continue skips the rest of the current iteration and moves to the next. "
    "break exits the loop entirely. pass does nothing. 'stop' is not a Python keyword.")

add(2, "C", "Armstrong numbers",
    "A program checks if a number is an Armstrong number. What is the output for input 9474?",
    ["Armstrong Number", "Not an Armstrong Number",
     "Error due to integer overflow", "Infinite loop"], 0,
    "9474 has 4 digits. 9⁴+4⁴+7⁴+4⁴ = 6561+256+2401+256 = 9474. It equals itself → Armstrong Number.")

add(2, "C", "Armstrong numbers",
    "An Armstrong number checker uses two while loops. How many times does each while loop "
    "execute when the input is 1000?",
    ["3", "4", "5", "It never executes"], 1,
    "1000 has 4 digits. The first while loop counts digits (4 iterations: 1000→100→10→1→0). "
    "The second loop processes each digit (4 iterations).")

add(2, "C", "Armstrong numbers",
    "In an Armstrong number checker, if 'temp = num' before the second loop is deleted, "
    "what happens for input 9474?",
    ["Armstrong Number", "Not an Armstrong Number",
     "The program hangs", "Raises NameError"], 1,
    "Without temp = num, the second loop uses the already-zero value (from first loop dividing). "
    "The sum would be 0, which ≠ 9474. Output: Not an Armstrong Number.")

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 2 — Jan-Apr 2026: Palindrome & Smart Discount (new scenarios)
# ═══════════════════════════════════════════════════════════════════════════════
add(2, "C", "Palindrome",
    "A function checks palindromes: reverse=0, while num>0: reverse = reverse*10 + num%10; num//=10. "
    "What is the final value of 'reverse' when called with is_palindrome(210)?",
    ["210", "120", "21", "12"], 3,
    "Step 1: reverse=0*10+210%10=0+0=0, num=21. "
    "Step 2: reverse=0*10+21%10=0+1=1, num=2. "
    "Step 3: reverse=1*10+2%10=10+2=12, num=0. Final reverse=12.")

add(2, "B", "Palindrome",
    "A palindrome checker reverses the number and compares to original. "
    "What does is_palindrome(210) return?",
    ["Error", "True", "False", "None"], 2,
    "210 reversed = 012 = 12. Since 12 ≠ 210, the function returns False.")

add(2, "C", "Palindrome",
    "A palindrome checker uses 'while num > 0'. How many times does the while loop execute "
    "for is_palindrome(121)?",
    ["2", "4", "3", "1"], 2,
    "121 has 3 digits. Loop: 121→12→1→0 (condition fails). Executes 3 times.")

add(2, "C", "Discount logic",
    "A premium customer purchases Rs.2,500. The system applies 10% discount for purchases > Rs.2,000. "
    "What discount amount is applied?",
    ["Rs.100", "Rs.200", "Rs.250", "Rs.0"], 2,
    "Rs.2,500 > Rs.2,000 → 10% discount applies. 10% of 2,500 = Rs.250.")

add(2, "C", "Discount logic",
    "A premium customer purchases Rs.2,000 exactly. The discount applies for amounts > Rs.2,000. "
    "What discount amount is applied?",
    ["Rs.100", "Rs.200", "Rs.300", "Rs.0"], 3,
    "The condition is 'amount > 2000'. Since 2000 is NOT greater than 2000 (it's equal), "
    "no discount applies. Discount = Rs.0.")

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 3 — Jul-Dec 2025: List Operations (Satish's attendance scenario)
# ═══════════════════════════════════════════════════════════════════════════════
add(3, "C", "List references",
    "Satish creates a backup: backup = submissions. Then he appends to submissions. "
    "Why does backup also show the new item?",
    ["Satish created a reference, not a real copy",
     "The backup was overwritten by append()",
     "backup and submissions point to the same list in memory",
     "The append() affected only submissions"], 2,
    "backup = submissions creates a REFERENCE — both variables point to the same list object. "
    "Changes through one variable are visible through the other. Use submissions.copy() or "
    "submissions[:] for an independent copy.")

add(3, "C", "List operations",
    "Which of the following statements about Python lists are FALSE?\n"
    "1) Lists are fixed in size\n2) Non-numeric indices can access elements\n"
    "3) Iterating over lists is possible\n4) Size must be specified when creating a list",
    ["Only statements 1 and 2 are false",
     "Only statements 1, 2, and 4 are false",
     "Only statement 3 is false",
     "All statements are false"], 1,
    "Lists in Python are dynamic (not fixed), use only integer indices (not non-numeric), "
    "CAN be iterated, and DON'T require size specification. Statements 1, 2, and 4 are false.")

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 3 — Jan-Apr 2025: Social Computing & File Handling
# ═══════════════════════════════════════════════════════════════════════════════
add(3, "A", "Social computing",
    "Which of the following are examples of Social Computing platforms?",
    ["ChatGPT", "Wikipedia", "Quora", "All of the above"], 3,
    "All three are social computing: ChatGPT (AI interaction), Wikipedia (collaborative knowledge), "
    "Quora (community Q&A). Social computing involves human-computer social interactions.")

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 5 — Jan-Apr 2025: Binary Search, Monty Hall
# ═══════════════════════════════════════════════════════════════════════════════
add(5, "C", "Search algorithms",
    "Given a sorted list of 2048 elements, what is the maximum number of comparisons for "
    "linear search? Can binary search do it in fewer?",
    ["Yes, binary search is more efficient; linear takes 1024 comparisons",
     "Yes, binary search is more efficient; linear takes 2048 comparisons",
     "No, binary search may not be more efficient; linear takes 1024",
     "No, binary search takes more comparisons; linear takes 2048"], 1,
    "Linear search: worst case checks all 2048 elements. "
    "Binary search: log₂(2048) = 11 comparisons. Binary search is far more efficient on sorted data.")

add(5, "B", "Binary search",
    "In binary search, the search space is divided in every iteration.",
    ["True", "False", "Only for sorted lists", "Only for integer lists"], 0,
    "True — binary search halves the remaining search space at each step by comparing "
    "the target to the middle element.")

add(5, "C", "Bubble sort",
    "Given array [4, 2, 7, 1, 3], what is the array after the third pass of Bubble Sort?",
    ["[1, 3, 2, 4, 7]", "[2, 4, 1, 3, 7]", "[1, 2, 3, 4, 7]", "[2, 1, 3, 4, 7]"], 2,
    "Pass 1: [2,4,1,3,7]. Pass 2: [2,1,3,4,7]. Pass 3: [1,2,3,4,7]. Fully sorted by pass 3.")

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 6 — Jan-Apr 2025: Function overloading
# ═══════════════════════════════════════════════════════════════════════════════
add(6, "C", "Functions",
    "What is the output? def func(x): return x**2\ndef func(x, y=1): return x**2 + y\nprint(func(5))",
    ["Error", "25", "26", "5"], 2,
    "In Python, the second definition REPLACES the first (no true overloading). "
    "func(5) calls func(x, y=1) with x=5, y=1. Returns 5²+1 = 25+1 = 26.")

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 7 — Jan-Apr 2025: Dictionary with duplicate keys
# ═══════════════════════════════════════════════════════════════════════════════
add(7, "C", "Dictionaries",
    "What is the output of: d = {1: 'one', 1.0: 'float one', True: 'boolean one'}; print(d)?",
    ['{1: "one", 1.0: "float one", True: "boolean one"}',
     '{1: "boolean one"}',
     '{1: "one", 1.0: "float one"}',
     '{1.0: "float one", True: "boolean one"}'], 1,
    "In Python, 1 == 1.0 == True (they hash to the same value). "
    "Each assignment overwrites the previous. The dict keeps the FIRST key form (1) "
    "with the LAST value ('boolean one'). Result: {1: 'boolean one'}.")

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 8 — Jan-Apr 2025: Mutable tuple contents
# ═══════════════════════════════════════════════════════════════════════════════
add(8, "C", "Tuples",
    "What is the output of: tup = ([1,2], [3,4]); tup[0].append(5); print(tup)?",
    ["([1, 2, 5], [3, 4])", "([1, 2], [3, 4])",
     "([1, 2], [3, 4, 5])", "TypeError: tuple does not support item assignment"], 0,
    "The tuple itself is immutable (can't reassign tup[0] = ...), but the LIST inside it "
    "is mutable. tup[0].append(5) modifies the list in-place without reassigning the tuple element.")

# ═══════════════════════════════════════════════════════════════════════════════
# WEEK 11 — Jan-Apr 2025: Selenium & Calendar
# ═══════════════════════════════════════════════════════════════════════════════
add(11, "B", "Selenium",
    "In Selenium, what is the purpose of WebDriver (e.g., webdriver.Chrome())?",
    ["Interact with web elements like buttons",
     "Launch and control a web browser session for automation",
     "Write test cases", "Handle databases"], 1,
    "WebDriver launches a browser instance and provides an API to control it — "
    "navigate URLs, click elements, fill forms, read page content.")

add(11, "B", "Selenium",
    "Which Selenium element locator strategy has the best performance?",
    ["find_element_by_name()", "find_element_by_id()",
     "find_element_by_class_name()", "find_element_by_xpath()"], 1,
    "find_element_by_id() is fastest because IDs are unique in HTML, "
    "allowing direct DOM lookup. XPath requires traversing the DOM tree.")

add(11, "C", "Calendar",
    "What does calendar.isleap(2100) return?",
    ["False", "True", "None", "1"], 0,
    "2100 is divisible by 100 but NOT by 400. The rule: leap if (div by 4 AND not div by 100) "
    "OR div by 400. 2100 fails both conditions → not a leap year → False.")

add(11, "C", "Datetime",
    "What is the output of: datetime.date(2024, 2, 29) + datetime.timedelta(days=1)?",
    ["2024-02-30", "2024-03-01", "ValueError", "2024-02-29"], 1,
    "2024 IS a leap year (2024 ÷ 4 = 506, not a century year), so Feb 29 exists. "
    "Adding 1 day: 2024-02-29 + 1 day = 2024-03-01.")

add(11, "B", "Datetime",
    "Which function is used to get the current local time in Python?",
    ["time.localtime()", "datetime.now()", "time.time()", "datetime.utcnow()"], 0,
    "time.localtime() returns a struct_time in local timezone. "
    "datetime.now() also gives local time. time.time() gives epoch seconds. "
    "utcnow() gives UTC, not local. Both A and B are valid but localtime() is from the time module.")

add(11, "C", "Datetime",
    "What happens when you call .astimezone() on a naive (timezone-unaware) datetime object?",
    ["It converts to UTC", "It raises an error",
     "It assumes local timezone", "It converts to IST"], 2,
    "In Python 3.6+, calling .astimezone() on a naive datetime assumes local timezone "
    "and converts accordingly. In older versions it raised ValueError.")

# ═══════════════════════════════════════════════════════════════════════════════
# Write updated JSON
# ═══════════════════════════════════════════════════════════════════════════════
all_questions = existing + new_qs
with open(QFILE, "w", encoding="utf-8") as f:
    json.dump(all_questions, f, indent=2, ensure_ascii=False)

from collections import Counter
secs = Counter(q["section"] for q in all_questions)
weeks = Counter(q["week"] for q in all_questions)

print(f"Added {len(new_qs)} new questions (2025/2026 sessions only)")
print(f"Total: {len(all_questions)} questions")
print(f"Sections: A={secs['A']}, B={secs['B']}, C={secs['C']}")
print(f"By week: {dict(sorted(weeks.items()))}")
