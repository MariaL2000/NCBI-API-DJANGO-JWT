from django.shortcuts import render, redirect
import requests
from xml.etree import ElementTree as ET

def is_valid_dna_sequence(sequence):
    sequence = sequence.upper()
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    return all(nucleotide in valid_nucleotides for nucleotide in sequence)

def sequence_view(request):
    query = request.GET.get('query', '')
    if query:
        if not is_valid_dna_sequence(query):
            return render(request, 'results.html', {'error': 'La cadena proporcionada no es una secuencia de ADN válida.'})

        url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term={query}&retmode=xml'
        response = requests.get(url)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            ids = [id_elem.text for id_elem in root.findall('.//Id')]
            
            if ids:
                request.session['dna_ids'] = ids
                return redirect('sequences:results_view')
            else:
                return render(request, 'results.html', {'error': 'No se encontraron resultados para la consulta.'})
        else:
            return render(request, 'results.html', {'error': 'Error al consultar la API de NCBI.'})
    
    return render(request, 'sequence.html')

def results_view(request):
    ids = request.session.get('dna_ids', [])
    results = []

    if ids:
        for id in ids:
            detail_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id={id}&retmode=xml'
            detail_response = requests.get(detail_url)
            if detail_response.status_code == 200:
                detail_root = ET.fromstring(detail_response.content)
                for seq in detail_root.findall('.//GBSeq'):
                    seq_id = seq.find('GBSeq_primary-accession').text
                    seq_name = seq.find('GBSeq_definition').text
                    seq_length = seq.find('GBSeq_length').text
                    seq_description = seq.find('GBSeq_organism').text
                    results.append({
                        'id': seq_id,
                        'name': seq_name,
                        'length': seq_length,
                        'description': seq_description,
                    })
        del request.session['dna_ids']
    else:
        return render(request, 'results.html', {'error': 'No se encontraron resultados.'})

    return render(request, 'results.html', {'results': results})



def about_view(request):
    return render(request, 'about.html') 

