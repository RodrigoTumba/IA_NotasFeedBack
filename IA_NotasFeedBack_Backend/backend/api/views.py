import openai
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

openai.api_key = settings.OPENAI_API_KEY

@api_view(['POST'])
def feedback(request):
    student = request.data

    prompt = f"""
    El estudiante {student.get('name')} tiene estas notas:
    N1: {student.get('n1')}, N2: {student.get('n2')}, N3: {student.get('n3')}.
    Promedio: {student.get('average')}, Estado: {student.get('status')}.
    
    Genera 3 recomendaciones prácticas y personalizadas para mejorar su rendimiento académico.
    1. Personaliza las recomendaciones según sus notas: enfócate más en las asignaturas con notas más bajas, toma en cuenta que la nota más alta es 20 y se debe de motivar al alumno cuando se acerca a esta nota.
    2. Devuelve el feedback en formato de viñetas, empezando cada recomendación con una breve frase en **negrita**, seguida de la explicación.
    3. Cada recomendación debe ser clara, accionable y fácil de entender.
    4. Mantén el contenido adecuado para mostrarlo en un modal de una aplicación web, sin incluir Markdown como `**` para negritas; usa solo texto plano que luego pueda procesarse para negrita en la UI.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
        )
        feedback_text = response.choices[0].message.content
        return Response({"feedback": feedback_text})
    except Exception as e:
        return Response({"error": str(e)}, status=500)