import json
import logging

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from .form import SummaryForm
from .summarizer import summarize

logger = logging.getLogger(__name__)

SUCCESS = 0
ERROR = 1


class SummaryView(generic.FormView):
    template_name = 'summary.html'
    form_class = SummaryForm
    success_url = reverse_lazy('summary:summary')

    def form_valid(self, form):
        if self.request.is_ajax():
            logger.debug('Request is Ajax.')
            try:
                text = form.cleaned_data['text']
                summarized_text = summarize(text)
                data_json = json.dumps({'summary': summarized_text,
                                        'status': SUCCESS,
                                        'errorMessage': None})
            except Exception:
                logger.exception('Exception occurs.')
                data_json = json.dumps({'summary': None,
                                        'status': ERROR,
                                        'errorMessage': '要約に失敗しました。'})

            response = HttpResponse(data_json, content_type='application/json')
        else:
            logger.debug('Request is not Ajax.')
            response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        if self.request.is_ajax():
            logger.debug('Request is Ajax.')
            response = HttpResponse({'error': 'Unprocessable Entity'})
            response.status_code = 422
        else:
            logger.debug('Request is not Ajax.')
            response = super().form_invalid(form)
        return response
