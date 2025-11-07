# Impuesto_411/views.py
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from .models import Formulario411

TASA_IMPUESTO = Decimal("0.003")  # 0,3 %
DOS_DECIMALES = Decimal("0.01")


def formulario_411(request):
  if request.method == "GET":
    return render(request, "Impuesto_411/411.html")
  return JsonResponse({"ok": False, "error": "Use ${PROJECT_ROOT}/api/impuesto411/ para POST"}, status=405)


@csrf_exempt
def impuesto_411_api(request):
  if request.method != "POST":
    return JsonResponse({"ok": False, "error": "Method not allowed"}, status=405)

  ctype = (request.META.get("CONTENT_TYPE") or "").lower()
  if "application/json" in ctype:
    try:
      payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
      return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)
  else:
    payload = request.POST.dict()

  def to_decimal(v):
    return Decimal(str(v).replace(",", "."))

  try:
    errores = []

    def _obtener_campo_obligatorio(nombre):
      valor = payload.get(nombre)
      if valor is None:
        errores.append(f"Falta el campo '{nombre}'.")
        return ""
      valor_str = str(valor).strip()
      if valor_str == "":
        errores.append(f"Falta el campo '{nombre}'.")
      return valor_str

    nif = _obtener_campo_obligatorio("nif").upper()
    iban_bruto = _obtener_campo_obligatorio("iban")
    cif = _obtener_campo_obligatorio("cif").upper()

    base_raw = payload.get("base_imponible")
    base_str = str(base_raw).strip() if base_raw is not None else ""
    if base_str == "":
      errores.append("Falta el campo 'base_imponible'.")

    territorio = (payload.get("territorio") or "No presencial").strip() or "No presencial"

    anio_raw = payload.get("año")
    if anio_raw is None:
      anio_raw = payload.get("anio")
    anio_str = str(anio_raw).strip() if anio_raw is not None else ""
    if not anio_str:
      errores.append("Falta el campo 'año'.")
    else:
      try:
        anio = int(anio_str)
      except (TypeError, ValueError):
        errores.append("El campo 'año' debe ser un número entero.")
      else:
        if anio < 2000 or anio > 2100:
          errores.append("El campo 'año' debe estar entre 2000 y 2100.")

    if errores:
      return JsonResponse({"ok": False, "error": "Datos inválidos", "errores": errores}, status=400)

    try:
      base_imponible = to_decimal(base_str)
    except (InvalidOperation, ValueError):
      return JsonResponse({"ok": False, "error": "Formato numérico inválido en base_imponible."}, status=400)

    if base_imponible < 0:
      return JsonResponse({"ok": False, "error": "La base imponible no puede ser negativa."}, status=400)

    cuota = (base_imponible * TASA_IMPUESTO).quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)
    importe_ingresar = cuota

    obj = Formulario411.objects.create(
      nif=nif,
      iban=iban_bruto.replace(" ", "").upper(),
      cif=cif,
      año=anio,
      base_imponible=base_imponible.quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP),
      territorio=territorio,
      cuota_tributaria=cuota,
      importe_ingresar=importe_ingresar,
    )
    return JsonResponse({"ok": True, "id": obj.id}, status=201)

  except InvalidOperation:
    return JsonResponse({"ok": False, "error": "Formato numérico inválido"}, status=400)
  except Exception as e:
    # log para depurar en consola
    print("ERROR guardando Formulario411:", e)
    print("Payload recibido:", payload)
    return JsonResponse({"ok": False, "error": str(e)}, status=500)
