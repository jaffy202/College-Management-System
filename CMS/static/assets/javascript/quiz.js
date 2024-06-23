//References
let timeLeft = document.querySelector(".time-left");
let quizContainer = document.getElementById("container");
let nextBtn = document.getElementById("next-button");
let countOfQuestion = document.querySelector(".number-of-question");
let displayContainer = document.getElementById("display-container");
let scoreContainer = document.querySelector(".score-container");
let restart = document.getElementById("restart");
let userScore = document.getElementById("user-score");
let startScreen = document.querySelector(".start-screen");
let startButton = document.getElementById("start-button");
let questionCount;
let scoreCount = 0;
let count = 31;
let countdown;

//Questions and Options array

const quizArray = [
    {
        id: "0",
        question: "A train running at the speed of 60 km/hr crosses a pole in 9 seconds. What is the length of the train?",
        options: ["120 meters", "150 meters", "180 meters", "240 meters"],
        correct: "180 meters",
    },
    {
        id: "1",
        question: "A man can row 50 km downstream and 30 km upstream in 10 hours. He can row 40 km downstream and 24 km upstream in 8 hours. What is the speed of the man in still water?",
        options: ["6 km/hr", "8 km/hr", "10 km/hr", "12 km/hr"],
        correct: "8 km/hr",
    },
    {
        id: "2",
        question: "A ladder 15 meters long just reaches the top of a wall 9 meters high. What is the distance of the foot of the ladder from the wall?",
        options: ["12 meters", "10 meters", "6 meters", "8 meters"],
        correct: "12 meters",
    },
    {
        id: "3",
        question: "A can do a piece of work in 15 days and B in 20 days. They work together for 4 days, and then A leaves. In how many more days will B finish the work?",
        options: ["4 days", "6 days", "8 days", "10 days"],
        correct: "6 days",
    },
    {
        id: "4",
        question: "The simple interest on a sum of money at 4% per annum for 3 years is $240. What is the sum?",
        options: ["$2000", "$2500", "$3000", "$3500"],
        correct: "$3000",
    },
    {
        id: "5",
        question: "At what rate percent per annum will the compound interest on a sum of money be 1/16 of the sum in 2 years?",
        options: ["4%", "6%", "8%", "10%"],
        correct: "6%",
    },
    {
        id: "6",
        question: "A trader marks his goods 20% above cost price and allows a discount of 10%. What is his gain percent?",
        options: ["8%", "9%", "10%", "12%"],
        correct: "8%",
    },
    {
        id: "7",
        question: "A, B and C enter into a partnership. A invests $6000 for 8 months, B invests $8000 for 10 months, and C invests $10000 for 12 months. If the total profit is $13200, then B's share in the profit is?",
        options: ["$2400", "$2800", "$3200", "$3600"],
        correct: "$3200",
    },
    {
        id: "8",
        question: "If 20% of a number is equal to two-third of another number, what is the ratio of first number to the second?",
        options: ["2:3", "3:2", "4:3", "3:4"],
        correct: "3:4",
    },
    {
        id: "9",
        question: "A father is four times as old as his son. After 5 years, he will be three times as old as his son. What is the present age of the father?",
        options: ["30 years", "40 years", "45 years", "50 years"],
        correct: "40 years",
    },
    {
        id: "10",
        question: "What day of the week was it on 17th June 1998?",
        options: ["Monday", "Tuesday", "Wednesday", "Thursday"],
        correct: "Wednesday",
    },
    {
        id: "11",
        question: "If the time by the clock is 2:45 PM, then what is the angle between the hands of the clock?",
        options: ["112.5 degrees", "120 degrees", "135 degrees", "150 degrees"],
        correct: "112.5 degrees",
    },
    {
        id: "12",
        question: "The average of first 50 natural numbers is?",
        options: ["25.5", "25", "26", "25.25"],
        correct: "25.5",
    },
    {
        id: "13",
        question: "The area of a square field is 24200 sq m. What is the cost of fencing it at $3.50 per meter?",
        options: ["$33810", "$34980", "$36320", "$37490"],
        correct: "$36320",
    },
    {
        id: "14",
        question: "The volume of a cube is 13824 cm³. What is its surface area?",
        options: ["10368 cm²", "12960 cm²", "15552 cm²", "17280 cm²"],
        correct: "17280 cm²",
    },
    {
        id: "15",
        question: "In how many different ways can the letters of the word 'LEADER' be arranged?",
        options: ["360", "720", "1440", "2880"],
        correct: "720",
    },
    {
        id: "16",
        question: "The sum of three consecutive odd numbers is 57. What is the middle number?",
        options: ["17", "19", "21", "23"],
        correct: "19",
    },
    {
        id: "17",
        question: "Find the greatest number that will divide 43, 91, and 183 so as to leave the same remainder in each case.",
        options: ["4", "6", "8", "10"],
        correct: "4"
    },
    {
        id: "18",
        question: "The LCM of two numbers is 120 and their HCF is 5. If one of the numbers is 15, find the other number.",
        options: ["20", "24", "30", "36"],
        correct: "24",
    },
    {
        id: "19",
        question: "If the price of an article is increased by 20% and then decreased by 10%, what is the net percentage change?",
        options: ["8%", "10%", "12%", "14%"],
        correct: "8%",
    },
    {
        id: "20",
        question: "The average of 5 numbers is 16. If one number is excluded, the average becomes 15. What is the excluded number?",
        options: ["10", "12", "15", "20"],
        correct: "20",
    },
    {
        id: "21",
        question: "If the area of a circle is 154 square meters, what is its circumference?",
        options: ["28 meters", "33 meters", "36 meters", "44 meters"],
        correct: "28 meters",
    },
    {
        id: "22",
        question: "What is the probability of getting a sum of 8 when two dice are thrown?",
        options: ["1/6", "1/9", "1/12", "1/36"],
        correct: "5/36",
    },
    {
        id: "23",
        question: "What is the unit's digit in the product (784 x 618 x 917)?",
        options: ["2", "4", "6", "8"],
        correct: "2",
    },
    {
        id: "24",
        question: "The least number which when divided by 5, 6, 7, and 8 leaves a remainder 3, but when divided by 9 leaves no remainder, is?",
        options: ["1677", "1683", "1687", "1693"],
        correct: "1683",
    }
];

//Restart Quiz
restart.addEventListener("click", () => {
    initial();
    displayContainer.classList.remove("hide");
    scoreContainer.classList.add("hide");
});

//Next Button
nextBtn.addEventListener(
    "click",
    (displayNext = () => {
        //increment questionCount
        questionCount += 1;
        //if last question
        if (questionCount == quizArray.length) {
            //hide question container and display score
            displayContainer.classList.add("hide");
            scoreContainer.classList.remove("hide");
            //user score
            userScore.innerHTML =
                "Your score is " + scoreCount + " out of " + questionCount;
        } else {
            //display questionCount
            countOfQuestion.innerHTML =
                questionCount + 1 + " of " + quizArray.length + " Question";
            //display quiz
            quizDisplay(questionCount);
            count = 31;
            clearInterval(countdown);
            timerDisplay();
        }
    })
);

//Timer
const timerDisplay = () => {
    countdown = setInterval(() => {
        count--;
        timeLeft.innerHTML = `${count}s`;
        if (count == 0) {
            clearInterval(countdown);
            displayNext();
        }
    }, 1000);
};

//Display quiz
const quizDisplay = (questionCount) => {
    let quizCards = document.querySelectorAll(".container-mid");
    //Hide other cards
    quizCards.forEach((card) => {
        card.classList.add("hide");
    });
    //display current question card
    quizCards[questionCount].classList.remove("hide");
};

//Quiz Creation
function quizCreator() {
    //randomly sort questions
    quizArray.sort(() => Math.random() - 0.5);
    //generate quiz
    for (let i of quizArray) {
        //randomly sort options
        i.options.sort(() => Math.random() - 0.5);
        //quiz card creation
        let div = document.createElement("div");
        div.classList.add("container-mid", "hide");
        //question number
        countOfQuestion.innerHTML = 1 + " of " + quizArray.length + " Question";
        //question
        let question_DIV = document.createElement("p");
        question_DIV.classList.add("question");
        question_DIV.innerHTML = i.question;
        div.appendChild(question_DIV);
        //options
        div.innerHTML += `
    <button class="option-div" onclick="checker(this)">${i.options[0]}</button>
     <button class="option-div" onclick="checker(this)">${i.options[1]}</button>
      <button class="option-div" onclick="checker(this)">${i.options[2]}</button>
       <button class="option-div" onclick="checker(this)">${i.options[3]}</button>
    `;
        quizContainer.appendChild(div);
    }
}

//Checker Function to check if option is correct or not
function checker(userOption) {
    let userSolution = userOption.innerText;
    let question =
        document.getElementsByClassName("container-mid")[questionCount];
    let options = question.querySelectorAll(".option-div");

    //if user clicked answer == correct option stored in object
    if (userSolution === quizArray[questionCount].correct) {
        userOption.classList.add("correct");
        scoreCount++;
    } else {
        userOption.classList.add("incorrect");
        //For marking the correct option
        options.forEach((element) => {
            if (element.innerText == quizArray[questionCount].correct) {
                element.classList.add("correct");
            }
        });
    }

    //clear interval(stop timer)
    clearInterval(countdown);
    //disable all options
    options.forEach((element) => {
        element.disabled = true;
    });
}

//initial setup
function initial() {
    quizContainer.innerHTML = "";
    questionCount = 0;
    scoreCount = 0;
    count = 31;
    clearInterval(countdown);
    timerDisplay();
    quizCreator();
    quizDisplay(questionCount);
}

//when user click on start button
startButton.addEventListener("click", () => {
    startScreen.classList.add("hide");
    displayContainer.classList.remove("hide");
    initial();
});

//hide quiz and display start screen
window.onload = () => {
    startScreen.classList.remove("hide");
    displayContainer.classList.add("hide");
};