import json
import os

from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render

from Aplicaciones.Mascota.models import Mascota
from Aplicaciones.Persona.models import Persona

from .models import Adopcion