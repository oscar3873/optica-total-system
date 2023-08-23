from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import (CreateView, View, DetailView)
from django.views.generic.edit import (FormView,)

from .models import *
from .forms import CustomerForm, HealthInsuranceForm, CalibrationOrderForm



class CalibrationOrderCreateView(LoginRequiredMixin, FormView):
    form_class = CalibrationOrderForm
    template_name = 'clients/lab_form.html'
    success_url = reverse_lazy('core_app:home')
    
    def form_valid(self, form):
        correc = Correction.objects.create(
            lej_od_esferico = form.cleaned_data['lej_od_esferico'], #el primer lej_od_esferico hace referencia al models y el segundo hace referencia al forms
            lej_od_cilindrico = form.cleaned_data['lej_od_cilindrico'],
            lej_od_eje = form.cleaned_data['lej_od_eje'],
            lej_oi_esferico = form.cleaned_data['lej_oi_esferico'],
            lej_oi_cilindrico = form.cleaned_data['lej_oi_cilindrico'],
            lej_oi_eje = form.cleaned_data['lej_oi_eje'],
            cer_od_esferico = form.cleaned_data['cer_od_esferico'],
            cer_od_cilindrico = form.cleaned_data['cer_od_cilindrico'],
            cer_od_eje = form.cleaned_data['cer_od_eje'],
            cer_oi_esferico = form.cleaned_data['cer_oi_esferico'],
            cer_oi_cilindrico = form.cleaned_data['cer_oi_cilindrico'],
            cer_oi_eje = form.cleaned_data['cer_oi_eje'],
        )
        mat = Material.objects.create(
            policarbonato = form.cleaned_data['policarbonato'],
            organic = form.cleaned_data['organic'],
            mineral = form.cleaned_data['mineral'],
            m_r8 = form.cleaned_data['m_r8']
        )
        col = Color.objects.create(
            white = form.cleaned_data['white'],
            full_gray = form.cleaned_data['full_gray'],
            gray_gradient = form.cleaned_data['gray_gradient'],
            flat_sepia = form.cleaned_data['flat_sepia']
        )
        cris = Cristal.objects.create(
            monofocal = form.cleaned_data['monofocal'],
            bifocal_fv = form.cleaned_data['bifocal_fv'],
            bifocal_k = form.cleaned_data['bifocal_k'],
            bifocal_pi = form.cleaned_data['bifocal_pi'],
            progressive = form.cleaned_data['progressive']
        )
        trat = Tratamient.objects.create(
            antireflex = form.cleaned_data['antireflex'],
            filtro_azul = form.cleaned_data['filtro_azul'],
            fotocromatico = form.cleaned_data['fotocromatico'],
            ultravex = form.cleaned_data['ultravex'],
            polarizado = form.cleaned_data['polarizado'],
            neutrosolar = form.cleaned_data['neutrosolar']
        )
        interpup = Interpupillary.objects.create(
            lej_od_nanopupilar = form.cleaned_data['lej_od_nanopupilar'],
            lej_od_pelicula = form.cleaned_data['lej_od_pelicula'],
            lej_oi_nanopupilar = form.cleaned_data['lej_oi_nanopupilar'],
            lej_oi_pelicula = form.cleaned_data['lej_oi_pelicula'],
            lej_total = form.cleaned_data['lej_total'],
            cer_od_nanopupilar = form.cleaned_data['cer_od_nanopupilar'],
            cer_od_pelicula = form.cleaned_data['cer_od_pelicula'],
            cer_oi_nanopupilar = form.cleaned_data['cer_oi_nanopupilar'],
            cer_oi_pelicula = form.cleaned_data['cer_oi_pelicula'],
            cer_total = form.cleaned_data['cer_total']
        )
        Calibration_Order.objects.create(
            is_done = form.cleaned_data['is_done'],
            correction = correc,
            material = mat,
            color = col,
            type_cristal = cris,
            tratamient = trat,
            interpupillary = interpup,
            medical_details = form.cleaned_data['medical_details'],
            employees = form.cleaned_data['employees'],
            armazon = form.cleaned_data['armazon'],
            observations = form.cleaned_data['observations']
        )
        return super().form_valid(form)

    
class CustomerCreateView(LoginRequiredMixin, FormView):
    form_class = CustomerForm
    template_name = 'clients/customer_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        customer_data = form.cleaned_data
        Customer.objects.create_customer(**customer_data)
        return super().form_valid(form)


class HealthInsuranceCreateView(LoginRequiredMixin, FormView):
    form_class = HealthInsuranceForm
    template_name = 'clients/insurance_form.html'
    success_url = reverse_lazy('core_app:home')

    def form_valid(self, form):
        HealthInsurance.objects.create(
            name = form.cleaned_data['name'],
            cuit = form.cleaned_data['cuit']
        )
        return super().form_valid(form)