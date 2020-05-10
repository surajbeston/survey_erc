from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from .models import User, Progress, Answer
import random
import json
from datetime import datetime


question_arr = [["What is your favourite favourite food while in ERC?", [["Chow Mein", "http://localhost:8001/brand_images/img/chowmein.jpeg"], ["Samosa", "http://localhost:8001/brand_images/img/samosa.jpg"], ["Momo", "http://localhost:8001/brand_images/img/momo.jpeg"], ["Paratha", "http://localhost:8001/brand_images/img/paratha.jpg"]]], ["Which on of them is your most preferred fooding place?", [["Aale", "http://localhost:8001/brand_images/img/aale.jpg"], ["Baale", "http://localhost:8001/brand_images/img/baale.jpg"] \
    , ["Baans Ghari", "http://localhost:8001/brand_images/img/baansghari.jpg"], ["Siddhakali Chowmein", "siddhakalichowmein.jpg"], ["Campus Canteen", "http://localhost:8001/brand_images/img/canteen.jpg"], ["Namsal Canteen", "http://localhost:8001/brand_images/img/namsalcanteen.jpg"]]], \
    ["Who is the most influential person in ERC (Male)?", [["Anil Panta", "http://localhost:8001/brand_images/img/anil.jpg"], ["Pratik Shrestha", "http://localhost:8001/brand_images/img/pratik.jpg"], ["Anup Paudel", "http://localhost:8001/brand_images/img/anup.jpg"], ["Nauneet Tiwari", "http://localhost:8001/brand_images/img/nauneet.jpg"], ["Rohit Century", "http://localhost:8001/brand_images/img/rohit.jpg"], ["Bibesh Mote", "http://localhost:8001/brand_images/img/bibesh.jpg"], ["Badri Karki", "http://localhost:8001/brand_images/img/badri.jpg"], ["Pawan Karkey", "http://localhost:8001/brand_images/img/pawan.jpg"]]], \
            ["Who is the most influential person in ERC (Female)?", [["Samjhana Bhetwal", "http://localhost:8001/brand_images/img/samjhana.jpg"], ["Binita Paudel", "http://localhost:8001/brand_images/img/binita.jpg"], ["Shakshi Chaudhary", "http://localhost:8001/brand_images/img/shakshi.jpg"], ["Anju Yadav", "http://localhost:8001/brand_images/img/anju.jpg"], ["Laxmi Bhattarai", "http://localhost:8001/brand_images/img/laxmi.jpg"], ["Dikshya Kafle", "http://localhost:8001/brand_images/img/dikshya.jpg"], ["Kritika Adhikari", "http://localhost:8001/brand_images/img/kritika.jpg"]]], \
                ["Which of these is your favourite sports?", [["Football", "http://localhost:8001/brand_images/img/football.jpg"], ["Cricket", "http://localhost:8001/brand_images/img/cricket.jpg"], ["Basketball", "http://localhost:8001/brand_images/img/basketball.jpg"], ["Volleyball", "http://localhost:8001/brand_images/img/volleyball.jpg"], ["Table Tennis", "http://localhost:8001/brand_images/img/tt.jpg"], ["Badminton", "http://localhost:8001/brand_images/img/badminton.jpg"]]],
                ["Which on these is the most useful gate?", [["Front Gate", "http://localhost:8001/brand_images/img/frontgate.jpg"], ["Back Gate", "http://localhost:8001/brand_images/img/backgate.jpg"]]], ["Which one of these is the most influential campus personel?", [["Samir Sakya", "http://localhost:8001/brand_images/img/samir.jpg"], ["Om Prakash Dhakal", "http://localhost:8001/brand_images/img/opd.jpg"], ["Anu Shrestha", "http://localhost:8001/brand_images/img/anu.jpg"], ["Manoj Kumar Guragain", "http://localhost:8001/brand_images/img/mkg.jpg"], ["Yagya Raj Subedi", "http://localhost:8001/brand_images/img/yrs.jpg"], ["Nabaraj Paudel","http://localhost:8001/brand_images/img/nabaraj.jpg"], \
                     ["Bishnu Chaudhary", "http://localhost:8001/brand_images/img/bishnu.jpg"], ["Sagar Kafle", "http://localhost:8001/brand_images/img/sagar.jpg"]]] \
            ,["Which chowk do you prefer?", [["Langhali Chowk", "http://localhost:8001/brand_images/img/langhali.jpg"],["Bargachi", "http://localhost:8001/brand_images/img/bargachi.jpg"], ["Sampang Chowk", "http://localhost:8001/brand_images/img/sampang.jpg"], ["Mahadev Chowk", "http://localhost:8001/brand_images/img/mahadev.jpg"], ["Bishal Chowk", "http://localhost:8001/brand_images/img/bishal.jpg"],  ["Shyam Chowk", "http://localhost:8001/brand_images/img/shyam.jpg"], ["Siddhakali Chowk", "http://localhost:8001/brand_images/img/siddhakali.jpg"]]], \
                ["Your favourite playground?", [["New Cricket Ground", "http://localhost:8001/brand_images/img/cricketground.png"], ["ERC Stadium", "http://localhost:8001/brand_images/img/footballstadium.jpg"], ["Mechanical Chautari Courts", "http://localhost:8001/brand_images/img/mechanicalcourt.jpg"], ["Front Ground(Basketball & Volleyball)", "http://localhost:8001/brand_images/img/basketballcourt.jpg"]]]] 

def home(request):
    try:
        email = request.session["email"] 
        return redirect("questioner")
    except KeyError:
        print ("User isn't logged in...")

    if request.method == "GET":
        context = {}
        context.update(csrf(request))
        return render(request,"home.html", context)
    if request.method == "POST":
        print (request.POST)
        try:
            name = request.POST["name"]
            email = request.POST["email"]
            image = request.POST["img"]
            obj = User.objects.filter(email = email)
            user = User(full_name = name, email = email, image = image)
            user.save()
            print ("reached here1 ")
            request.session["email"] = email
            arr_natural = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            random.shuffle(arr_natural)
            progress = Progress(user = user, in_question = 0, last_questions = arr_natural, random_iter = random.randrange(1, 9))
            progress.save()
            print ("reached here 2")
            return redirect("questioner")
        except KeyError:
            print ("No data Provided")
            return HttpResponse("No credentials. You must not signed with google.")

def questioner(request):
    if request.method == "GET":
        print ("Reached here")
        try:
            email = request.session["email"]
        except KeyError:
            return redirect("home")
        progress = Progress.objects.get(user__email = email)
        print (progress.in_question)
        if progress.in_question < 9:
            question_no = progress.last_questions[progress.in_question]
            progress.in_question += 1
            print ("over here")
            print (question_no)
            progress.track_time = datetime.now()
            progress.save()
            question = question_arr[question_no]
            random.shuffle(question[1])

            context = {"question": question[0], "options": question[1], "question_no": progress.in_question}
            context.update(csrf(request))

            return render(request, "question.html", context)
        else:
            return render(request, "question.html", {"error": "Thanks for participating in this. We will be posting the average very soon... And we really don't want anything from the offendees, neither punches nor lawsuits, just keep it to yourself , \"Sorry, no sorry\"."})
    if request.method == "POST":
        try: 
            question = request.POST["question"]
            answer = request.POST["answer"]
            time = request.POST["time"]
            time = json.loads('['+time[:-1]+']')
            try: 
                email = request.session["email"]
            except KeyError:
                return redirect("home")
            user = User.objects.get(email = email)
            progress = Progress.objects.get(user = user)
            delay = datetime.now() - progress.track_time
            obj = Answer(user = user, question = question, answer = answer, hover_duration = time, time_duration = delay.microseconds)
            obj.save()
            return redirect("questioner")
        except KeyError:
            return HttpResponse("Something went wrong. Return to <a href = \"/question\" >Questions</a>.")

            