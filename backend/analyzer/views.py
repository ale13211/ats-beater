import fitz
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import analyze

MAX_FILE_SIZE = 3 * 1024 * 1024

class AnalysisInput(serializers.Serializer):
    job_description = serializers.CharField(max_length=20000)
    resume_text = serializers.CharField(max_length=30000, required=False, allow_blank=True)
    resume_file = serializers.FileField(required=False)

    def validate(self, attrs):
        if not attrs.get("resume_text") and not attrs.get("resume_file"):
            raise serializers.ValidationError("Provide resume_text or resume_file.")
        f = attrs.get("resume_file")
        if f and (f.size > MAX_FILE_SIZE or not f.name.lower().endswith(".pdf")):
            raise serializers.ValidationError("Only PDF files up to 3 MB are supported.")
        return attrs

class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"})

class AnalyzeView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        data = AnalysisInput(data=request.data)
        data.is_valid(raise_exception=True)
        validated = data.validated_data
        resume = validated.get("resume_text", "")
        if file := validated.get("resume_file"):
            try:
                document = fitz.open(stream=file.read(), filetype="pdf")
                if document.page_count > 10:
                    return Response({"error": "Maximum 10 pages."}, status=400)
                resume = "\n".join(page.get_text() for page in document)
                document.close()
            except Exception:
                return Response({"error": "Invalid or unreadable PDF."}, status=400)
        if not resume.strip():
            return Response({"error": "No extractable text in resume."}, status=400)
        return Response(analyze(resume[:30000], validated["job_description"]))
