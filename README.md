# Python Projects by Ieva

This repository contains a collection of Python scripts developed for various assignments. Each script showcases different aspects of Python programming, including working with Numpy arrays, creating a number guessing game, data visualization, and image processing.

## Table of Contents

- [Task 1A: Numpy Arrays](#task-1a-numpy-arrays)
- [Task 1B: Guess the Number Game](#task-1b-guess-the-number-game)
- [Task 1C: Multiplication Table Trainer](#task-1c-multiplication-table-trainer)
- [Task 3: Data Visualization and Image Processing](#task-3-data-visualization-and-image-processing)
- [Task 4: Visual Stimuli Generation](#task-4-visual-stimuli-generation)
- [Task 5: Final Behavioral Data Analysis Project](#task-5-final-behavioral-data-analysis-project)

---

## Task 1A: Numpy Arrays

### Overview
This script demonstrates basic operations with Numpy arrays, including array creation, mathematical operations, and filtering elements based on conditions.

### Key Features
- **Array Creation:** Arrays `a` and `b` are created using Numpy.
- **Operations:** Compute the size, mean, median, and sum of the arrays. Perform element-wise operations such as addition, subtraction, and modulus.
- **Odd Number Extraction:** Extract odd numbers from arrays `a` and `b`.
- **Range Array:** Generate arrays containing all integer values between 1 and 10,000 using different methods.

### Usage
Simply run the script, and the results will be printed to the console.

---

## Task 1B: Guess the Number Game

### Overview
This is a simple number guessing game where the user has up to six attempts to guess a random number between 1 and 100.

### Key Features
- **Random Number Generation:** The script generates a random number between 1 and 100.
- **User Interaction:** The user is prompted to guess the number, with feedback provided on whether the guess is too high or too low.
- **Win/Loss Conditions:** The game informs the user if they guessed the number correctly or if they ran out of attempts.

### Usage
Run the script and follow the on-screen instructions to guess the number.

---

## Task 1C: Multiplication Table Trainer

### Overview
This script helps users practice multiplication tables by generating random multiplication problems.

### Key Features
- **Random Problems:** The user selects a multiplication table to practice, and the script generates random problems.
- **Feedback:** The script provides feedback on whether the user's answer is correct.
- **Exit Option:** Users can quit the game by pressing 'q'.

### Usage
Run the script, input the desired multiplication table, and solve the problems.

---

## Task 3: Data Visualization and Image Processing

### Part 1: Eye Velocity Data Visualization
This script visualizes eye velocity data over time using Matplotlib.

- **Plotting:** The script plots eye velocity against time and marks the average velocity with a dashed line.
- **Histogram:** A histogram of eye movement velocities is generated to analyze the distribution.

### Part 2: Image Display and Manipulation
This script demonstrates loading and manipulating images using Matplotlib, PIL, and OpenCV.

- **Image Display:** Display multiple images individually and as a 2x2 grid.
- **Image Manipulation:** Rotate, resize, and concatenate images using OpenCV.
- **Image Saving:** The final image is saved as both a JPG and PDF.

### Usage
Ensure you have the required image files (`1.png`, `2.png`, `3.png`, `4.png`) in the working directory. Run the script to see the visualizations and image manipulations.

---

## Task 4: Visual Stimuli Generation

### Overview
This script generates visual stimuli consisting of a target shape among distractors, useful for psychology experiments.

### Key Features
- **Background Setup:** Define the background size and color.
- **Target and Distractors:** Specify properties such as shape, size, color, and number for both the target and distractors.
- **Random Placement:** The target and distractors are randomly placed on the background.
- **Image Saving:** The generated stimuli are saved as an image file.

### Usage
Run the script, and the stimuli image will be saved in the `Stimuli` directory.

---

## Task 5: Final Behavioral Data Analysis Project

### Overview
This script completes data wrangling procedures, visualizes datasets of interest, runs mixed effects models, and performs inferential statistical analyses.

### Key Features
- **Data Management:** Handles data loading, preprocessing, and management, including column renaming and condition-based categorization.
- **Analysis:** Performs various analyses such as repeated measures ANOVA and mixed effects models on different datasets.
- **Visualization:** Generates plots and visualizations for accuracy, response time, and memory specificity data.

### Usage
Ensure all required libraries are installed before running the script. Update file paths in the script as needed for local data access. Run the script in a Python environment with necessary dependencies.

### Dependencies
- pandas
- numpy
- matplotlib
- statsmodels
- seaborn
- scipy

### Notes
- This script performs extensive data wrangling and visualization. Ensure the input data is correctly formatted as specified in the script.
- Results will be saved in specified directories; ensure appropriate permissions and paths are set.

---

For further details on any of the scripts, refer to their individual sections or the comments within the scripts themselves.
