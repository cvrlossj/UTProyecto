from django.shortcuts import render, redirect
from django.http import JsonResponse
# Vistas Genericas
from django.views.generic import TemplateView, View
# Utilidades
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Formularios propios
from .forms import AddJuntaVecinos
# Modelos
from accounts.models import Comuna, Perfiles
from .models import JuntaVecinos
# Mensajes
from django.contrib import messages

# Cargar Perfiles por Comuna
def get_perfiles_by_comuna(request, comuna_id):
    perfiles = Perfiles.objects.filter(id_comuna=comuna_id, id_rol=2).exclude(juntavecinos__isnull=False)
    perfiles_list = list(perfiles.values('rut', 'nombre', 'apellido'))
    return JsonResponse(perfiles_list, safe=False)

# Cargar comunas
def load_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = Comuna.objects.filter(id_region=region_id).order_by('nombre_comuna')
    comunas_list = [{'id': comuna.id_comuna, 'nombre': comuna.nombre_comuna} for comuna in comunas]
    return JsonResponse(comunas_list, safe=False)

@method_decorator(login_required, name='dispatch')
class JuntaVecinosView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = AddJuntaVecinos()
        juntas = JuntaVecinos.objects.select_related('id_comuna', 'id_comuna__id_region').all()
        
        context = {
            'user': user,
            'form': form,
            'juntas': juntas,
        }
        return render(request, 'dashboarda/listajuntavecinos.html', context)
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        
        if action == 'create':
            return self.create_junta_vecinos(request)
        elif action == 'edit':
            return self.edit_junta_vecinos(request)
        
        return redirect('dashboarda:juntavecinos')
    
    def create_junta_vecinos(self, request):
        form = AddJuntaVecinos(data=request.POST)
        if form.is_valid():
            try:
                nombre_organizacion = form.cleaned_data['nombreOrganizacion']
                fecha_integracion = form.cleaned_data['fechaIntegracion']
                direccion = form.cleaned_data['direccionOrganizacion']
                comuna = form.cleaned_data['comunaOrganizacion']
                
                junta_vecinos = JuntaVecinos.objects.create(
                    nombre_organizacion=nombre_organizacion,
                    fecha_integracion=fecha_integracion,
                    direccion=direccion,
                    id_comuna=comuna,
                    id_estado_id=1
                )        
                
                perfiles = form.cleaned_data.get('perfilesOrganizacion')
                if perfiles:
                    junta_vecinos.perfiles.add(*perfiles)
                
                messages.success(request, f'Junta de Vecino con nombre {nombre_organizacion} creada correctamente')
                return redirect('dashboarda:juntavecinos')
                
            except Exception as e:
                messages.error(request, f'Error al crear la Junta de Vecino: {str(e)}')
                return redirect('dashboarda:juntavecinos')
        else:
            print("Errores del formulario:", form.errors)
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
            return render(request, 'dashboarda/listajuntavecinos.html', {
                'form': form,
                'juntas': JuntaVecinos.objects.select_related('id_comuna', 'id_comuna__id_region').all(),
                'user': request.user
            })
            
@method_decorator(login_required, name='dispatch')
class DashboardAdminView(TemplateView):
    template_name = 'dashboarda/dashboardadmin.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        total_juntas = JuntaVecinos.objects.count()
        habilitadas_juntas = JuntaVecinos.objects.filter(id_estado=1).count()
        inhabilitadas_juntas = JuntaVecinos.objects.filter(id_estado=2).count()
        
        context.update({
            'user': user,
            'total_juntas': total_juntas,
            'habilitadas_juntas': habilitadas_juntas,
            'inhabilitadas_juntas': inhabilitadas_juntas
        })
        return context