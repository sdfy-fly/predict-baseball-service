import datetime

from django.shortcuts import render, redirect

from .playerDetails.playerDetailsViews import PlayersDetail
from .schedule.scheduleViews import GetSchesule, GetInjuryNews

from asgiref.sync import sync_to_async, async_to_sync

from rest_framework.views import APIView
from rest_framework.response import Response


