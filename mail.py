import math
import random

# Global variables
num1 = num2 = correctAnswer = wrongAnswer1 = wrongAnswer2 = answer = 0
operation = ""
isCorrect = None
score = 0
level = 1
max_level = 5
question_type = ""
game_state = "title"  # Initial game state

# List of background colors
background_colors = [(220, 220, 255), (255, 220, 220), (220, 255, 220), (255, 255, 220)]
current_background_color = background_colors[0]
last_color_change_time = 0  # To keep track of the last time the color changed

# List to hold geometric shapes for animation
shapes = []

# Tracking consecutive correct answers
consecutive_correct_answers = 0

# Variables for pop-up shapes
popper_shapes = []
popper_speed = 2

def setup():
    size(600, 600)  # Setting the size of the game window
    textSize(32)  # Setting the default text size for displaying questions and answers

    # Initialize geometric shapes with random positions and velocities
    for i in range(5):
        x = random.randint(0, width)
        y = random.randint(0, height)
        vx = random.uniform(-1, 1)
        vy = random.uniform(-1, 1)
        size = random.randint(20, 60)
        shapes.append({'x': x, 'y': y, 'vx': vx, 'vy': vy, 'size': size})

def draw():
    global game_state
    if game_state == "title":
        drawTitleScreen()
    elif game_state == "game":
        drawGameScreen()

def drawTitleScreen():
    global shapes
    changeBackgroundColor()  # Change the background color every 2 seconds
    background(*current_background_color)  # Soft blue background
    
    # Update and draw each shape
    for shape in shapes:
        shape['x'] += shape['vx']
        shape['y'] += shape['vy']
        
        # Wrap around screen edges
        if shape['x'] < 0:
            shape['x'] = width
        elif shape['x'] > width:
            shape['x'] = 0
        
        if shape['y'] < 0:
            shape['y'] = height
        elif shape['y'] > height:
            shape['y'] = 0
        
        # Draw shapes based on size
        if shape['size'] < 40:
            fill(255, 150, 150)  # Red for smaller shapes
        else:
            fill(150, 255, 150)  # Green for larger shapes
        
        ellipse(shape['x'], shape['y'], shape['size'], shape['size'])
    
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(48)  # Title screen text size
    text("Math Quiz Game", width / 2, height / 4)
    
    textSize(24)  # Instructions text size
    text("Click anywhere to start", width / 2, height / 2)
    text("Instructions:", width / 2, height / 2 + 50)
    textSize(18)  # Text size for instructions
    text("1. You will get negative marking for wrong answers.", width / 2, height / 2 + 80)
    text("2. Level changes after answering 5 consecutive questions correctly.", width / 2, height / 2 + 110)

def drawGameScreen():
    global num1, num2, correctAnswer, wrongAnswer1, wrongAnswer2, operation, isCorrect, score, level, question_type
    changeBackgroundColor()  # Change the background color every 2 seconds
    background(*current_background_color)  # Soft blue background

    fill(0)
    textAlign(CENTER, CENTER)
    textSize(32)  # Game screen question text size
    if question_type == "math":
        # Displaying math question using string concatenation
        text(str(num1) + " " + operation + " " + str(num2) + " = ?", width / 2, height / 4)
    elif question_type == "pow":
        # Displaying power question using string concatenation
        text(str(num1) + "^" + str(num2) + " = ?", width / 2, height / 4)

    fill(255, 220, 220)  # Soft red for answer boxes
    rect(width / 4 - 75, height / 2 - 50, 150, 100)
    rect(width / 2 - 75, height / 2 - 50, 150, 100)
    rect(3 * width / 4 - 75, height / 2 - 50, 150, 100)

    fill(0)
    textSize(24)  # Game screen answer text size
    text(int(correctAnswer), width / 4, height / 2)
    text(int(wrongAnswer1), width / 2, height / 2)
    text(int(wrongAnswer2), 3 * width / 4, height / 2)

    if isCorrect is not None:
        if isCorrect:
            fill(0, 255, 0)  # Green for correct
            textSize(32)  # Result message text size
            text("Correct!", width / 2, 3 * height / 4)
        else:
            fill(255, 0, 0)  # Red for incorrect
            textSize(32)  # Result message text size
            text("Incorrect! Negative marking applies.", width / 2, 3 * height / 4)

    fill(0)
    textAlign(LEFT, CENTER)
    textSize(20)  # Score and level text size
    text("Score: " + str(score), 20, 20)
    text("Level: " + str(level), 20, 50)

    # Draw pop-up shapes when level increases
    for shape in popper_shapes:
        fill(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ellipse(shape['x'], shape['y'], shape['size'], shape['size'])
        shape['y'] -= popper_speed
        shape['size'] -= 0.5
        if shape['size'] <= 0:
            popper_shapes.remove(shape)

def mousePressed():
    global game_state
    if game_state == "title":
        game_state = "game"
        generateQuestion()  # Transition to game state and generate the first question
    elif game_state == "game":
        checkAnswer()  # Check the selected answer and proceed to the next question

def checkAnswer():
    global num1, num2, correctAnswer, wrongAnswer1, wrongAnswer2, operation, isCorrect, score, level, consecutive_correct_answers
    selectedAnswer = None
    
    # Determine which answer box was clicked
    if (mouseX > width / 4 - 75 and mouseX < width / 4 + 75 and
        mouseY > height / 2 - 50 and mouseY < height / 2 + 50):
        selectedAnswer = correctAnswer
    elif (mouseX > width / 2 - 75 and mouseX < width / 2 + 75 and
          mouseY > height / 2 - 50 and mouseY < height / 2 + 50):
        selectedAnswer = wrongAnswer1
    elif (mouseX > 3 * width / 4 - 75 and mouseX < 3 * width / 4 + 75 and
          mouseY > height / 2 - 50 and mouseY < height / 2 + 50):
        selectedAnswer = wrongAnswer2

    # Check if the selected answer is correct and update score accordingly
    if selectedAnswer is not None:
        if selectedAnswer == answer:
            isCorrect = True
            score += 1
            consecutive_correct_answers += 1
        else:
            isCorrect = False
            score -= 1
            consecutive_correct_answers = 0  # Reset consecutive correct answers on wrong answer
        
        # Check if level should be increased
        if consecutive_correct_answers >= 5:
            level += 1
            consecutive_correct_answers = 0  # Reset after increasing level
            generatePopperShapes()  # Generate pop-up shapes when level increases
        
        generateQuestion()  # Generate the next question

def generateQuestion():
    global num1, num2, correctAnswer, wrongAnswer1, wrongAnswer2, operation, answer, level, question_type
    
    question_type = random.choice(["math", "pow"])  # Randomly select question type
    
    if question_type == "math":
        # Generate math question and answers
        num1 = random.randint(1, 5 * level)
        num2 = random.randint(1, 5 * level)
        operation_index = random.randint(0, 2)
        
        if operation_index == 0:
            operation = "+"
            answer = num1 + num2
        elif operation_index == 1:
            operation = "-"
            answer = num1 - num2
        elif operation_index == 2:
            operation = "*"
            answer = num1 * num2
        correctAnswer = answer
    
    elif question_type == "pow":
        # Generate power question and answers
        num1 = random.randint(1, 5)
        num2 = random.randint(1, 3)
        answer = math.pow(num1, num2)
        correctAnswer = int(answer)

    # Generate unique wrong answers
    wrongAnswer1 = correctAnswer
    while wrongAnswer1 == correctAnswer:
        wrongAnswer1 = int(correctAnswer + random.randint(-5, 5))
    
    wrongAnswer2 = correctAnswer
    while wrongAnswer2 == correctAnswer or wrongAnswer2 == wrongAnswer1:
        wrongAnswer2 = int(correctAnswer + random.randint(-5, 5))

    # Shuffle answers
    answers = [correctAnswer, wrongAnswer1, wrongAnswer2]
    random.shuffle(answers)
    correctAnswer, wrongAnswer1, wrongAnswer2 = answers

def changeBackgroundColor():
    global current_background_color, last_color_change_time
    if millis() - last_color_change_time > 2000:
        current_background_color = random.choice(background_colors)
        last_color_change_time = millis()

def generatePopperShapes():
    global popper_shapes
    for _ in range(random.randint(3, 5)):  # Generate between 3 to 5 shapes
        x = random.randint(50, width - 50)
        y = random.randint(height // 2, height - 50)
        size = random.randint(20, 40)
        popper_shapes.append({'x': x, 'y': y, 'size': size})
