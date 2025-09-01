from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import io
import json
import os
import tempfile

try:
    import PyPDF2
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import pytesseract
    from PIL import Image
except Exception:
    PyPDF2 = None

from .models import SoilTest
from .forms import SoilTestForm


@login_required
def soil_test_form(request):
    if request.method == 'POST':
        form = SoilTestForm(request.POST)
        if form.is_valid():
            soil_test = form.save(commit=False)
            soil_test.user = request.user
            soil_test.calculate_quality_index()
            soil_test.save()
            messages.success(request, 'Soil test completed successfully!')
            return redirect('soil_report', soil_test.id)
    else:
        form = SoilTestForm()
    return render(request, 'soil/test_form.html', {'form': form})

@login_required
def soil_report(request, test_id):
    try:
        soil_test = SoilTest.objects.get(id=test_id, user=request.user)
        return render(request, 'soil/report.html', {'soil_test': soil_test})
    except SoilTest.DoesNotExist:
        messages.error(request, 'Soil test report not found!')
        return redirect('soil_test')

@login_required
def soil_history(request):
    tests = SoilTest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'soil/history.html', {'tests': tests})

@login_required
def generate_recommendations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        test_id = data.get('test_id')
        
        try:
            soil_test = SoilTest.objects.get(id=test_id, user=request.user)
            recommendations = []
            
            # pH recommendations
            if soil_test.ph_value < 6.0:
                recommendations.append("Add lime to increase soil pH and reduce acidity.")
            elif soil_test.ph_value > 7.5:
                recommendations.append("Add organic matter or sulfur to reduce soil pH.")
            
            # NPK recommendations
            if soil_test.nitrogen < 20:
                recommendations.append("Apply nitrogen-rich fertilizers like urea or compost.")
            if soil_test.phosphorus < 15:
                recommendations.append("Add phosphorus fertilizers like DAP or bone meal.")
            if soil_test.potassium < 150:
                recommendations.append("Apply potassium fertilizers like MOP or wood ash.")
            
            # Moisture recommendations
            if soil_test.moisture < 30:
                recommendations.append("Improve irrigation system and add organic mulch.")
            elif soil_test.moisture > 70:
                recommendations.append("Improve drainage to prevent waterlogging.")
            
            # Organic matter recommendations
            if soil_test.organic_matter < 2:
                recommendations.append("Add compost, farmyard manure, or green manure.")
            
            soil_test.recommendations = "; ".join(recommendations)
            soil_test.save()
            
            return JsonResponse({'recommendations': recommendations})
            
        except SoilTest.DoesNotExist:
            return JsonResponse({'error': 'Soil test not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def pdf_tools(request):
    return render(request, 'soil/pdf_tools.html')


@login_required
@csrf_exempt
def generate_grid(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    if PyPDF2 is None:
        return JsonResponse({'error': 'PyPDF2/reportlab not installed'}, status=500)
    try:
        pdf = request.FILES.get('template')
        grid_size = int(request.POST.get('grid_size', '50'))
        reader = PyPDF2.PdfReader(pdf)
        page = reader.pages[0]
        media_box = page.mediabox
        width = float(media_box.width)
        height = float(media_box.height)
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(width, height))
        can.setStrokeColorRGB(0.8, 0.8, 0.8)
        for x in range(0, int(width), grid_size):
            can.line(x, 0, x, height)
            if x % (grid_size * 5) == 0:
                can.setStrokeColorRGB(0.6, 0.6, 0.6)
                can.line(x, 0, x, height)
                can.setStrokeColorRGB(0.8, 0.8, 0.8)
        for y in range(0, int(height), grid_size):
            can.line(0, y, width, y)
            if y % (grid_size * 5) == 0:
                can.setStrokeColorRGB(0.6, 0.6, 0.6)
                can.line(0, y, width, y)
                can.setStrokeColorRGB(0.8, 0.8, 0.8)
        can.setFillColorRGB(1, 0, 0)
        can.setFont("Helvetica", 8)
        for x in range(0, int(width), grid_size * 5):
            can.drawString(x, 10, str(x))
        for y in range(0, int(height), grid_size * 5):
            can.drawString(10, y, str(y))
        can.save()
        packet.seek(0)
        overlay = PyPDF2.PdfReader(packet)
        writer = PyPDF2.PdfWriter()
        page.merge_page(overlay.pages[0])
        writer.add_page(page)
        out_stream = io.BytesIO()
        writer.write(out_stream)
        out_stream.seek(0)
        resp = HttpResponse(out_stream.read(), content_type='application/pdf')
        resp['Content-Disposition'] = 'attachment; filename="template_with_grid.pdf"'
        return resp
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@csrf_exempt
def extract_text_from_pdf(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    if PyPDF2 is None or 'pytesseract' not in globals():
        return JsonResponse({'error': 'Required libraries not installed'}, status=500)
    try:
        pdf_file = request.FILES.get('pdf')
        if not pdf_file:
            return JsonResponse({'error': 'No PDF file provided'}, status=400)
        
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            for chunk in pdf_file.chunks():
                temp_pdf.write(chunk)
            temp_pdf_path = temp_pdf.name
        
        # Extract text using PyPDF2 and OCR with pytesseract
        extracted_text = {}
        reader = PyPDF2.PdfReader(temp_pdf_path)
        
        # Process first page only for now
        page = reader.pages[0]
        text = page.extract_text()
        
        # If text extraction is poor, try OCR
        if not text or len(text) < 100:  # Arbitrary threshold
            # Convert PDF to image for OCR
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_img:
                temp_img_path = temp_img.name
            
            # Use external tool to convert PDF to image (this is a placeholder)
            # In a real implementation, you might use pdf2image or another library
            # For now, we'll just use the text extraction from PyPDF2
            
            # Placeholder for OCR
            # text = pytesseract.image_to_string(Image.open(temp_img_path))
            # os.unlink(temp_img_path)
        
        # Clean up the temporary PDF file
        os.unlink(temp_pdf_path)
        
        # Extract common soil test fields
        # This is a simple example - in a real app, you'd use more sophisticated parsing
        extracted_data = {}
        
        # Look for common patterns in soil reports
        if 'pH' in text or 'ph' in text.lower():
            # Find pH value (typically followed by a number)
            import re
            ph_match = re.search(r'pH\s*[:-]?\s*(\d+\.?\d*)', text, re.IGNORECASE)
            if ph_match:
                extracted_data['ph_value'] = ph_match.group(1)
        
        # Look for nitrogen (N)
        n_match = re.search(r'N\s*[:-]?\s*(\d+\.?\d*)', text)
        if n_match:
            extracted_data['nitrogen'] = n_match.group(1)
        
        # Look for phosphorus (P)
        p_match = re.search(r'P\s*[:-]?\s*(\d+\.?\d*)', text)
        if p_match:
            extracted_data['phosphorus'] = p_match.group(1)
        
        # Look for potassium (K)
        k_match = re.search(r'K\s*[:-]?\s*(\d+\.?\d*)', text)
        if k_match:
            extracted_data['potassium'] = k_match.group(1)
        
        return JsonResponse({
            'success': True,
            'extracted_text': text[:500],  # Return first 500 chars as preview
            'extracted_data': extracted_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_exempt
def fill_pdf(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    if PyPDF2 is None:
        return JsonResponse({'error': 'PyPDF2/reportlab not installed'}, status=500)
    try:
        template = request.FILES.get('template')
        mapping_json = request.POST.get('mapping', '{}')
        data_json = request.POST.get('data', '{}')
        mapping = json.loads(mapping_json)
        form_data = json.loads(data_json)
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 10)
        for field_name, value in form_data.items():
            if field_name in mapping:
                coords = mapping[field_name]
                x = float(coords.get('x', 0))
                y = float(coords.get('y', 0))
                can.drawString(x, y, str(value))
        can.save()
        packet.seek(0)
        overlay = PyPDF2.PdfReader(packet)
        existing = PyPDF2.PdfReader(template)
        writer = PyPDF2.PdfWriter()
        for i in range(len(existing.pages)):
            page = existing.pages[i]
            if i < len(overlay.pages):
                page.merge_page(overlay.pages[i])
            writer.add_page(page)
        out_stream = io.BytesIO()
        writer.write(out_stream)
        out_stream.seek(0)
        resp = HttpResponse(out_stream.read(), content_type='application/pdf')
        resp['Content-Disposition'] = 'attachment; filename="filled_soil_report.pdf"'
        return resp
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
