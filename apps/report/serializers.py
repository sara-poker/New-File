from rest_framework.serializers import BaseSerializer


class ContractReportSerializer(BaseSerializer):

    def to_representation(self, instance):
        request = self.context['request']
        params = request.query_params.get('report_type')
        if params == 'total_price':
            return {
                'province': str(instance.province.english_title),
                'data': instance.cost
            }
        elif params == 'deposit_amount':
            return {
                'province': str(instance.province.english_title),
                'data': instance.total_settlements
            }
        elif params == 'percent_of_total':
            return {
                'province': str(instance.province.english_title),
                'data': round((instance.total_settlements / instance.cost) * 100, 2)
            }
