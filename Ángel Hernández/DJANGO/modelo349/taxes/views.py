from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import SujetoForm, DeclaracionForm, OperadorFormSet
from .models import Declaracion349, SujetoPasivo
from .serializers import DeclaracionSerializer, SujetoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv
from django.http import HttpResponse

# WEB: formulario con formset
class HomeView(View):
    def get(self, request):
        sujeto_form = SujetoForm()
        decl_form = DeclaracionForm()
        formset = OperadorFormSet()
        return render(request, 'taxes/form.html', {'sujeto_form': sujeto_form, 'decl_form': decl_form, 'formset': formset})

    def post(self, request):
        sujeto_form = SujetoForm(request.POST)
        decl_form = DeclaracionForm(request.POST)
        if sujeto_form.is_valid() and decl_form.is_valid():
            sujeto = SujetoPasivo.objects.filter(nif=sujeto_form.cleaned_data['nif']).first()
            if not sujeto:
                sujeto = sujeto_form.save()
            decl = decl_form.save(commit=False)
            decl.sujeto = sujeto
            decl.save()
            formset = OperadorFormSet(request.POST, instance=decl)
            if formset.is_valid():
                formset.save()
                # actualizar totales
                ops = decl.operadores.all()
                decl.total_operadores = ops.count()
                decl.total_base_imponible = sum([o.base_imponible for o in ops])
                decl.save()
                return render(request, 'taxes/result.html', {'declaracion': decl})
            else:
                # si formset no válido, mostramos errores
                return render(request, 'taxes/form.html', {'sujeto_form': sujeto_form, 'decl_form': decl_form, 'formset': formset})
        else:
            formset = OperadorFormSet(request.POST)
            return render(request, 'taxes/form.html', {'sujeto_form': sujeto_form, 'decl_form': decl_form, 'formset': formset})

# API: listar y crear declaraciones
class DeclaracionListCreateAPI(APIView):
    def get(self, request):
        qs = Declaracion349.objects.all().order_by('-created_at')
        serializer = DeclaracionSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeclaracionSerializer(data=request.data)
        if serializer.is_valid():
            decl = serializer.save()
            return Response(DeclaracionSerializer(decl).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API: crear/listar sujetos
class SujetoListCreateAPI(APIView):
    def get(self, request):
        qs = SujetoPasivo.objects.all()
        serializer = SujetoSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SujetoSerializer(data=request.data)
        if serializer.is_valid():
            sujeto = serializer.save()
            return Response(SujetoSerializer(sujeto).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Export CSV
def export_declaracion_csv(request, pk):
    decl = get_object_or_404(Declaracion349, pk=pk)
    rows = decl.operadores.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="modelo349_{decl.id}.csv"'
    writer = csv.writer(response)
    writer.writerow(['NIF_operador','Nombre','Pais','Clave','Base_imponible','Observaciones'])
    for op in rows:
        writer.writerow([op.nif_operador, op.nombre, op.pais, op.clave, str(op.base_imponible), op.observaciones or ''])
    return response
