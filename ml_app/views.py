from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm, ImageForm, ImageUploadForm
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
import torch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import functional as F
from torchmetrics.functional import accuracy
import pytorch_lightning as pl
import torchvision
from ml_app.models import Net

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


# model = Net()
# net = Net().cpu().eval()
# net.load_state_dict(torch.load('ml_app/yolov5s.pt',
#                     map_location=torch.device('cpu')))


def index(request):
    image_url = ''
    result = ''
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image_name = request.FILES['image']
            image_url = 'media/documents/{}'.format(image_name)
            result = model(image_url)
            result = result.display(show=True)
        return render(request, '../templates/result.html', {'image_url': image_url, 'result': result})
    else:
        form = ImageForm()
        return render(request, '../templates/index.html', {'form': form})


class Login(LoginView):
    form_class = LoginForm
    template_name = '../templates/login.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            new_user = authenticate(username=username, password=password)

            if new_user is not None:
                login(request, new_user)
                return redirect('login')

    else:
        form = SignUpForm()
    return render(request, '../templates/signup.html', {'form': form})


class Logout(LogoutView):
    template_name = '../templates/base.html'


def result(request):
    # form = ImageForm(request.POST, request.FILES)
    # if request.method == 'POST':
    #     if form.is_valid():
    #         form.save()
    #         image_name = request.FILES['image']
    #         image_url = 'media/documents/{}'.format(image_name)
    #         img = preprocess(image_url)
    #         y = net(img)
    #         inference = torch.argmax(y)
    #         inference = inference.detach().numpy()

    #         probability = F.softmax(y)
    #         probability = (probability.max() * 100).detach().numpy()

    #         SaveModel.objects.create(
    #             inference=inference, probability=probability)

    return render(request, '../templates/result.html')
    # else:
    #     form = ImageForm()
    #     return render(request, '../templates/index.html', {'form': form})
