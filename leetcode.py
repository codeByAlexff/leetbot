import requests
import random
import math
from bs4 import BeautifulSoup


def leetProblem(problem):

        url = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={problem}"

        response = requests.get(url)
        print(response.status_code)
        data = response.json()

        title = data["questionTitle"]
        difficulty = data["difficulty"]
        if data["question"] is None:
               return None, None, None, None, None
        clean_question = BeautifulSoup(data["question"], "html.parser").get_text()
        hints = data["hints"]
        question_id = data["questionId"]
            
        return question_id, title, difficulty, clean_question, hints
       
       

def leetUser(user):
        url = f"https://alfa-leetcode-api.onrender.com/{user}"

        response = requests.get(url)
        data = response.json()

        username = data["username"]
        avatar = data["avatar"]
        ranking = data["ranking"]
        github = data["gitHub"]
        about = data["about"]

        return username, avatar, ranking, github, about

def dailyProblem():
        url = "https://alfa-leetcode-api.onrender.com/daily"

        response = requests.get(url)
        data = response.json()

        dailyDate = data["date"]
        title = data["questionTitle"]
        question_id = data["questionId"]
        diff = data["difficulty"]
        clean_question = BeautifulSoup(data["question"], "html.parser").get_text()
        slug = data["titleSlug"]

        return title, dailyDate, question_id, diff, clean_question, slug

def randomProblem(diff=None):
    skip_value = random.randint(0,2900)
    url = f"https://alfa-leetcode-api.onrender.com/problems?limit=100&skip={skip_value}"
    response = requests.get(url)
    data = response.json()
    questionList = []
    if diff == None:
        randomQuestion = random.choice(data["problemsetQuestionList"])
        return randomQuestion
    elif diff == "easy" or diff == "medium" or diff == "hard":
        diff_formatted = diff.capitalize()
        for i in data["problemsetQuestionList"]:
                  if i["difficulty"] == diff_formatted:
                         questionList.append(i)
        if len(questionList) == 0:
               return randomProblem(diff)
        randomQuestion = random.choice(questionList)
        return randomQuestion
    else:
           raise ValueError("Difficulty value error. Try easy, medium, or hard")


