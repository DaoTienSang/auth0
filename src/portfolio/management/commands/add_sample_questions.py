from django.core.management.base import BaseCommand
from portfolio.models import ChatbotQuestion

class Command(BaseCommand):
    help = 'Adds sample questions to the chatbot database'

    def handle(self, *args, **options):
        questions = [
            'Tôi cần mua cổ phiếu ở đâu?',
            'Tôi nên đầu tư vào cổ phiếu ngành nào ở Việt Nam?',
            'Tôi có nên đầu tư vào công nghệ không?',
            'Làm thế nào để phân tích cổ phiếu cơ bản?',
            'Chỉ số P/E là gì?',
            'Làm sao để tạo danh mục đầu tư đa dạng?',
            'Các chiến lược đầu tư dài hạn phổ biến?',
            'Cách quản lý rủi ro trong đầu tư chứng khoán?'
        ]

        for question in questions:
            ChatbotQuestion.objects.get_or_create(question_text=question)
        
        self.stdout.write(self.style.SUCCESS('Successfully added sample questions'))